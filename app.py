import streamlit as st
import config
import llm_client

def build_messages(history: list[dict], user_input: str) -> list[dict]:
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    return messages


st.set_page_config(page_title="Chatbot with Memory")
st.title("Chatbot with Memory")
st.write(
    "This chatbot sends the whole conversation to the LLM with every question, "
    "so it can remember what you said earlier. Tell it your name, then ask "
    "what your name is."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

configuration_error = config.get_configuration_error()

if configuration_error:
    st.error(f"Configuration problem: {configuration_error}")
    st.stop()

st.caption(f"Provider: {config.LLM_PROVIDER}")

if st.button("Clear conversation"):
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me anything...")

if user_input and user_input.strip():
    user_input = user_input.strip()

    with st.chat_message("user"):
        st.write(user_input)

    try:
        reply = llm_client.get_llm_response(
            build_messages(st.session_state.messages, user_input)
        )
    except Exception as error:
        st.error(f"Sorry, something went wrong: {error}")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)
