from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from TTS.api import TTS
import os
import uuid
import logging
import urllib.request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Offline Text-to-Speech Generator")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ensure audio directory exists
os.makedirs("static/audio", exist_ok=True)

# Global variables for TTS
tts = None
tts_model_type = None
speaker_wav_path = None

def download_speaker_sample():
    """Download a sample speaker WAV file for XTTS v2"""
    speaker_dir = "speaker_samples"
    os.makedirs(speaker_dir, exist_ok=True)
    speaker_path = os.path.join(speaker_dir, "female_speaker.wav")
    
    if not os.path.exists(speaker_path):
        try:
            # Download a sample speaker file from Coqui's examples
            logger.info("Downloading speaker sample for voice cloning...")
            url = "https://github.com/coqui-ai/TTS/raw/dev/tests/data/ljspeech/wavs/LJ001-0001.wav"
            urllib.request.urlretrieve(url, speaker_path)
            logger.info(f"Speaker sample downloaded to {speaker_path}")
            return speaker_path
        except Exception as e:
            logger.error(f"Could not download speaker sample: {e}")
            return None
    return speaker_path

# Initialize TTS model
logger.info("Loading TTS model... This may take a few minutes on first run.")
try:
    # Strategy: Try VITS first (fast, high-quality, no speaker needed)
    # It's the best balance between quality and simplicity
    model_name = "tts_models/en/ljspeech/vits"
    logger.info(f"Attempting to load {model_name}...")
    tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
    tts_model_type = "single_speaker"
    logger.info(f"✓ TTS model loaded successfully: {model_name}")
    logger.info("Model type: Single-speaker English (LJSpeech VITS)")
except Exception as e:
    logger.error(f"Error loading VITS model: {e}")
    try:
        # Fallback to Tacotron2
        model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        logger.info(f"Attempting fallback to {model_name}...")
        tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
        tts_model_type = "single_speaker"
        logger.info(f"✓ TTS model loaded successfully: {model_name}")
    except Exception as e2:
        logger.error(f"Error loading Tacotron2 model: {e2}")
        # Last resort: try a very simple model
        try:
            model_name = "tts_models/en/ljspeech/glow-tts"
            logger.info(f"Attempting final fallback to {model_name}...")
            tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
            tts_model_type = "single_speaker"
            logger.info(f"✓ TTS model loaded successfully: {model_name}")
        except Exception as e3:
            logger.error(f"All model loading attempts failed: {e3}")
            tts = None
            tts_model_type = None


class TTSRequest(BaseModel):
    text: str
    language: str = "en"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech and return audio file URL
    """
    if tts is None:
        raise HTTPException(status_code=500, detail="TTS model not loaded. Please check server logs.")
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 1000:
        raise HTTPException(status_code=400, detail="Text is too long (max 1000 characters)")
    
    try:
        # Generate unique filename for the audio
        audio_id = str(uuid.uuid4())
        audio_filename = f"{audio_id}.wav"
        audio_path = os.path.join("static", "audio", audio_filename)
        
        logger.info(f"Generating speech for: '{request.text[:50]}...'")
        
        # Generate speech
        tts.tts_to_file(
            text=request.text,
            file_path=audio_path
        )
        
        logger.info(f"✓ Audio generated: {audio_filename}")
        
        return {
            "success": True,
            "audio_url": f"/static/audio/{audio_filename}",
            "message": "Speech generated successfully!"
        }
    
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": tts is not None,
        "model_type": tts_model_type
    }


@app.delete("/api/audio/{filename}")
async def delete_audio(filename: str):
    """Delete generated audio file"""
    try:
        audio_path = os.path.join("static", "audio", filename)
        if os.path.exists(audio_path):
            os.remove(audio_path)
            return {"success": True, "message": "Audio deleted"}
        else:
            raise HTTPException(status_code=404, detail="Audio file not found")
    except Exception as e:
        logger.error(f"Error deleting audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 60)
    logger.info("🎙️  Offline Text-to-Speech Generator")
    logger.info("=" * 60)
    logger.info("Server starting on http://127.0.0.1:8000")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

