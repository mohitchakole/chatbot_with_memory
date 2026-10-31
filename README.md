# Chatbot With Memory (Beginner GenAI Project)

A very small GenAI project that shows **one idea**: the difference between a
chatbot that forgets everything and a chatbot that remembers the conversation.

No LangChain, no vector database, no frameworks. Just plain Python, a few API
calls, a Python list, and Streamlit.

---

## 1. Project objective

Build the same chatbot twice:

- once **without memory**, where every question is sent to the LLM on its own, and
- once **with memory**, where the whole conversation is sent with every question,

so you can see with your own eyes why the second one can remember your name
and the first one cannot.

## 2. What does "conversation memory" mean?

An LLM has no built-in memory. Every API request is completely independent:
the model only sees the text you send in that one request. It does not
remember the previous request at all.

So "giving a chatbot memory" simply means:

> keep the previous messages in a list, and send that list again with the next question.

That is all `memory.py` does. It is a Python list of dictionaries like this:

```python
[
    {"role": "user", "content": "My name is Rahul."},
    {"role": "assistant", "content": "Nice to meet you, Rahul!"},
]
```

**Important distinction:** storing messages on your computer is not the same
as the LLM receiving them. The model only knows what you actually put into the
request. In this project you can see exactly what is sent by looking at the
`build_messages()` function in `no_memory_chat.py` and in `chat.py`.

## 3. No memory vs. with memory

| | `no_memory_chat.py` | `chat.py` / `app.py` |
|---|---|---|
| What is sent to the LLM | system instruction + the current question only | system instruction + all previous messages + the current question |
| Can it remember your name? | No | Yes |
| Where is the history kept? | Nowhere | In a Python list (`memory.py`) or in `st.session_state` |
| Cost of a long chat | Stays the same | Grows, because more text is sent each time |

## 4. Project structure

```
chatbot-with-memory/
├── no_memory_chat.py   # CLI chatbot WITHOUT memory
├── chat.py             # CLI chatbot WITH memory
├── llm_client.py       # Talks to OpenAI / Gemini / Ollama and returns text
├── memory.py           # The conversation list plus add / get / clear functions
├── config.py           # Reads settings and API keys from the .env file
├── app.py              # Streamlit web UI for the chatbot with memory
├── requirements.txt    # Python packages needed
├── README.md           # This file
└── .env.example        # Template for your own .env file
```

## 5. Prerequisites

- Python 3.10 or newer (`python --version`)
- A terminal (Windows PowerShell is used in the examples below)
- **One** of the following:
  - an OpenAI API key, or
  - a Google Gemini API key, or
  - [Ollama](https://ollama.com) installed locally (free, no key needed)

## 6. Create and activate a virtual environment

A virtual environment keeps this project's packages separate from the rest of
your computer.

**Windows PowerShell**

```powershell
cd chatbot-with-memory
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**macOS / Linux**

```bash
cd chatbot-with-memory
python3 -m venv .venv
source .venv/bin/activate
```

## 7. Install the dependencies

```powershell
pip install -r requirements.txt
```

## 8. Configure your `.env` file

```powershell
Copy-Item .env.example .env
```

macOS / Linux: `cp .env.example .env`

Then open `.env` and fill in the values for the provider you want to use.

| Variable | Meaning | Default |
|---|---|---|
| `LLM_PROVIDER` | `openai`, `gemini` or `ollama` | `openai` |
| `OPENAI_API_KEY` | Your OpenAI key | *(none)* |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o-mini` |
| `GEMINI_API_KEY` | Your Google Gemini key | *(none)* |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.0-flash` |
| `OLLAMA_BASE_URL` | Where Ollama is running | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |
| `SYSTEM_PROMPT` | Instruction given to the assistant | a friendly-assistant message |

Switching providers means changing **one line** in `.env`. None of the chatbot
files need to be edited.

> **Keep your keys private.** Your `.env` file contains real credentials, so it
> must never be committed to Git or shared. This project does not ship a
> `.gitignore`; if you put the project under version control, add a line
> containing `.env` to your `.gitignore` before your first commit.

### 9. Using OpenAI

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4o-mini
```

Get a key at <https://platform.openai.com/api-keys>. OpenAI requests are paid,
although `gpt-4o-mini` is very cheap.

### 10. Using Google Gemini

```
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-real-key
GEMINI_MODEL=gemini-2.0-flash
```

Get a free key at <https://aistudio.google.com/app/apikey>.

### 11. Using Ollama (free, runs on your computer)

1. Download and install Ollama from <https://ollama.com/download>.
2. Download a model (about 2 GB):

   ```powershell
   ollama pull llama3.2
   ```

3. Make sure the Ollama server is running. The desktop app starts it
   automatically; otherwise run:

   ```powershell
   ollama serve
   ```

4. Set this in `.env`:

   ```
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

No API key is needed and nothing is charged, because the model runs locally.

## 12. Running the applications

```powershell
# Chatbot WITHOUT memory (terminal)
python no_memory_chat.py

# Chatbot WITH memory (terminal)
python chat.py

# Chatbot WITH memory (web page in your browser)
streamlit run app.py
```

Type `exit` or `quit` to leave the terminal chatbots.

## 13. The demonstration

Ask the **same two questions** to both programs.

**`python no_memory_chat.py`**

```
You: My name is Rahul, and I work as a Python developer.
Assistant: Nice to meet you, Rahul!

You: What is my name and profession?
Assistant: I don't have that information. Could you tell me your name
           and what you do?
```

**`python chat.py`**

```
You: My name is Rahul, and I work as a Python developer.
Assistant: Nice to meet you, Rahul!

You: What is my name and profession?
Assistant: You are Rahul, and you work as a Python developer.
```

Same model, same key, same question. The only difference is that `chat.py`
also sent the earlier two messages in the second request.

## 14. Common errors and how to fix them

| Message | What it means | Fix |
|---|---|---|
| `Configuration problem: OPENAI_API_KEY is missing.` | No key was found in `.env` | Copy `.env.example` to `.env` and paste your key |
| `LLM_PROVIDER is 'Openai'. Please use one of: ...` | Typo in the provider name | Use lowercase `openai`, `gemini` or `ollama` |
| `Could not reach Ollama at http://localhost:11434` | Ollama is not running | Start the Ollama app, or run `ollama serve` |
| `Ollama request failed: 404 ...` | The model was never downloaded | Run `ollama pull llama3.2` |
| `OpenAI request failed: ... 401` | The key is wrong or expired | Create a new key and update `.env` |
| `OpenAI request failed: ... 429` | Rate limit or no credit left | Wait a moment, or add billing credit |
| `ModuleNotFoundError: No module named 'openai'` | Packages are not installed | Activate the venv and run `pip install -r requirements.txt` |
| `.\.venv\Scripts\Activate.ps1 cannot be loaded` | PowerShell script policy | Run the `Set-ExecutionPolicy` command from section 6 |

## 15. Memory is temporary

The conversation is kept in an ordinary Python list (and in
`st.session_state` for the Streamlit app). Both live only inside the running
program's memory.

That means the chatbot forgets everything when you:

- close the terminal or press `Ctrl+C`,
- type `exit` or `quit`,
- press **Clear conversation** in the Streamlit app, or
- stop and restart `streamlit run app.py`.

Nothing is written to a file or a database. If you want memory that survives a
restart, you would have to save the list to a file or a database, which is a
topic for a later project.
