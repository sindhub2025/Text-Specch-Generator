# 🎯 Project Architecture

## Overview
This document provides a technical overview of the Offline Text-to-Speech Generator architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           HTML/CSS/JavaScript Frontend                │  │
│  │  • Text input with validation                         │  │
│  │  • Character counter                                  │  │
│  │  • Generate button with loading states               │  │
│  │  • Audio player with download                        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │ (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  POST /api/tts                                        │  │
│  │    • Validate text input                             │  │
│  │    • Generate unique filename                        │  │
│  │    • Call TTS engine                                 │  │
│  │    • Return audio URL                                │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  GET /api/health                                      │  │
│  │    • Check model status                              │  │
│  │    • Return system health                            │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  DELETE /api/audio/{filename}                        │  │
│  │    • Validate filename (security)                    │  │
│  │    • Delete audio file                               │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Coqui TTS Engine                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Model Loading Strategy:                             │  │
│  │  1. VITS (primary) - Fast, high quality             │  │
│  │  2. Tacotron2-DDC (fallback 1)                      │  │
│  │  3. Glow-TTS (fallback 2)                           │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Process:                                            │  │
│  │  • Text → Phonemes                                   │  │
│  │  • Phonemes → Mel Spectrogram                       │  │
│  │  • Mel Spectrogram → Audio (WAV)                    │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   File System                                │
│  static/audio/                                              │
│    • Generated WAV files                                    │
│    • Served via static file mount                          │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
Text-Speech-Generator/
├── app.py                    # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # Comprehensive documentation
├── QUICKSTART.md            # Quick start guide
├── ARCHITECTURE.md          # This file
├── run.sh                   # Unix/Linux run script
├── run.bat                  # Windows run script
│
├── static/                  # Static files served by FastAPI
│   ├── audio/              # Generated audio files (gitignored)
│   │   └── .gitkeep        # Keep directory in git
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── app.js          # Frontend JavaScript
│
└── templates/               # Jinja2 templates
    └── index.html          # Main application page
```

## Component Details

### Frontend (Browser)

**Technologies:**
- HTML5 for structure
- CSS3 for styling (gradients, animations)
- Vanilla JavaScript (no frameworks)

**Key Features:**
- Character counter (live update)
- Input validation (client-side)
- Loading states and spinners
- Error message display
- Audio player integration
- Download functionality

**API Communication:**
```javascript
// Generate speech
POST /api/tts
{
  "text": "Hello world",
  "language": "en"
}

Response:
{
  "success": true,
  "audio_url": "/static/audio/uuid.wav",
  "message": "Speech generated successfully!"
}
```

### Backend (FastAPI)

**Technologies:**
- FastAPI framework
- Uvicorn ASGI server
- Pydantic for validation
- Python 3.9+ compatible

**Key Features:**
- REST API endpoints
- Request validation
- Error handling
- Static file serving
- Security measures (path traversal prevention)
- Logging (no sensitive data)

**Endpoints:**

1. **GET /** - Serve main page
   - Returns HTML template

2. **POST /api/tts** - Generate speech
   - Input: JSON with text and language
   - Validation: Length, empty check
   - Output: Audio URL
   - Error handling: 400, 500 codes

3. **GET /api/health** - Health check
   - Returns model status
   - Used by frontend on load

4. **DELETE /api/audio/{filename}** - Delete audio
   - Filename validation (regex)
   - Path traversal prevention
   - File existence check

### TTS Engine (Coqui TTS)

**Model Strategy:**
1. Try VITS (fastest, best quality)
2. Fallback to Tacotron2-DDC
3. Final fallback to Glow-TTS

**Models Details:**

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| VITS | ~150MB | Fast | High | Primary |
| Tacotron2 | ~200MB | Medium | High | Fallback |
| Glow-TTS | ~120MB | Fast | Good | Last resort |

**Process Flow:**
```
Text Input
    ↓
Text Normalization
    ↓
Phoneme Conversion
    ↓
Acoustic Model (VITS/Tacotron2/Glow)
    ↓
Mel Spectrogram
    ↓
Vocoder (built-in)
    ↓
Audio Waveform (WAV)
    ↓
File Output
```

## Data Flow

### Speech Generation Flow

```
1. User enters text in browser
   ↓
2. JavaScript validates input (length, empty)
   ↓
3. AJAX POST request to /api/tts
   ↓
4. FastAPI validates request
   ↓
5. Generate unique UUID for filename
   ↓
6. Call TTS.tts_to_file()
   ↓
7. VITS model processes text
   ↓
8. WAV file saved to static/audio/
   ↓
9. Return JSON with audio URL
   ↓
10. Frontend displays audio player
   ↓
11. User plays/downloads audio
```

## Security Considerations

### Implemented Security

1. **Path Traversal Prevention**
   - Filename regex validation
   - Absolute path checking
   - Whitelist approach

2. **Input Validation**
   - Text length limits (1000 chars)
   - Empty text checks
   - Type validation (Pydantic)

3. **Privacy**
   - No text logging (only length)
   - Local processing
   - No external API calls

4. **File Management**
   - Unique UUIDs prevent conflicts
   - Generated files in dedicated directory
   - Proper error handling

### Security Best Practices

- ✅ Input sanitization
- ✅ Path traversal protection
- ✅ No sensitive data logging
- ✅ Error message sanitization
- ✅ Local-only by default (127.0.0.1)

## Performance Characteristics

### Model Loading
- **First run**: 2-10 minutes (download + load)
- **Subsequent runs**: 10-30 seconds (load only)
- **Memory usage**: ~500MB-1GB RAM

### Speech Generation
- **Short text** (< 50 chars): 2-5 seconds
- **Medium text** (50-200 chars): 5-10 seconds
- **Long text** (200-1000 chars): 10-20 seconds

### Optimization Opportunities

1. **GPU Acceleration**
   - 3-5x faster generation
   - Requires NVIDIA GPU + CUDA

2. **Model Caching**
   - Keep server running
   - Avoid reload overhead

3. **Batch Processing**
   - Process multiple requests
   - Queue system for heavy load

## Deployment

### Development
```bash
python app.py
# Runs on http://127.0.0.1:8000
```

### Production Considerations

1. **Use Production Server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
   ```

2. **Add Reverse Proxy** (Nginx/Apache)
   - SSL/TLS termination
   - Load balancing
   - Static file serving

3. **Environment Variables**
   - Port configuration
   - Model selection
   - GPU enable/disable

4. **Monitoring**
   - Health check endpoint
   - Application logs
   - Resource usage

## Extensibility

### Easy Extensions

1. **Multiple Voices**
   - Add multi-speaker models
   - Voice selection UI

2. **More Languages**
   - Use multilingual models
   - Language selector

3. **Voice Cloning**
   - Add XTTS v2 support
   - Upload speaker samples

4. **Audio Effects**
   - Speed control
   - Pitch adjustment
   - Effects processing

### API Extensions

```python
# Example: Add speed control
@app.post("/api/tts/advanced")
async def tts_advanced(
    text: str,
    speed: float = 1.0,
    pitch: float = 1.0
):
    # Implementation
    pass
```

## Testing

### Manual Testing
1. UI interaction
2. Different text lengths
3. Error conditions
4. Download functionality

### Automated Testing (Future)
- Unit tests for endpoints
- Integration tests for TTS
- Load testing
- Security testing

## Maintenance

### Regular Tasks
1. Clean up old audio files
2. Monitor disk space
3. Check for TTS library updates
4. Review logs for errors

### Backup
- Application code (Git)
- Configuration files
- Custom models (if any)

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Model won't load | Network/disk | Check connection & space |
| Out of memory | Large model | Reduce text length |
| Slow generation | CPU only | Enable GPU if available |
| Port in use | Another app | Change port in app.py |

## License & Credits

- **Coqui TTS**: Mozilla Public License 2.0
- **FastAPI**: MIT License
- **This Project**: MIT License

---

**Version**: 1.0.0  
**Last Updated**: January 2026
