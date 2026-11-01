import config
import llm_client
import memory

EXIT_COMMAND = ["exit","quit"]

def build_message(user_input: str)-> list[dict]:
    messages = [{"role":"system","content":conifg.SYSTEM_PROMPT}]
    message.extend(memory.get_history())
    messages.append({"role":"user","content":user_input})

    return messages

def main()-> None:
    print("chatbot WITH memory")
    print(F"Provider:{config.LLM_provider}")
    print("type 'exit' or 'quit' t stop. \n ")

    configuration_error = config.get_configuration_error()
    if configuration_error :
        print(f"Configuartion problem: {configuration_error}")
        return

    while True:
        try:
            user_input = input("YOU: ").strip()
        except (EOFError,KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not user_input :
            print("please type a question.\n")
            continue

        if user_input.lower() in EXIT_COMMAND:
            print("Goodbye!")
            return

        try:
            reply = llm_client.get_llm_response(build_message(user_input))
        except Exception as error:
            print(f"Sorry, something went wrong:{error}\n")
            continue

        memory.add_user_message(user_input)
        memory.add_asistant_message(reply)

        print(f"Assistant: {reply}\n")

if __name__== "__main__":
    main()
