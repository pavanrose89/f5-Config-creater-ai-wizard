# f5_ollama_streamlit_v5.py
import streamlit as st
import re

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
        if not ollama_available:
            return ChatResponse("Ollama SDK not installed or running.", self.model)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": user_input}]
            )

            # Extract text safely
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

    # --- Generate CLI script from template inputs ---
    def generate_cli_from_template(
        self,
        vip_name, vip_ip, vip_port,
        pool_name, pool_members,
        snat=None, ssl_cert=None,
        profiles_http=None, profiles_tcp=None
    ):
        # --- Auto-select monitor ---
        if vip_port == 443:
            monitor_type = "https"
        elif vip_port == 80:
            monitor_type = "http"
        else:
            monitor_type = "tcp"

        members_str = " ".join(pool_members)
        profiles_http_str = " ".join(profiles_http) if profiles_http else "http"
        profiles_tcp_str = " ".join(profiles_tcp) if profiles_tcp else "tcp"

        prompt = f"""
You are an expert F5 L3 AI engineer. Generate a step-by-step CLI script with comments.

VIP: {vip_name} IP: {vip_ip} Port: {vip_port} Monitor: {monitor_type}
Pool: {pool_name} Members: {members_str}
SNAT: {snat if snat else 'none'}
SSL Certificate: {ssl_cert if ssl_cert else 'none'}
HTTP Profiles: {profiles_http_str}
TCP Profiles: {profiles_tcp_str}

Provide full TMSH CLI commands with comments for creating these objects and linking them properly.
"""
        return self.run_ollama(prompt)


# --- Streamlit UI ---
st.set_page_config(page_title="F5 AI L3 Assistant v5", layout="wide")
st.title("⚡ F5 AI L3 CLI Generator with Object Templates")

st.markdown("""
Use this tool to generate **ready-to-use F5 CLI scripts** interactively:
- Fill VIP, Pool, SSL, SNAT, Monitors, Profiles.
- AI generates **step-by-step CLI commands**.
- Monitor type is **auto-selected based on VIP port**.
""")

# --- Template Input Fields ---
with st.form("f5_template_form"):
    st.subheader("VIP Configuration")
    vip_name = st.text_input("VIP Name:", "MyVIP")
    vip_ip = st.text_input("VIP IP Address:", "10.0.0.50")
    vip_port = st.number_input("VIP Port:", min_value=1, max_value=65535, value=443)

    st.subheader("Pool Configuration")
    pool_name = st.text_input("Pool Name:", "WebPool")
    pool_members = st.text_area("Pool Members (IP space-separated):", "10.0.0.101 10.0.0.102").split()

    st.subheader("Additional Options")
    snat = st.text_input("SNAT (optional):", "")
    ssl_cert = st.text_input("SSL Certificate (optional):", "")
    profiles_http = st.text_area("HTTP Profiles (space-separated, optional):", "http").split()
    profiles_tcp = st.text_area("TCP Profiles (space-separated, optional):", "tcp").split()

    submit_button = st.form_submit_button("💻 Generate CLI Script")

if submit_button:
    if not vip_name or not vip_ip or not pool_name or not pool_members:
        st.warning("Please fill VIP and Pool details.")
    else:
        f5_app = F5App(use_ollama=True)
        result = f5_app.generate_cli_from_template(
            vip_name=vip_name,
            vip_ip=vip_ip,
            vip_port=vip_port,
            pool_name=pool_name,
            pool_members=pool_members,
            snat=snat if snat else None,
            ssl_cert=ssl_cert if ssl_cert else None,
            profiles_http=profiles_http,
            profiles_tcp=profiles_tcp
        )

        if result.has_error():
            st.error(result.text)
        else:
            st.success(f"Model Used: {result.model}")
            st.code(result.text, language="bash")

st.markdown("""
### Example usage:
- VIP 10.0.0.50, Pool WebPool, Members 10.0.0.101 10.0.0.102, SSL 'mycert', port 443 → AI will use HTTPS monitor.
- VIP 10.0.0.60, Pool AppPool, Members 10.0.0.110 10.0.0.111, port 8080 → AI will use TCP monitor.
""")
