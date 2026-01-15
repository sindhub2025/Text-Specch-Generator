# 🚀 Quick Start Guide

This guide will help you get the Text-to-Speech application up and running quickly.

## Installation Steps

### Option 1: Using the Run Script (Easiest)

**On Linux/macOS:**
```bash
./run.sh
```

**On Windows:**
```cmd
run.bat
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the server

### Option 2: Manual Installation

1. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

2. **Activate Virtual Environment**
   
   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Start the Server**
   ```bash
   python app.py
   ```

## First Run Experience

### What to Expect

1. **Model Download** (First time only)
   - The application will automatically download the TTS model
   - Size: ~150-300 MB depending on the model
   - Time: 2-10 minutes depending on internet speed
   - Location: `~/.local/share/tts/` (cached for future use)

2. **Model Loading**
   - Takes 10-30 seconds to load into memory
   - Only happens once per server start

3. **Server Ready**
   - You'll see: "Server starting on http://127.0.0.1:8000"
   - Open this URL in your browser

## Using the Application

1. **Open Browser**
   ```
   http://localhost:8000
   ```

2. **Enter Text**
   - Type any text (up to 1000 characters)
   - Example: "Hello, this is a test of the text to speech system."

3. **Generate Speech**
   - Click "Generate Speech" button
   - Wait 5-15 seconds (depends on text length)

4. **Listen & Download**
   - Audio player appears automatically
   - Click play to listen
   - Click download to save the audio file

## Testing the Installation

### Test 1: Health Check

Open in browser or use curl:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "single_speaker"
}
```

### Test 2: Generate Sample Speech

1. Go to http://localhost:8000
2. Enter: "This is a test."
3. Click "Generate Speech"
4. Verify audio plays correctly

### Test 3: Different Text Lengths

- Short: "Hello world."
- Medium: "The quick brown fox jumps over the lazy dog."
- Long: A paragraph of text (100-200 words)

## Troubleshooting

### Port Already in Use

If port 8000 is busy:

**Edit app.py:**
```python
uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
```

Or run with custom port:
```bash
python -c "from app import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8001)"
```

### Model Loading Fails

Check logs for:
- Internet connection (for first download)
- Disk space (need ~2GB free)
- Python version (need 3.9+)

### Out of Memory

If generation fails with memory error:
- Try shorter text
- Close other applications
- Restart the server

### Audio Not Playing

- Try a different browser (Chrome/Firefox recommended)
- Check browser console for errors (F12)
- Verify the audio file was created in `static/audio/`

## Performance Tips

### Speed up Generation

1. **Use GPU** (if available)
   - Edit `app.py`: Change `gpu=False` to `gpu=True`
   - Install CUDA-enabled PyTorch

2. **Keep Server Running**
   - Model stays loaded in memory
   - Subsequent generations are faster

3. **Shorter Text**
   - Break long text into sentences
   - Generate separately

### Reduce Memory Usage

1. Use VITS model (fastest, smallest)
2. Close browser tabs after generating
3. Restart server periodically

## System Requirements

### Minimum
- Python 3.9+
- 4GB RAM
- 2GB disk space
- Any modern browser

### Recommended
- Python 3.10+
- 8GB RAM
- 5GB disk space
- Chrome or Firefox browser

### With GPU (Optional)
- NVIDIA GPU with 4GB+ VRAM
- CUDA 11.8+
- cuDNN 8.x

## File Locations

### Generated Audio
```
static/audio/*.wav
```

### TTS Models Cache
```
~/.local/share/tts/        (Linux/macOS)
C:\Users\<user>\.local\share\tts\  (Windows)
```

### Log Files
- Server logs: Console output
- Access logs: Console output

## Security Notes

1. **Local Only by Default**
   - Server binds to 127.0.0.1 (localhost)
   - Not accessible from other machines

2. **Network Access** (Optional)
   - Change host to "0.0.0.0" for LAN access
   - Add firewall rules if needed
   - Be cautious on public networks

3. **Generated Files**
   - Audio files accumulate in `static/audio/`
   - Clean up periodically
   - Not automatically deleted

## Next Steps

After successful installation:

1. ✅ Bookmark http://localhost:8000
2. ✅ Test with various text lengths
3. ✅ Explore language options (English by default)
4. ✅ Download and save favorite generations
5. ✅ Check the main README.md for advanced features

## Support

- Check README.md for detailed documentation
- Review server logs for error messages
- Open GitHub issue for bugs/features

---

**Happy TTS Generation! 🎙️**
