import streamlit as st
import streamlit.components.v1 as components
import time

# Use the new genai SDK
from google import genai
from google.genai import types

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="A2A B2B Swarm", layout="wide")

# --- FLASHY UI INJECTION (CSS & JS) ---
flashy_injection = """
<style>
/* Neon Scrollbar */
::-webkit-scrollbar { width: 12px; }
::-webkit-scrollbar-track { background: #050510; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #00ffcc, #ff00cc); border-radius: 10px; }

/* Pulsing Headers */
h1, h2, h3 {
    text-shadow: 0 0 5px #00ffcc, 0 0 15px #00ffcc, 0 0 30px #00ffcc;
    animation: pulseText 2s infinite alternate;
}
@keyframes pulseText {
    0% { text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc; }
    100% { text-shadow: 0 0 10px #00ffcc, 0 0 25px #00ffcc, 0 0 40px #ff00cc; }
}

/* Animated Start Button */
.stButton > button {
    background: linear-gradient(45deg, #ff00cc, #00ffcc, #ff00cc);
    background-size: 200% 200%;
    animation: rgbShift 3s ease infinite;
    border: none !important;
    box-shadow: 0 0 20px #ff00cc;
    color: white !important;
    font-weight: bold;
    font-size: 18px !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 40px #00ffcc, 0 0 60px #00ffcc;
}
@keyframes rgbShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glowing Input Fields */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background-color: rgba(0, 20, 20, 0.7) !important;
    border: 1px solid #00ffcc !important;
    color: #fff !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 204, 0.2);
    transition: box-shadow 0.3s;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    box-shadow: inset 0 0 20px rgba(255, 0, 204, 0.5), 0 0 15px #ff00cc !important;
    border-color: #ff00cc !important;
}
</style>

<script>
// Inject Custom Cursor into Parent Window
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('flashy-cursor')) {
    const cursor = parentDoc.createElement('div');
    cursor.id = 'flashy-cursor';
    cursor.style.position = 'fixed';
    cursor.style.width = '20px';
    cursor.style.height = '20px';
    cursor.style.borderRadius = '50%';
    cursor.style.backgroundColor = 'rgba(0, 255, 204, 0.8)';
    cursor.style.boxShadow = '0 0 20px #00ffcc, 0 0 40px #00ffcc';
    cursor.style.pointerEvents = 'none';
    cursor.style.zIndex = '999999';
    cursor.style.transform = 'translate(-50%, -50%)';
    cursor.style.transition = 'width 0.15s, height 0.15s, background-color 0.15s';
    parentDoc.body.appendChild(cursor);

    parentDoc.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    parentDoc.addEventListener('mousedown', () => {
        cursor.style.width = '40px';
        cursor.style.height = '40px';
        cursor.style.backgroundColor = 'rgba(255, 0, 204, 0.9)';
        cursor.style.boxShadow = '0 0 30px #ff00cc, 0 0 60px #ff00cc';
    });

    parentDoc.addEventListener('mouseup', () => {
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.backgroundColor = 'rgba(0, 255, 204, 0.8)';
        cursor.style.boxShadow = '0 0 20px #00ffcc, 0 0 40px #00ffcc';
    });
}
</script>
"""
components.html(flashy_injection, height=0)

# --- APP CONTENT ---
st.title("⚡ Autonomous Negotiation Swarm")

api_key_input = st.text_input("🔑 Paste your Gemini API Key here to begin:", type="password")

st.markdown("### 📊 Negotiation Parameters")
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔵 Buyer Constraints")
    product = st.text_input("Product Name", value="Industrial Drones")
    quantity = st.number_input("Quantity Required", value=500, step=50)
    buyer_budget = st.number_input("Target Price per unit ($)", value=800, step=10)
    buyer_delivery = st.text_input("Required Delivery Time", value="Within 14 days")
    
with col2:
    st.subheader("🟢 Seller Constraints")
    seller_floor = st.number_input("Minimum Acceptable Price ($)", value=750, step=10)
    seller_delivery = st.text_input("Standard Delivery Time", value="Within 21 days")

