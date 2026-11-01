import requests 
import config

def get_llm_response(messages: list[dict])->str:
    if config.LLM_PROVIDER == "openai":
        return ask_openai(messages)
       
    if config.LLM_PROVIDER == "gemini":
         return ask_gemini(messages)

    if config.LLM_PROVIDER == "ollama":
        return ask_ollama(messages)

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: {config.LLM_PROVIDER}, Please use one of :{', '.join(config.SUPPORTED_PROVIDER)}"
    )             

def ask_openai(messages:list[dict])->str:
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPEN_API_KEY is missing please add it to your .env")

    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    try :
        response = client.chat.completions.create(
            model = config.OPENAI_MODEL,
            messages = messages,
        )    
    except Exception as e :
        raise RuntimeError(F"OpenAI request failed: {e}")

    return response.choices[0].message.content
    
def ask_gemini(messages: list[dict])->str:
    if not config.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing . add it to your .env file.")

    from google import genai

    system_instruction = ""
    contents = []

    for message in messages :
        if message["role"] == "system":
            system_instruction = message["content"]
        else:
            gemini_role = "model" if message["role"] == "assistant" else "user"
            contents.append(
                {"role" : gemini_role, "parts": [{"text": message["content"]}]}
            )   

    generation_setting = None
    if system_instruction:
        generation_setting = {"system_instruction": system_instruction}

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    try:
        reponse=client.models.generate_content(
            model = config.GEMINI_MODEL,
            contents=contents,
            config=generation_setting,
        )    
    except Exception as error:
        raise RuntimeError(f"Gemini request failed : {error}")

    return response.text

def ask_ollama(messages: list[dict])-> str:
    url = f"{config.OLLAMA_BASE_URL}/api/chat"

    payload = {
        "model" : config.OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }    

    try:
        response = requests.post(url, json=payload , timeout = 120)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Could not reach Ollama at {config.OLLAMA_BASE_URL}"
        )
    except Exception as error:
        raise RuntimeError(f"Ollama request failed : {error}")

    return response.json()["message"]["content"]