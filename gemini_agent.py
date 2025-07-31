import google.generativeai as genai
import os
from typing import List, Dict, Optional
import json
from datetime import datetime

class GeminiAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initialize Gemini AI Agent
        
        Args:
            api_key (str): Google Gemini API key
            model_name (str): Model name to use (default: gemini-pro)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.conversation_history: List[Dict] = []
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize chat session
        self.chat = self.model.start_chat(history=[])
        
        print(f"✅ Gemini Agent initialized with model: {model_name}")
    
    def add_system_prompt(self, system_prompt: str):
        """Add system prompt to guide the agent's behavior"""
        self.system_prompt = system_prompt
        # Send system prompt as first message
        try:
            response = self.chat.send_message(f"System: {system_prompt}")
            self.conversation_history.append({
                "role": "system",
                "content": system_prompt,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error setting system prompt: {e}")
    
    def send_message(self, message: str, include_history: bool = True) -> str:
        """
        Send message to Gemini and get response
        
        Args:
            message (str): User message
            include_history (bool): Whether to include conversation history
            
        Returns:
            str: Agent response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Send message to Gemini
            response = self.chat.send_message(message)
            response_text = response.text
            
            # Add agent response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error communicating with Gemini: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history and start fresh"""
        self.conversation_history = []
        self.chat = self.model.start_chat(history=[])
        print("🔄 Conversation history cleared")
    
    def save_conversation(self, filename: str):
        """Save conversation history to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    def load_conversation(self, filename: str):
        """Load conversation history from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            print(f"📂 Conversation loaded from {filename}")
        except Exception as e:
            print(f"Error loading conversation: {e}")
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        try:
            models = genai.list_models()
            current_model_info = None
            
            for model in models:
                if self.model_name in model.name:
                    current_model_info = {
                        "name": model.name,
                        "display_name": model.display_name,
                        "description": model.description,
                        "input_token_limit": getattr(model, 'input_token_limit', 'Unknown'),
                        "output_token_limit": getattr(model, 'output_token_limit', 'Unknown')
                    }
                    break
            
            return current_model_info or {"name": self.model_name, "status": "Model info not found"}
            
        except Exception as e:
            return {"error": f"Error getting model info: {e}"}

# Example usage
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        exit(1)
    
    # Initialize agent
    agent = GeminiAgent(api_key)
    
    # Set system prompt
    agent.add_system_prompt(
        "Anda adalah AI assistant yang helpful, harmless, dan honest. "
        "Jawab pertanyaan dengan informatif dan ramah dalam bahasa Indonesia."
    )
    
    # Interactive chat loop
    print("\n🤖 Gemini AI Agent siap! Ketik 'quit' untuk keluar.\n")
    
    while True:
        user_input = input("👤 Anda: ")
        
        if user_input.lower() in ['quit', 'exit', 'keluar']:
            print("👋 Terima kasih! Sampai jumpa!")
            break
        
        if user_input.lower() == 'clear':
            agent.clear_history()
            continue
        
        if user_input.lower() == 'save':
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            agent.save_conversation(filename)
            continue
        
        response = agent.send_message(user_input)
        print(f"🤖 Agent: {response}\n")