market_info = st.text_area("📈 Market Information (Context for Agents)", 
                           value="Global supply chain shortages have increased drone manufacturing costs. Average market price is currently $820/unit.")

# This is the variable that was missing before!
start_button = st.button("🚀 Start Autonomous Negotiation", use_container_width=True)

# --- BACKEND LOGIC (THE AI SWARM) ---
if start_button:
    if not api_key_input:
        st.error("⚠️ Stop! Please paste your API key in the box at the top first.")
    else:
        # Initialize the new SDK client
        client = genai.Client(api_key=api_key_input)
        
        st.session_state.log = []
        
        # System Prompts
        buyer_system = f"""You are an autonomous AI Buyer Agent negotiating a B2B deal.
Product: {quantity} units of {product}.
Your Target Price: ${buyer_budget}/unit.
Required Delivery: {buyer_delivery}.
Market Info: {market_info}
Instructions: Negotiate price, quantity, and delivery. Handle offers and counteroffers intelligently. 
Keep responses under 3 sentences. You MUST end your response with exactly one of: [COUNTER], [ACCEPTED], or [REJECTED]."""

        seller_system = f"""You are an autonomous AI Seller Agent negotiating a B2B deal.
Product: {quantity} units of {product}.
Your Absolute Minimum Price: ${seller_floor}/unit. (Never go below this).
Standard Delivery: {seller_delivery}.
Market Info: {market_info}
Instructions: Negotiate price, quantity, and delivery. Justify pricing.
Keep responses under 3 sentences. You MUST end your response with exactly one of: [COUNTER], [ACCEPTED], or [REJECTED]."""

        # Assign personas using the new GenerateContentConfig
        buyer_config = types.GenerateContentConfig(system_instruction=buyer_system)
        seller_config = types.GenerateContentConfig(system_instruction=seller_system)
        
        st.markdown("---")
        st.markdown("### ⚔️ Live Arena")
        chat_container = st.container()
        
        def display_chat():
            chat_container.empty()
            with chat_container:
                for chat in st.session_state.log:
                    if chat["role"] == "Buyer":
                        st.info(f"**🔵 Buyer Agent:** {chat['text']}")
                    else:
                        st.success(f"**🟢 Seller Agent:** {chat['text']}")
        
        buyer_msg = f"Hello. We require {quantity} {product}. We propose an initial price of ${buyer_budget - 50}/unit with delivery {buyer_delivery}. [COUNTER]"
        st.session_state.log.append({"role": "Buyer", "text": buyer_msg})
        display_chat()
        
        current_offer = buyer_msg
        status = "Negotiating"
        
        # The Negotiation Loop
        for round_num in range(1, 5): 
            time.sleep(1.5) 
            
            # Use the new client.models.generate_content syntax
            seller_response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=f"Buyer just said: {current_offer}\nRespond:",
                config=seller_config
            ).text
            st.session_state.log.append({"role": "Seller", "text": seller_response})
            display_chat()
            
            if "[ACCEPTED]" in seller_response.upper():
                status = "Accepted"
                break
            elif "[REJECTED]" in seller_response.upper():
                status = "Rejected"
                break
                
            time.sleep(1.5)
            
            buyer_response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=f"Seller just said: {seller_response}\nRespond:",
                config=buyer_config
            ).text
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
            st.markdown("### 📝 Generating Final Agreement...")
            transcript = "\n".join([f"{c['role']}: {c['text']}" for c in st.session_state.log])
            
            agreement_prompt = f"Based on this B2B negotiation transcript, generate a formal, final contract.\n\nTranscript:\n{transcript}"
            agreement = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=agreement_prompt
            ).text
            st.markdown(f"> **FINAL CONTRACT:**\n\n{agreement}")
            st.balloons()
        elif status == "Rejected":
            st.error("❌ Negotiation Failed. Agents walked away.")
        else:
            st.warning("⚠️ Negotiation Stalemate. Timeout reached.")
