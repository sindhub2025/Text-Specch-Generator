# 🎙️ Offline Text-to-Speech Generator

A fully local, offline Text-to-Speech web application that runs on `http://localhost:8000` and produces natural human-sounding voice using **Coqui XTTS v2**, an open-source state-of-the-art TTS model.

## ✨ Features

- ✅ **Fully Offline**: No internet required after initial setup
- ✅ **Natural Voice**: Uses Coqui XTTS v2 for realistic human-sounding speech
- ✅ **Multilingual**: Supports 15+ languages (English, Spanish, French, German, Italian, Portuguese, Polish, Turkish, Russian, Dutch, Czech, Arabic, Chinese, Japanese, Korean, Hindi)
- ✅ **No Paid APIs**: Completely free and open-source
- ✅ **Privacy-Focused**: All processing happens locally on your machine
- ✅ **Modern UI**: Clean, responsive web interface
- ✅ **Audio Download**: Download generated speech as WAV files

## 📁 Folder Structure

```
Text-Specch-Generator/
├── app.py                  # FastAPI backend server
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── static/                # Static files
│   ├── audio/            # Generated audio files (created at runtime)
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── templates/             # HTML templates
    └── index.html        # Main page
```

## 🔧 Installation

### Prerequisites

- **Python 3.9 or higher** (Python 3.10 recommended)
- **pip** (Python package manager)
- **4GB+ RAM** (8GB+ recommended for better performance)
- **2GB+ free disk space** (for models)

### Step 1: Clone the Repository

```bash
git clone https://github.com/sindhub2025/Text-Specch-Generator.git
cd Text-Specch-Generator
```

### Step 2: Create a Virtual Environment (Recommended)

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: The first installation will download the XTTS v2 model (approximately 1.8GB). This happens automatically when you first run the application.

### Installation Time

- Initial pip install: 5-10 minutes
- First-time model download (automatic on first run): 5-15 minutes depending on internet speed
- Subsequent runs: Instant (model is cached)

## 🚀 Running the Application

### Start the Server

```bash
python app.py
```

Or alternatively:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

### Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

### First Run

On the first run, the application will:
1. Download the XTTS v2 model (~1.8GB) automatically
2. Cache it in your home directory (`~/.local/share/tts/`)
3. Load the model into memory

This process takes 5-15 minutes on first run. Subsequent runs are much faster.

## 📖 How to Use

1. **Enter Text**: Type or paste the text you want to convert to speech (max 1000 characters)
2. **Select Language**: Choose your desired language from the dropdown
3. **Generate Speech**: Click the "Generate Speech" button
4. **Listen**: The audio player will appear with your generated speech
5. **Download**: Click the download button to save the audio file

### Keyboard Shortcuts

- **Ctrl/Cmd + Enter** in the text area: Generate speech

## 🛠️ Technical Details

### Backend Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Coqui TTS**: Open-source Text-to-Speech library
- **XTTS v2**: State-of-the-art multilingual TTS model

### Frontend Stack

- **HTML5**: Structure and semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No frameworks, just pure JS for simplicity

### Model Information

**Coqui XTTS v2** (Cross-lingual Text-to-Speech)
- Multi-speaker, multilingual TTS model
- High-quality, natural-sounding voice
- Supports 16+ languages
- Based on transformer architecture
- Zero-shot voice cloning capabilities

## 🔍 API Endpoints

### `GET /`
Serves the main HTML interface

### `POST /api/tts`
Generate speech from text

**Request Body:**
```json
{
  "text": "Your text here",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "audio_url": "/static/audio/[uuid].wav",
  "message": "Speech generated successfully"
}
```

### `GET /api/health`
Check API and model status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## ⚙️ Configuration

### Changing Server Settings

Edit `app.py` (bottom of file):

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
```

- Change `host` to `"0.0.0.0"` to allow access from other devices on your network
- Change `port` to use a different port number

### Using GPU Acceleration (Optional)

If you have an NVIDIA GPU with CUDA installed, you can enable GPU acceleration for faster generation:

In `app.py`, change:
```python
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=False)
```

to:
```python
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=True)
```

Also install CUDA-enabled PyTorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 🐛 Troubleshooting

### Model Download Issues

If the model fails to download automatically:
1. Check your internet connection
2. Manually download from: https://huggingface.co/coqui/XTTS-v2
3. Place in `~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/`

### Memory Issues

If you encounter out-of-memory errors:
- Close other applications
- Try processing shorter text segments
- Consider using a machine with more RAM

### Port Already in Use

If port 8000 is already in use:
```bash
python app.py --port 8001
```

Or edit the port in `app.py`

### Audio Not Playing

- Check browser console for errors
- Ensure browser supports HTML5 audio
- Try a different browser (Chrome/Firefox recommended)

## 📝 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **Coqui TTS**: Open-source Text-to-Speech library
- **XTTS v2**: State-of-the-art multilingual TTS model
- **FastAPI**: Modern web framework
- **Community**: All contributors and users

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ using open-source technologies**