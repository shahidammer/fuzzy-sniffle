# ============================================================================
# FILE 3: openai_client.py
# ============================================================================
"""
OpenAI API client wrapper class.
Handles all interactions with OpenAI services.
"""

from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import base64
from io import BytesIO
from PIL import Image
from constants import (
    OPENAI_MODEL, DALLE_MODEL, 
    TTS_MODEL, WHISPER_MODEL, TTS_VOICE
)

import os
from dotenv import load_dotenv
# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

class OpenAIClient:
    """Wrapper class for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the OpenAI client with API key."""
        self.client = OpenAI(api_key=openai_api_key)
    
    def chat_completion(self, messages, tools=None):
        """
        Create a chat completion with optional tool calling.
        
        Args:
            messages (list): List of conversation messages
            tools (list): Optional list of tools for function calling
        
        Returns:
            ChatCompletion: OpenAI response object
        """
        # TODO: Implement chat completion
        if tools:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        else:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
        return response
    
    def generate_image(self, prompt):
        """
        Generate an image using DALL-E.
        
        Args:
            prompt (str): Image generation prompt
        
        Returns:
            str: URL of generated image
        """
        # TODO: Implement DALL-E image generation
        response = self.client.images.generate(
            model=DALLE_MODEL,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    
    def text_to_speech(self, text):
        
        """
        Convert text to speech using OpenAI TTS.
        
        Args:
            text (str): Text to convert to audio
        
        Returns:
            bytes: Audio data
        """
        # TODO: Implement TTS
        response = self.client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text
        )
        audio_stream = BytesIO(response.content)
        audio = AudioSegment.from_file(audio_stream, format="mp3")
        play(audio)
        return response.content
    
    def speech_to_text(self, audio_file_path):
        """
        Convert speech to text using Whisper.
        
        Args:
            audio_file_path (str): Path to audio file
        
        Returns:
            str: Transcribed text
        """
        # TODO: Implement Whisper transcription
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file
            )
        return transcript.text
    
    def translate_text(self, text, target_language):
        """
        Translate text to target language.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code
        
        Returns:
            str: Translated text
        """
        # TODO: Implement translation
        messages = [
            {
                "role": "system",
                "content": f"Translate the following text to {target_language}. Return only the translation, no explanations."
            },
            {
                "role": "user",
                "content": text
            }
        ]
        response = self.chat_completion(messages)
        return response.choices[0].message.content
