import streamlit as st
import google.generativeai as genai
import time

# --- SETUP YOUR AI ---
# VOIDPHOENIX: You need to get a free API key from Google AI Studio and paste it below.
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="A2A B2B Swarm", layout="wide")
st.title("⚡ Autonomous Negotiation Swarm")

if "log" not in st.session_state:
    st.session_state.log = []

# --- FRONTEND UI (CONTROL PANEL) ---
col1, col2 = st.columns(2)
with col1:
    buyer_budget = st.number_input("Buyer Max Budget ($)", value=50000)
with col2:
    seller_floor = st.number_input("Seller Min Price ($)", value=40000)

start_button = st.button("🚀 Start AI Negotiation")

# --- BACKEND LOGIC (THE AI SWARM) ---
if start_button:
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        st.error("⚠️ Stop! You need to put a real API key in the code first.")
    else:
        st.session_state.log = []
        
        # Initial Prompts to give the AI agents their identities
        buyer_prompt = f"You are a strict corporate Buyer. Your maximum budget is ${buyer_budget}. You want to buy 1000 units. Start by making an initial low offer. Keep responses under 2 sentences."
        seller_prompt = f"You are a stubborn Seller. Your absolute lowest acceptable price is ${seller_floor} for 1000 units. A buyer will make an offer. Counter it. Keep responses under 2 sentences."
        
        # Round 1: Buyer starts
        buyer_response = model.generate_content(buyer_prompt).text
        st.session_state.log.append({"role": "Buyer", "text": buyer_response})
        
        # Simulated Back-and-Forth Loop
        current_offer = buyer_response
        for round_num in range(3): # Limiting to 3 rounds so it doesn't run forever
            # Seller reacts to Buyer
            seller_reaction_prompt = seller_prompt + f"\n\nThe buyer just said: '{current_offer}'. Reply directly to them."
            seller_response = model.generate_content(seller_reaction_prompt).text
            st.session_state.log.append({"role": "Seller", "text": seller_response})
            
            # Buyer reacts to Seller
            buyer_reaction_prompt = buyer_prompt + f"\n\nThe seller just said: '{seller_response}'. Reply directly to them to negotiate."
            current_offer = model.generate_content(buyer_reaction_prompt).text
            st.session_state.log.append({"role": "Buyer", "text": current_offer})

# --- FRONTEND UI (DISPLAY ARENA) ---
st.markdown("### ⚔️ Live Arena")
for chat in st.session_state.log:
    if chat["role"] == "Buyer":
        st.info(f"**🔵 Buyer Agent:** {chat['text']}")
    else:
        st.success(f"**🟢 Seller Agent:** {chat['text']}")
    time.sleep(0.5) # Slight pause to make it readable
