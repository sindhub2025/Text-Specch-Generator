from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from TTS.api import TTS
import os
import uuid
import logging

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

# Initialize TTS model (Coqui XTTS v2)
logger.info("Loading TTS model... This may take a few minutes on first run.")
try:
    # Using XTTS v2 for high-quality multilingual TTS
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=False)
    logger.info("TTS model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading TTS model: {e}")
    tts = None


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
        raise HTTPException(status_code=500, detail="TTS model not loaded")
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 1000:
        raise HTTPException(status_code=400, detail="Text is too long (max 1000 characters)")
    
    try:
        # Generate unique filename for the audio
        audio_id = str(uuid.uuid4())
        audio_filename = f"{audio_id}.wav"
        audio_path = os.path.join("static", "audio", audio_filename)
        
        logger.info(f"Generating speech for text: {request.text[:50]}...")
        
        # Generate speech
        # XTTS v2 requires a speaker reference, we'll use the default
        tts.tts_to_file(
            text=request.text,
            language=request.language,
            file_path=audio_path,
            speaker_wav=None,  # Using default speaker
            emotion=None
        )
        
        logger.info(f"Audio generated successfully: {audio_filename}")
        
        return {
            "success": True,
            "audio_url": f"/static/audio/{audio_filename}",
            "message": "Speech generated successfully"
        }
    
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": tts is not None
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
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
