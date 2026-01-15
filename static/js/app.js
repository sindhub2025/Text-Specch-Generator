// DOM Elements
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.querySelector('.btn-text');
const spinner = document.querySelector('.spinner');
const outputSection = document.getElementById('outputSection');
const audioPlayer = document.getElementById('audioPlayer');
const downloadBtn = document.getElementById('downloadBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const statusMessage = document.getElementById('statusMessage');

let currentAudioUrl = null;

// Update character count
textInput.addEventListener('input', () => {
    const count = textInput.value.length;
    charCount.textContent = count;
    
    // Change color based on length
    if (count > 900) {
        charCount.style.color = '#dc2626';
    } else if (count > 700) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '#666';
    }
});

// Generate speech
generateBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    
    // Validation
    if (!text) {
        showError('Please enter some text to convert to speech.');
        return;
    }
    
    if (text.length > 1000) {
        showError('Text is too long. Please limit to 1000 characters.');
        return;
    }
    
    // Hide previous results and errors
    hideError();
    outputSection.style.display = 'none';
    
    // Show loading state
    setLoading(true);
    
    try {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: "en"
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to generate speech');
        }
        
        // Display the audio
        currentAudioUrl = data.audio_url;
        audioPlayer.src = currentAudioUrl;
        outputSection.style.display = 'block';
        statusMessage.textContent = data.message || 'Speech generated successfully!';
        
        // Scroll to the audio player
        outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        setLoading(false);
    }
});

// Download audio
downloadBtn.addEventListener('click', () => {
    if (currentAudioUrl) {
        const link = document.createElement('a');
        link.href = currentAudioUrl;
        link.download = `tts_audio_${Date.now()}.wav`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

// Allow Enter key with Ctrl/Cmd to generate
textInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        generateBtn.click();
    }
});

// Helper functions
function setLoading(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        btnText.textContent = 'Generating...';
        spinner.style.display = 'inline-block';
        loadingIndicator.style.display = 'block';
    } else {
        generateBtn.disabled = false;
        btnText.textContent = 'Generate Speech';
        spinner.style.display = 'none';
        loadingIndicator.style.display = 'none';
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Check API health on page load
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API Health:', data);
        
        if (!data.model_loaded) {
            showError('TTS model is not loaded. Please check the server logs.');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        showError('Unable to connect to the server. Please make sure the server is running.');
    }
}

// Run health check on page load
checkHealth();

