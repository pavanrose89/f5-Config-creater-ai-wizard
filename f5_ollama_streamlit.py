# f5_ollama_streamlit.py
import streamlit as st

# Try importing Ollama
try:
    import ollama
    ollama_available = True
except ImportError:
    ollama_available = False

# --- ChatResponse class ---
class ChatResponse:
    def __init__(self, text, model):
        self.text = text
        self.model = model

    def has_error(self):
        return "error" in self.text.lower()


# --- F5 AI App class ---
class F5App:
    def __init__(self, use_ollama=True):
        self.use_ollama = use_ollama
        self.model = "llama3:latest"  # Default Ollama model

    def run(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return ChatResponse("Input cannot be empty.", self.model)

        # Ollama AI mode
        if self.use_ollama:
            if not ollama_available:
                return ChatResponse("Ollama SDK not installed or running.", self.model)
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": user_input}]
                )

                # --- Extract clean assistant text ---
                if hasattr(response, "text"):
                    ai_text = response.text
                elif hasattr(response, "content"):
                    ai_text = response.content
                elif hasattr(response, "message") and hasattr(response.message, "content"):
                    ai_text = response.message.content
                elif hasattr(response, "messages") and len(response.messages) > 0:
                    ai_text = response.messages[0].content
                elif hasattr(response, "output") and len(response.output) > 0:
                    ai_text = response.output[0].content
                else:
                    ai_text = str(response)

                return ChatResponse(ai_text, self.model)

            except Exception as e:
                return ChatResponse(f"Error: {str(e)}", self.model)

        # --- Fallback basic mapping ---
        basic_mapping = {
            "VIP check": "tmsh show ltm virtual",
            "Pool check": "tmsh show ltm pool members",
            "Health monitor": "tmsh show ltm monitor"
        }

        for key, cmd in basic_mapping.items():
            if key.lower() in user_input.lower():
                return ChatResponse(f"Suggested Command: {cmd}", "Basic Analysis")

        return ChatResponse("No suggestion available.", "Basic Analysis")


# --- Streamlit UI ---
st.set_page_config(page_title="F5 Config Assistant", layout="wide")
st.title("⚡ F5 Configuration Assistant via Ollama AI")

st.markdown("""
This tool helps F5 engineers generate **root cause analysis and configuration commands** using AI.

- Enter your F5 query below.
- Ollama AI will provide suggested commands or troubleshooting steps.
""")

# Input area
user_query = st.text_area("Enter your F5 Query:", height=100)

# Run button
if st.button("Generate F5 Commands / Analysis"):
    f5_app = F5App(use_ollama=True)
    result = f5_app.run(user_query)

    if result.has_error():
        st.error(result.text)
    else:
        st.success(f"Model Used: {result.model}")
        st.code(result.text, language="bash")
