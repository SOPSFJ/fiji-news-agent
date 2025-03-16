import os
import datetime
import pyttsx3
from gtts import gTTS
import threading

class TextToSpeech:
    def __init__(self):
        # Create the audio directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Initialize pyttsx3 TTS engine
        self.offline_engine = pyttsx3.init()
        
        # Configure voice properties
        self.offline_engine.setProperty('rate', 150)  # Speed of speech
        self.offline_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices and set to a English voice if available
        voices = self.offline_engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower():
                self.offline_engine.setProperty('voice', voice.id)
                break
    
    def convert(self, text):
        """Convert text to speech and return the filename"""
        if not text:
            return None
        
        # Create a timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/audio_{timestamp}.mp3"
        
        # Try to use gTTS (online) first, fall back to pyttsx3 (offline)
        try:
            self._convert_online(text, filename)
        except Exception as e:
            print(f"Online TTS failed: {str(e)}. Falling back to offline TTS.")
            self._convert_offline(text, filename)
        
        return filename
    
    def _convert_online(self, text, filename):
        """Convert text to speech using gTTS (requires internet)"""
        # Break text into chunks if it's very long (gTTS has limits)
        max_chars = 5000
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        
        # Process only the first chunk for now to avoid lengthy processing
        # In a production system, you might want to process all chunks and combine them
        if chunks:
            tts = gTTS(text=chunks[0], lang='en', slow=False)
            tts.save(filename)
    
    def _convert_offline(self, text, filename):
        """Convert text to speech using pyttsx3 (offline)"""
        # pyttsx3 doesn't support mp3 directly, so we'll save as .wav initially
        wav_file = filename.replace('.mp3', '.wav')
        
        # Save to file
        self.offline_engine.save_to_file(text, wav_file)
        self.offline_engine.runAndWait()
        
        # In a real application, you might want to convert .wav to .mp3 here
        # For simplicity, we'll just rename the file
        if os.path.exists(wav_file):
            os.rename(wav_file, filename)
    
    def convert_async(self, text, callback=None):
        """Convert text to speech asynchronously"""
        thread = threading.Thread(target=self._async_convert, args=(text, callback))
        thread.daemon = True
        thread.start()
        return True
    
    def _async_convert(self, text, callback):
        """Internal method for asynchronous conversion"""
        filename = self.convert(text)
        if callback:
            callback(filename) 