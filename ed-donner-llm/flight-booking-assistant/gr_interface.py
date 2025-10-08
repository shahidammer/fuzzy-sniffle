# ============================================================================
# FILE 4: app.py (Main Application Class)
# ============================================================================
"""
Main application class that combines UI and business logic.
"""


import gradio as gr
from openai_client import OpenAIClient
from constants import (
    SUPPORTED_LANGUAGES, UI_TITLE, UI_DESCRIPTION, 
    CHATBOT_HEIGHT, SYSTEM_PROMPT
)
from tools import TOOLS, execute_tool
import json

class FlightBookingApp:
    """Main application class for the flight booking assistant."""
    
    def __init__(self):
        """Initialize the application with OpenAI client."""
        self.openai_client = OpenAIClient()
        self.interface = None
        self.system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    
    # ========================================================================
    # BUSINESS LOGIC METHODS
    # ========================================================================
    
    def process_message(self, user_message, conversation_history, 
                       target_language, selected_destination):
        """
        Process user message through the complete pipeline.
        
        Args:
            user_message (str): User's message
            conversation_history (list): Previous messages (list of [user, bot] pairs)
            target_language (str): Language for translation
            selected_destination (str): Current destination
        
        Returns:
            tuple: (english_chat, translated_chat, image, updated_history, destination, cleared_input)
        """
        if not user_message.strip():
            return (
                conversation_history,
                conversation_history,
                None,
                conversation_history,
                selected_destination,
                ""
            )
        
        # TODO: Implement message processing
        # Step 1: Build messages array for OpenAI
        messages = [self.system_message]
        for user_msg, bot_msg in conversation_history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": user_message})
        print(messages)
        print("-"*88)

        # Step 2: Call OpenAI with tools
        response = self.openai_client.chat_completion(messages, TOOLS)
        
        # Step 3: Handle tool calls if present
        if response.choices[0].message.tool_calls:
            messages, response = self.handle_tool_calls(messages, response)
        
        # Step 4: Get final response
        assistant_message = response.choices[0].message.content
        # Step 5: Update conversation history
        updated_history = conversation_history + [[user_message, assistant_message]]
        
        # Step 6: Translate if needed
        translated_history = self.translate_conversation(updated_history, target_language)
        # Step 7: Generate image if destination mentioned
        image_url = None
        if self.detect_destination_confirmation(assistant_message):
            destination = selected_destination
            image_url = self.generate_destination_image(destination)

        # # Step 8: Convert to speech (handled by Gradio Audio component)
        # audio_data = self.openai_client.text_to_speech(assistant_message)

        return (
            updated_history,
            translated_history,
            image_url,
            updated_history,
            selected_destination,
            ""  # Clear input box
        )
        
        pass
    
    def handle_tool_calls(self, messages, response):
        """
        Handle tool calls from OpenAI response.
        
        Args:
            messages (list): Current message history
            response: OpenAI response with tool calls
        
        Returns:
            tuple: (updated_messages, new_response)
        
        """
        # TODO: Implement tool call handling
        # Add assistant message with tool calls
        messages.append(response.choices[0].message)
        # Execute each tool call
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute tool and get result
            tool_result = execute_tool(function_name, function_args)
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": tool_result
            })
        
        # Get final response after tool execution
        final_response = self.openai_client.chat_completion(messages, TOOLS)
        return messages, final_response
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text.
        
        Args:
            audio_file_path (str): Path to audio file
        
        Returns:
            str: Transcribed text
        """
        if not audio_file_path:
            return ""
        
        # TODO: Use OpenAI client to transcribe
        return self.openai_client.speech_to_text(audio_file_path)
    
    def translate_conversation(self, conversation_history, target_language):
        """
        Translate entire conversation to target language.
        
        Args:
            conversation_history (list): Conversation to translate
            target_language (str): Target language name
        
        Returns:
            list: Translated conversation
        """
        if target_language == "English":
            return conversation_history
        
        # TODO: Translate each message
        language_code = SUPPORTED_LANGUAGES.get(target_language, "en")
        translated = []
        for user_msg, bot_msg in conversation_history:
            translated_user = self.openai_client.translate_text(user_msg, language_code)
            translated_bot = self.openai_client.translate_text(bot_msg, language_code)
            translated.append([translated_user, translated_bot])
        return translated
    
    def generate_destination_image(self, city_name):
        """
        Generate image for a destination.
        
        Args:
            city_name (str): Name of the city
        
        Returns:
            str: Image URL or path
        """
        # TODO: Generate image
        prompt = f"A beautiful scenic view of {city_name}, travel destination, photorealistic, vibrant, high quality"
        return self.openai_client.generate_image(prompt)
    
    def detect_destination_confirmation(self, message):
        """
        Detect if a destination has been confirmed in the message.
        Simple keyword detection.
        """
        keywords = ["confirmed", "booked", "selected", "chosen", "going to"]
        return any(keyword in message.lower() for keyword in keywords)
    
    def extract_destination(self, message):
        """
        Extract destination city from message.
        Simple implementation - can be improved with NLP.
        """
        # TODO: Implement better extraction logic
        # For now, return None - will be improved
        return None
    
    # ========================================================================
    # GRADIO UI EVENT HANDLERS
    # ========================================================================
    
    def handle_text_input(self, user_text, conversation_history, 
                         target_language, selected_dest):
        """
        Handle text input from user.
        
        Args:
            user_text (str): User's text input
            conversation_history (list): Conversation history
            target_language (str): Selected language
            selected_dest (str): Currently selected destination
        
        Returns:
            tuple: Updated UI components
        """
        
        return self.process_message(
            user_text, 
            conversation_history, 
            target_language, 
            selected_dest
        )
    
    def handle_voice_input(self, audio_file, conversation_history, 
                          target_language, selected_dest):
        """
        Handle voice input from user.
        
        Args:
            audio_file: Recorded audio file
            conversation_history (list): Conversation history
            target_language (str): Selected language
            selected_dest (str): Currently selected destination
        
        Returns:
            tuple: Updated UI components
        """
        if audio_file is None:
            return (
                conversation_history,
                conversation_history,
                None,
                conversation_history,
                selected_dest
            )
        
        # Transcribe audio to text
        transcribed_text = self.transcribe_audio(audio_file)
        
        if not transcribed_text:
            return (
                conversation_history,
                conversation_history,
                None,
                conversation_history,
                selected_dest
            )
        
        # Process the transcribed text
        return self.process_message(
            transcribed_text,
            conversation_history,
            target_language,
            selected_dest
        )
    
    def handle_language_change(self, conversation_history, target_language):
        """
        Handle language selection change.
        
        Args:
            conversation_history (list): Current conversation
            target_language (str): New target language
        
        Returns:
            list: Translated conversation history
        """
        return self.translate_conversation(conversation_history, target_language)
    
    # ========================================================================
    # GRADIO UI CREATION
    # ========================================================================
    
    def create_interface(self):
        """
        Create and configure the Gradio interface.
        
        Returns:
            gr.Blocks: Configured Gradio interface
        """
        with gr.Blocks(title=UI_TITLE, theme=gr.themes.Soft()) as interface:
            gr.Markdown(f"# {UI_TITLE}")
            gr.Markdown(UI_DESCRIPTION)
            
            # State management
            conversation_state = gr.State([])
            selected_destination = gr.State(None)
            
            with gr.Row():
                # Panel 1: English Conversation
                with gr.Column(scale=1):
                    gr.Markdown("### 🇬🇧 English Conversation")
                    english_chatbot = gr.Chatbot(
                        label="Chat",
                        height=CHATBOT_HEIGHT,
                        show_label=False
                    )
                    
                    with gr.Row():
                        text_input = gr.Textbox(
                            label="Type your message",
                            placeholder="e.g., I want to fly to Paris",
                            scale=4,
                            show_label=False
                        )
                        send_btn = gr.Button("Send", scale=1, variant="primary")
                    
                    audio_input = gr.Audio(
                        sources=["microphone"],
                        type="filepath",
                        label="🎤 Or speak your message"
                    )
                
                # Panel 2: Translated Conversation
                with gr.Column(scale=1):
                    gr.Markdown("### 🌍 Translated Conversation")
                    language_dropdown = gr.Dropdown(
                        choices=["English"] + list(SUPPORTED_LANGUAGES.keys()),
                        value="German",
                        label="Select Language"
                    )
                    translated_chatbot = gr.Chatbot(
                        label="Translated Chat",
                        height=CHATBOT_HEIGHT,
                        show_label=False
                    )
                
                # Panel 3: Destination Image
                with gr.Column(scale=1):
                    gr.Markdown("### 🖼️ Destination Preview")
                    destination_image = gr.Image(
                        label="Generated Image",
                        height=CHATBOT_HEIGHT,
                        show_label=False
                    )
            
            # Event handlers
            send_btn.click(
                fn=self.handle_text_input,
                inputs=[text_input, conversation_state, language_dropdown, selected_destination],
                outputs=[english_chatbot, translated_chatbot, destination_image, 
                        conversation_state, selected_destination, text_input]
            )
            
            text_input.submit(
                fn=self.handle_text_input,
                inputs=[text_input, conversation_state, language_dropdown, selected_destination],
                outputs=[english_chatbot, translated_chatbot, destination_image, 
                        conversation_state, selected_destination, text_input]
            )
            
            audio_input.change(
                fn=self.handle_voice_input,
                inputs=[audio_input, conversation_state, language_dropdown, selected_destination],
                outputs=[english_chatbot, translated_chatbot, destination_image, 
                        conversation_state, selected_destination]
            )
            
            language_dropdown.change(
                fn=self.handle_language_change,
                inputs=[conversation_state, language_dropdown],
                outputs=[translated_chatbot]
            )
            
            self.interface = interface
            return interface
    
    def launch(self, share=False):
        """Launch the Gradio interface."""
        if self.interface is None:
            self.create_interface()
        
        print("✅ Application ready!")
        print("🌐 Launching web interface...")
        self.interface.launch(share=share)

