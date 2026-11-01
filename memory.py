conversation_history : list[dict]=[]

def add_user_message(content : str)-> None:
    conversation_hiustory.appned({"role":"user","content":content})

def add_assistant_message(content:str)->None:
        conversation_history.append({"role":"assistant","content":content})

def get_history()-> list[dict]:
    return list(conversation_history)

def clear_memory()-> None:
    conversation_history.clear()