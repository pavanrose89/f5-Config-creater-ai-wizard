# f5_ollama_streamlit_wizard_fixed.py
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

    def generate_cli_from_wizard(
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
st.set_page_config(page_title="F5 AI L3 Wizard", layout="wide")
st.title("⚡ F5 AI L3 CLI Wizard Assistant")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "wizard_data" not in st.session_state:
    st.session_state.wizard_data = {}

f5_app = F5App(use_ollama=True)

# --- Step 1: VIP ---
if st.session_state.step == 1:
    st.subheader("Step 1: VIP Configuration")
    vip_name = st.text_input("VIP Name:", st.session_state.wizard_data.get("vip_name", "MyVIP"))
    vip_ip = st.text_input("VIP IP Address:", st.session_state.wizard_data.get("vip_ip", "10.0.0.50"))
    vip_port = st.number_input("VIP Port:", min_value=1, max_value=65535, value=st.session_state.wizard_data.get("vip_port", 443))

    if st.button("Next: Pool Configuration"):
        st.session_state.wizard_data.update({
            "vip_name": vip_name,
            "vip_ip": vip_ip,
            "vip_port": vip_port
        })
        st.session_state.step = 2
        st.stop()  # <- replaced experimental_rerun

# --- Step 2: Pool ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Pool Configuration")
    pool_name = st.text_input("Pool Name:", st.session_state.wizard_data.get("pool_name", "WebPool"))
    pool_members = st.text_area(
        "Pool Members (space-separated IPs):",
        " ".join(st.session_state.wizard_data.get("pool_members", ["10.0.0.101", "10.0.0.102"]))
    ).split()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back: VIP Configuration"):
            st.session_state.step = 1
            st.stop()
    with col2:
        if st.button("Next: SSL & SNAT"):
            st.session_state.wizard_data.update({
                "pool_name": pool_name,
                "pool_members": pool_members
            })
            st.session_state.step = 3
            st.stop()

# --- Step 3: SSL & SNAT ---
elif st.session_state.step == 3:
    st.subheader("Step 3: SSL & SNAT Configuration")
    ssl_cert = st.text_input("SSL Certificate (optional):", st.session_state.wizard_data.get("ssl_cert", ""))
    snat = st.text_input("SNAT (optional):", st.session_state.wizard_data.get("snat", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back: Pool Configuration"):
            st.session_state.step = 2
            st.stop()
    with col2:
        if st.button("Next: Profiles & Monitor"):
            st.session_state.wizard_data.update({
                "ssl_cert": ssl_cert,
                "snat": snat
            })
            st.session_state.step = 4
            st.stop()

# --- Step 4: Profiles & Monitor ---
elif st.session_state.step == 4:
    st.subheader("Step 4: Profiles & Monitor")
    profiles_http = st.text_area(
        "HTTP Profiles (space-separated, optional):",
        " ".join(st.session_state.wizard_data.get("profiles_http", ["http"]))
    ).split()
    profiles_tcp = st.text_area(
        "TCP Profiles (space-separated, optional):",
        " ".join(st.session_state.wizard_data.get("profiles_tcp", ["tcp"]))
    ).split()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back: SSL & SNAT"):
            st.session_state.step = 3
            st.stop()
    with col2:
        if st.button("Next: Generate CLI"):
            st.session_state.wizard_data.update({
                "profiles_http": profiles_http,
                "profiles_tcp": profiles_tcp
            })
            st.session_state.step = 5
            st.stop()

# --- Step 5: Generate CLI ---
elif st.session_state.step == 5:
    st.subheader("Step 5: Generate CLI Script")
    data = st.session_state.wizard_data

    result = f5_app.generate_cli_from_wizard(
        vip_name=data["vip_name"],
        vip_ip=data["vip_ip"],
        vip_port=data["vip_port"],
        pool_name=data["pool_name"],
        pool_members=data["pool_members"],
        snat=data.get("snat"),
        ssl_cert=data.get("ssl_cert"),
        profiles_http=data.get("profiles_http"),
        profiles_tcp=data.get("profiles_tcp")
    )

    if result.has_error():
        st.error(result.text)
    else:
        st.success(f"Model Used: {result.model}")
        st.code(result.text, language="bash")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back: Profiles & Monitor"):
            st.session_state.step = 4
            st.stop()
    with col2:
        if st.button("Start Over"):
            st.session_state.step = 1
            st.session_state.wizard_data = {}
            st.stop()

st.markdown("""
### Wizard Instructions:
1. Fill VIP info → Next  
2. Fill Pool info → Next  
3. SSL & SNAT → Next  
4. Profiles → Next  
5. Generate ready-to-use CLI script
""")
