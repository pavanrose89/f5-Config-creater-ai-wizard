# f5_ollama_streamlit_v3.py
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

            # --- Extract clean text ---
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

    # --- Troubleshoot Issue ---
    def troubleshoot(self, issue_description):
        prompt = f"""
You are an expert F5 L3 AI engineer. Analyze the following F5 issue and provide:
- Root cause
- Checks
- Recommended tmsh commands
Issue: {issue_description}
"""
        return self.run_ollama(prompt)

    # --- Generate full CLI Script ---
    def generate_cli_script(self, issue_description, details=""):
        prompt = f"""
You are an expert F5 L3 AI engineer. Based on the issue description and details below,
generate a full step-by-step F5 CLI script.
Include commands for:
- Virtual Server (VIP)
- Pool & Pool Members
- SNAT
- SSL Certificate
- HTTP & HTTPS Monitors
- TCP & HTTP Profiles
- Any related configuration required
Include comments and order commands properly.

Issue Description: {issue_description}
Additional Details: {details}
"""
        return self.run_ollama(prompt)


# --- Streamlit UI ---
st.set_page_config(page_title="F5 AI L3 Assistant", layout="wide")
st.title("⚡ F5 AI L3 Configuration & CLI Generator")

st.markdown("""
This AI assistant helps F5 engineers to:
1. **Troubleshoot issues** – Get root cause, checks, and recommended commands.
2. **Generate full CLI scripts** – Create VIPs, Pools, Monitors, SNATs, SSLs, Profiles, and more.

💡 Enter the F5 issue or desired object configuration and use the buttons below.
""")

# Input boxes
issue_input = st.text_area("F5 Issue / Task Description:", height=120)
additional_details = st.text_area("Additional Details (e.g., VIP IP, Pool members, SSL info):", height=100)

# Initialize F5 AI app
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
    if st.button("💻 Generate Full F5 CLI Script"):
        if not issue_input.strip():
            st.warning("Please enter the F5 issue description or task.")
        else:
            st.info("Generating CLI script with AI...")
            result = f5_app.generate_cli_script(issue_input, additional_details)
            if result.has_error():
                st.error(result.text)
            else:
                st.success(f"Model Used: {result.model}")
                st.code(result.text, language="bash")

# Optional: pre-fill examples
st.markdown("""
### Examples you can try:
- Troubleshoot: `"VIP not responding, pool members down"`
- CLI Script: `"Create VIP 10.0.0.50, Pool WebPool, Members 10.0.0.101, 10.0.0.102, attach SSL certificate 'mycert'"`
""")
