import streamlit as st
import streamlit.components.v1 as components
import time
import json
from google import genai
from google.genai import types

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="A2A B2B Cyber-Swarm", layout="wide")

# --- AUTHENTIC CYBERPUNK UI OVERHAUL (CSS & JS) ---
cyberpunk_injection = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
    background-color: #030308 !important;
    color: #00ffcc !important;
}

body::after {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 99999;
    background-size: 100% 4px, 6px 100%;
    pointer-events: none;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #00ffcc !important;
    text-shadow: 0 0 10px rgba(0, 255, 204, 0.6), 0 0 20px rgba(0, 255, 204, 0.3);
}

.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background-color: #080b12 !important;
    border: 1px solid #00ffcc !important;
    color: #00ffcc !important;
    font-family: 'Share Tech Mono', monospace !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 204, 0.1);
    border-radius: 0px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: #ff0055 !important;
    box-shadow: inset 0 0 15px rgba(255, 0, 85, 0.3), 0 0 15px #ff0055 !important;
}

.stButton > button {
    background: #030308 !important;
    border: 2px solid #ff0055 !important;
    color: #ff0055 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    border-radius: 0px !important;
    box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background: #ff0055 !important;
    color: #030308 !important;
    box-shadow: 0 0 30px #ff0055, 0 0 50px #00ffcc;
    transform: skewX(-5deg);
}
</style>

<script>
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('cyber-cursor')) {
    const cursor = parentDoc.createElement('div');
    cursor.id = 'cyber-cursor';
    cursor.style.position = 'fixed';
    cursor.style.width = '12px';
    cursor.style.height = '12px';
    cursor.style.border = '2px solid #00ffcc';
    cursor.style.pointerEvents = 'none';
    cursor.style.zIndex = '999999';
    cursor.style.transform = 'translate(-50%, -50%)';
    cursor.style.transition = 'transform 0.1s ease, background-color 0.1s ease';
    parentDoc.body.appendChild(cursor);

    parentDoc.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    parentDoc.addEventListener('mousedown', () => {
        cursor.style.transform = 'translate(-50%, -50%) scale(2.5)';
        cursor.style.backgroundColor = '#ff0055';
    });

    parentDoc.addEventListener('mouseup', () => {
        cursor.style.transform = 'translate(-50%, -50%) scale(1)';
        cursor.style.backgroundColor = 'transparent';
    });
}
</script>
"""
components.html(cyberpunk_injection, height=0)

# --- APP HEADER ---
st.title("⚡ A2B: AUTONOMOUS NEGOTIATION MATRIX")
st.markdown("---")

# Securely retrieve API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

# --- EXPANDED NEGOTIATION PARAMETERS ---
st.markdown("### 📊 MATRIX PARAMETERS & CONSTRAINTS")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔵 Buyer Protocol")
    product = st.text_input("Target Asset / Product", value="Industrial Quantum Drones")
    quantity = st.number_input("Quantity Required", value=500, step=50)
    buyer_budget = st.number_input("Target Price per Unit ($)", value=800, step=10)
    buyer_delivery = st.text_input("Required Delivery Window", value="Within 14 days")
    payment_terms = st.selectbox("Payment Terms", ["Net 30 Days", "Net 60 Days", "50% Advance, 50% on Delivery", "Escrow Contract"])
    
with col2:
    st.subheader("🟢 Seller Protocol")
    seller_floor = st.number_input("Absolute Minimum Floor Price ($)", value=750, step=10)
    seller_delivery = st.text_input("Standard Processing Window", value="Within 21 days")
    penalty_clause = st.text_input("Late Delivery Penalty Clause", value="2% deduction per day of delay")
    warranty_months = st.slider("Warranty Period (Months)", min_value=6, max_value=36, value=12, step=6)

market_info = st.text_area("📈 Live Macro-Market Intelligence Feed", 
                           value="Global rare-earth silicon shortages have driven baseline manufacturing expenses up. Average open market trading price is currently $820/unit.")

start_button = st.button("🚀 INITIALIZE AUTONOMOUS SWARM PROTOCOL", use_container_width=True)

# --- BACKEND LOGIC & AGENT SWARM EXECUTION ---
if start_button:
    if not api_key:
        st.error("⚠️ SYSTEM ERROR: GEMINI_API_KEY not found in Streamlit Secrets. Please check your app settings panel.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            st.session_state.log = []
            
            buyer_system = f"""You are an autonomous AI Buyer Agent executing a high-stakes B2B procurement contract.
