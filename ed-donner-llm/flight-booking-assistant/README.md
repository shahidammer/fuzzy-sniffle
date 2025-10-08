# Technical Documentation: Flight Booking Assistant

## Overview
A multilingual flight booking application that combines price comparison, AI-generated destination imagery, audio interaction, and real-time translation using OpenAI services and Gradio UI.

## System Architecture

### Core Components
- **OpenAI Client**: Handles LLM interactions, image generation, and audio processing
- **Gradio Interface**: Provides multi-panel UI with audio recording capabilities
- **Tool Functions**: Custom functions for flight search and location recommendations

## Feature Specifications

### 1. Flight Price Search with Alternative Suggestions

**Primary Tool: `search_flight_prices`**
- Input: City name from user prompt
- Output: List of flight prices to specified destination
- Triggers automatically when user mentions a city

**Secondary Tool: `find_cheaper_nearby_locations`**
- Invoked when primary search returns results
- Calls OpenAI LLM to analyze nearby cities/airports
- Returns alternative destinations with lower prices
- Uses geographic proximity and price differential logic

### 2. Destination Image Generation

**Trigger**: User confirms destination selection

**Implementation**:
- Uses OpenAI DALL-E API (`client.images.generate()`)
- Generates contextual image of selected destination
- Parameters: destination name, travel context
- Displays generated image in dedicated UI panel

### 3. Audio Response System

**Text-to-Speech Flow**:
- User receives text response from LLM
- OpenAI TTS API (`client.audio.speech.create()`) converts response to audio
- Audio plays automatically in browser
- Supports voice selection and speed control

### 4. Gradio UI Layout

**Three-Panel Design**:

**Panel 1: Original Language (English)**
- Displays user input and assistant responses
- Primary conversation thread
- Default language: English

**Panel 2: Translated Conversation**
- Shows real-time translation of Panel 1
- User selects target language (German, Spanish, etc.)
- Uses OpenAI translation via LLM prompting
- Maintains conversation history in translated language

**Panel 3: Destination Imagery**
- Displays DALL-E generated images
- Updates when new destination selected
- Shows loading state during generation

### 5. Voice Input System

**Speech-to-Text Implementation**:
- Gradio Audio component captures user voice
- Records audio input from microphone
- OpenAI Whisper API (`client.audio.transcriptions.create()`) transcribes audio
- Transcribed text sent to LLM as standard prompt
- Supports multiple languages for input

## Technical Flow

```
User Input (Voice/Text) 
    → Whisper STT (if voice)
    → LLM Processing + Tool Calls
        → search_flight_prices()
        → find_cheaper_nearby_locations()
    → User Selects Destination
    → DALL-E Image Generation
    → Response Display (Text + Translation)
    → TTS Audio Playback
```

## API Requirements

### OpenAI Services
- **Chat Completions**: GPT-4 or GPT-3.5-turbo with function calling
- **DALL-E**: Image generation (dall-e-3 recommended)
- **Whisper**: Audio transcription
- **TTS**: Text-to-speech synthesis

### Authentication
- OpenAI API key required
- Set via environment variable or configuration file

## Gradio Components

### Interface Elements
- `gr.Textbox`: Text input/output
- `gr.Audio`: Voice recording input
- `gr.Image`: Display DALL-E generated images
- `gr.Dropdown`: Language selection
- `gr.Column`: Layout structure for three panels

### State Management
- Conversation history tracking
- Selected language persistence
- Current destination state

## Implementation Considerations

### Error Handling
- API rate limiting for OpenAI services
- Invalid city name validation
- Audio recording failures
- Translation fallback mechanisms

### Performance
- Asynchronous API calls where possible
- Caching for repeated location queries
- Image generation timeout handling

### Language Support
- English as base language
- Dynamic translation to user-selected language
- Language codes: 'de' (German), 'es' (Spanish), 'fr' (French), etc.

## Development Stack
- **Framework**: Python 3.8+
- **UI Library**: Gradio
- **AI Services**: OpenAI Python SDK
- **Audio Processing**: Native browser recording + Whisper API

## Future Enhancements
- Real-time flight API integration
- Booking confirmation workflow
- Multi-city itinerary support
- Price alert notifications
- Historical price tracking