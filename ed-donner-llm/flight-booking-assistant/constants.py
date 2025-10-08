# ============================================================================
# FILE 1: constants.py
# ============================================================================
"""
Configuration and constant values for the application.
"""

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
DALLE_MODEL = "dall-e-3"
TTS_MODEL = "tts-1"
WHISPER_MODEL = "whisper-1"

# Voice Configuration
TTS_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer

# Language Configuration
SUPPORTED_LANGUAGES = {
    "German": "de",
    "Spanish": "es",
    "French": "fr",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese": "zh",
    "Portuguese": "pt"
}

# Mock Flight Database
MOCK_FLIGHT_DATA = {
    "paris": {
        "base_price": 450,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["brussels", "amsterdam", "lyon"]
    },
    "london": {
        "base_price": 380,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["manchester", "edinburgh", "dublin"]
    },
    "tokyo": {
        "base_price": 1200,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["osaka", "seoul", "taipei"]
    },
    "new york": {
        "base_price": 350,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["boston", "philadelphia", "washington dc"]
    },
    "barcelona": {
        "base_price": 420,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["madrid", "valencia", "marseille"]
    },
    "dubai": {
        "base_price": 650,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["abu dhabi", "doha", "muscat"]
    },
    "sydney": {
        "base_price": 1400,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["melbourne", "brisbane", "auckland"]
    },
    "rome": {
        "base_price": 480,
        "currency": "USD",
        "availability": True,
        "nearby_cities": ["milan", "florence", "venice"]
    }
}

# UI Configuration
UI_TITLE = "✈️ AI Flight Booking Assistant"
UI_DESCRIPTION = "Book flights with AI assistance, multilingual support, and visual previews"
CHATBOT_HEIGHT = 400

# System Prompt
SYSTEM_PROMPT = """You are a helpful flight booking assistant. 
Help users find flights, and provide information about destinations.
When users confirm a destination, An image will be generated.
Be friendly, concise, and informative."""

