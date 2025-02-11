# models/TextModel.py
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
load_dotenv()
class ChatModel:
    def __init__(self):
        self.model_name = os.getenv("MODEL_NAME")
        self.model = self.load_model()

    def load_model(self):
        # Specify the custom port when initializing
        model_name = os.getenv("MODEL_NAME")
        ollama_url = os.getenv("OLLAMA_URL")
        temperature = os.getenv("TEMPERATURE",0.5)
        max_tokens = os.getenv("MAX_TOKENS",4192)
        if model_name and ollama_url:
            return ChatOllama(
                model=model_name,
                base_url=ollama_url,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError("MODEL_NAME or OLLAMA_URL not set in .env file")

    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)