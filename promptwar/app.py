# --- IMPORT CHANGES ---
import streamlit as st
import streamlit.components.v1 as components
import time

# Replace the old generativeai import with the new genai SDK
from google import genai
from google.genai import types

# ... [KEEP YOUR FLASHY UI INJECTION AND FRONTEND CODE HERE] ...

# --- BACKEND LOGIC (THE AI SWARM) ---
if start_button:
    if not api_key_input:
        st.error("⚠️ Stop! Please paste your API key in the box at the top first.")
    else:
        # 1. Initialize the new SDK client
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

        # 2. Assign personas using the new GenerateContentConfig
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
            
            # 3. Use the new client.models.generate_content syntax
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
