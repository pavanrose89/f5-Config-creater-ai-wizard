# f5_ollama_streamlit_v2.py
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
        self.model = "llama3:latest"

    def run_ollama(self, user_input):
        """Send query to Ollama and return clean assistant text"""
        if not ollama_available:
            return ChatResponse("Ollama SDK not installed or running.", self.model)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": user_input}]
            )

            # Extract clean text for all versions
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

    def troubleshoot(self, issue_description):
        """Part 1: Troubleshoot F5 issue"""
        prompt = f"""
You are an F5 L3 AI engineer. Analyze the following issue and provide
root cause analysis, checks, and recommended commands:

Issue: {issue_description}
"""
        return self.run_ollama(prompt)

    def generate_cli_script(self, issue_description, details=""):
        """Part 2: Generate full CLI script based on issue and details"""
        prompt = f"""
You are an expert F5 L3 engineer. Based on the issue description and details below,
generate a full, step-by-step F5 CLI script that can be used to troubleshoot and fix the problem.
Provide commands in order, with comments if needed.

Issue Description: {issue_description}
Additional Details: {details}
"""
        return self.run_ollama(prompt)


# --- Streamlit UI ---
st.set_page_config(page_title="F5 AI Assistant", layout="wide")
st.title("⚡ F5 AI L3 Configuration Assistant")

st.markdown("""
This tool helps F5 engineers perform **two main tasks**:

1. **Troubleshoot F5 Issues** – Get root cause analysis, checks, and recommendations.
2. **Generate Full F5 CLI Script** – Produce a step-by-step CLI script for the issue.

💡 Enter the F5 issue description below and use the buttons to choose the action.
""")

# Input box
issue_input = st.text_area("Enter F5 Issue Description:", height=120)
additional_details = st.text_area("Provide additional details for CLI script (optional):", height=100)

# Initialize F5 App
f5_app = F5App(use_ollama=True)

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("⚙️ Troubleshoot Issue"):
        if not issue_input.strip():
            st.warning("Please enter the F5 issue description.")
        else:
            st.info("Analyzing issue with AI...")
            result = f5_app.troubleshoot(issue_input)
            if result.has_error():
                st.error(result.text)
            else:
                st.success(f"Model Used: {result.model}")
                st.code(result.text, language="bash")

with col2:
    if st.button("💻 Generate CLI Script"):
        if not issue_input.strip():
            st.warning("Please enter the F5 issue description.")
        else:
            st.info("Generating CLI script with AI...")
            result = f5_app.generate_cli_script(issue_input, additional_details)
            if result.has_error():
                st.error(result.text)
            else:
                st.success(f"Model Used: {result.model}")
                st.code(result.text, language="bash")
