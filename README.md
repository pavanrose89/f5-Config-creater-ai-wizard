# ⚡ F5 AI L3 Wizard – Python, Streamlit & Ollama AI

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI](https://img.shields.io/badge/AI-Enabled-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Made With Love](https://img.shields.io/badge/Made%20with-❤️-red)

This repository is a **hands-on lab for F5 BIG-IP LTM engineers and students**. It contains **six evolving versions of an interactive F5 L3 Wizard** built using **Python, Streamlit, and Ollama AI**. The wizard helps automate the creation of **VIPs, Pools, SSL profiles, SNATs, Monitors, and Profiles**, while generating **step-by-step F5 BIG-IP TMSH CLI scripts**.

---

## 🧰 Features Across Versions

1. **Basic VIP & Pool input** – foundational CLI generation.  
2. **Auto monitor selection** – automatically chooses HTTP, HTTPS, or TCP monitor based on VIP port.  
3. **SSL and SNAT support** – add security and NAT configurations to VIPs.  
4. **Multi-step wizard with session persistence** – smooth navigation and input tracking.  
5. **AI-generated CLI scripts** – uses **Ollama AI** to generate smart automation commands.  
6. **Final fixed version** – robust AI extraction and safe CLI outputs.

**Monitor auto-selection:**  

- Port 443 → HTTPS Monitor  
- Port 80 → HTTP Monitor  
- Other → TCP Monitor  

**Purpose:**  
- Learn **F5 network automation**.  
- Understand **step-by-step evolution of automation scripts**.  
- Practice integrating **AI with network operations**.  
- Generate copy-paste ready CLI for BIG-IP configurations.

---

## 📌 Prerequisites

- **Python 3.10+**
- [Streamlit](https://streamlit.io/)
- [Ollama AI](https://ollama.com/)
- Internet connection for Ollama AI

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/f5-ollama-ai-wizard.git
cd f5-ollama-ai-wizard

Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Install dependencies:
pip install -r requirements.txt

Install and configure Ollama AI:
python -c "import ollama; print('Ollama Installed')"

🚀 Running the Wizard

Each version adds new features. Run any with:

streamlit run f5_ollama_streamlit_wizard_fixed.py
streamlit run f5_ollama_streamlit.py
streamlit run f5_ollama_streamlit_v2.py
streamlit run f5_ollama_streamlit_v3.py
streamlit run f5_ollama_streamlit_v4.py
streamlit run f5_ollama_streamlit_v5.py

🧑‍🏫 How It Works
Wizard Interface: Streamlit forms and multi-step navigation.
AI Engine: Ollama AI generates step-by-step TMSH CLI commands.
Monitor Selection: Auto-selects HTTP, HTTPS, or TCP monitor based on VIP port.
Result: Copy-paste ready CLI scripts for VIPs, Pools, SSLs, SNATs, and Monitors.

Additional Notes:

SSL profiles and SNATs are optional.
Pool members are comma-separated.
All scripts include comments for teaching and learning purposes.
📚 References
Streamlit Documentation
Ollama AI Documentation
F5 BIG-IP TMSH Reference

⚖️ License

MIT License – see LICENSE file

🏷️ Topics

F5 BIG-IP, LTM, VIP, Pool, SNAT, SSL, CLI, Network Automation, Streamlit, Ollama AI, Python, DevOps, Networking Lab, Automation, TMSH