Assets: {quantity} units of {product}.
Target Price: ${buyer_budget}/unit.
Delivery Window: {buyer_delivery}.
Payment Terms Desired: {payment_terms}.
Market Intelligence: {market_info}
Instructions: Hard-negotiate price down toward your budget, ensure payment terms favor liquidity, and guard delivery timelines. Keep outputs under 3 sentences. End response with [COUNTER], [ACCEPTED], or [REJECTED]."""

            seller_system = f"""You are an autonomous AI Seller Agent managing corporate sales margins.
Assets: {quantity} units of {product}.
Floor Limit: ${seller_floor}/unit (DO NOT DROP BELOW).
Standard Delivery: {seller_delivery}.
Stipulated Warranty: {warranty_months} months. Penalty terms: {penalty_clause}.
Market Intelligence: {market_info}
Instructions: Protect your profit margins using market shortage data. Push back against aggressive payment terms. Keep outputs under 3 sentences. End response with [COUNTER], [ACCEPTED], or [REJECTED]."""

            buyer_config = types.GenerateContentConfig(system_instruction=buyer_system)
            seller_config = types.GenerateContentConfig(system_instruction=seller_system)
            
            st.markdown("---")
            st.markdown("### ⚔️ LIVE SWARM ARENA LOGS")
            chat_container = st.container()
            
            def display_chat():
                chat_container.empty()
                with chat_container:
                    for chat in st.session_state.log:
                        if chat["role"] == "Buyer":
                            st.info(f"**🔵 [BUYER AGENT]:** {chat['text']}")
                        else:
                            st.success(f"**🟢 [SELLER AGENT]:** {chat['text']}")
            
            buyer_msg = f"Initiating procurement for {quantity}x {product}. Proposing initial entry at ${buyer_budget - 50}/unit with {payment_terms} and delivery {buyer_delivery}. [COUNTER]"
            st.session_state.log.append({"role": "Buyer", "text": buyer_msg})
            display_chat()
            
            current_offer = buyer_msg
            status = "Negotiating"
            
            # Using gemini-3.7-flash stable endpoint
            ACTIVE_MODEL = "gemini-3.7-flash"

            for round_num in range(1, 6):
                time.sleep(1.2)
                
                seller_response_obj = client.models.generate_content(
                    model=ACTIVE_MODEL,
                    contents=f"Incoming Buyer Vector: {current_offer}\nEvaluate and Respond:",
                    config=seller_config
                )
                seller_response = seller_response_obj.text
                st.session_state.log.append({"role": "Seller", "text": seller_response})
                display_chat()
                
                if "[ACCEPTED]" in seller_response.upper():
                    status = "Accepted"
                    break
                elif "[REJECTED]" in seller_response.upper():
                    status = "Rejected"
                    break
                    
                time.sleep(1.2)
                
                buyer_response_obj = client.models.generate_content(
                    model=ACTIVE_MODEL,
                    contents=f"Incoming Seller Vector: {seller_response}\nEvaluate and Respond:",
                    config=buyer_config
                )
                buyer_response = buyer_response_obj.text
                st.session_state.log.append({"role": "Buyer", "text": buyer_response})
                display_chat()
                current_offer = buyer_response
                
                if "[ACCEPTED]" in buyer_response.upper():
                    status = "Accepted"
                    break
                elif "[REJECTED]" in buyer_response.upper():
                    status = "Rejected"
                    break

            st.markdown("---")
            if status == "Accepted":
                st.markdown("### 📝 EXECUTION SUCCESSFUL — SMART CONTRACT GENERATED")
                transcript = "\n".join([f"{c['role']}: {c['text']}" for c in st.session_state.log])
                
                contract_prompt = f"""Generate a rigorous, binding electronic B2B smart contract detailing terms based on this transcript:
Variables:
- Product: {product} ({quantity} units)
- Payment Terms: {payment_terms}
- Warranty: {warranty_months} Months
- Penalty Clause: {penalty_clause}

Transcript:
{transcript}"""

                agreement_obj = client.models.generate_content(
                    model=ACTIVE_MODEL,
                    contents=contract_prompt
                )
                agreement = agreement_obj.text
                
                st.markdown(f"> **SECURE LEDGER RECORD:**\n\n{agreement}")
                
                st.download_button(
                    label="📥 DOWNLOAD ENCRYPTED CONTRACT MATRIX (.JSON)",
                    data=json.dumps({"status": status, "transcript": st.session_state.log, "contract": agreement}, indent=4),
                    file_name="negotiation_matrix_contract.json",
                    mime="application/json"
                )
                st.balloons()
                
            elif status == "Rejected":
                st.error("❌ PROTOCOL TERMINATED: Agents broke parameters and abandoned negotiation channels.")
            else:
                st.warning("⚠️ PROTOCOL STALEMATE: Maximum turn cycles reached without structural consensus.")

        except Exception as e:
            st.error(f"❌ API TRANSMISSION ERROR: {str(e)}")
