import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER","ollama").lower().strip()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY","")
OPENAI_MODEL=os.getenv("OPENAI_MODEL","gpt-40-mini")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY","")
GEMINI_MODEL= os.getenv("GEMINI_MODEL","gemini-2.0-flash")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL","http://localhost:11434")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","llama3.2")

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT","You are a freindly assistant")

SUPPORTED_PROVIDER = ["openai","gemini","ollama"]

def get_configuration_error()-> str|None:
    if LLM_PROVIDER not in SUPPORTED_PROVIDER:
        return(F"LLM_PROVIDER is '{LLM_PROVIDER}' which is not supported")
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        return "OPENAI_API_KEY is missing , add it to your .env"   
    if LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
        return "GEMINI_API_KEY is missing , add it to your .env"
    if LLM_PROVIDER == "ollama" and not OLLAMA_BASE_URL:
        return "OLLAMA_BASE_URL is missing, add it to your .env"

    return None           