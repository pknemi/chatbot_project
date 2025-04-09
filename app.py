import streamlit as st
import google.generativeai as gen_ai

# Load API Key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Initialize session state for chat history (only keeps the latest message)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for Purple Background & Improved UI
st.markdown(
    """
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #6A11CB, #8E44AD); /* Purple Gradient */
            color: white;
        }
        
        
        
        .message {
            padding: 12px 15px;
            border-radius: 15px;
            max-width: 75%;
            word-wrap: break-word;
        }
        .user-message {
            align-self: flex-end;
            background: #007bff;
            color: white;
            text-align: right;
        }
        .bot-message {
            align-self: flex-start;
            background: #28a745;
            color: white;
            text-align: left;
        }
        .input-container {
            width: 100%;
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .stTextInput {
            flex-grow: 1;
            border-radius: 20px !important;
        }
        .stButton > button {
            border-radius: 20px;
            background: #007bff;
            color: white;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title (Now White for Visibility)
st.markdown("<h2 style='text-align: center; color: white;'>🤖 ChatterMind-A bot with Mind</h2>", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display only the latest chat message
chat_box = st.container()
with chat_box:
    st.markdown('<div class="chat-box" id="chatBox">', unsafe_allow_html=True)

    # Show only the latest user and bot message
    if len(st.session_state.chat_history) > 0:
        latest_chat = st.session_state.chat_history[-1]
        st.markdown(f'<div class="message user-message"><b>You:</b> {latest_chat["user"]}</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="message bot-message"><b>Gemini:</b> {latest_chat["bot"]}</div>',
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Chat input and send button (inside chat container)
with st.container():
    col1, col2 = st.columns([4, 1])

    # Reset input field on page refresh
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    with col1:
        user_input = st.text_input("Type a message...", value=st.session_state.user_input, key="input",
                                   label_visibility="collapsed")

    with col2:
        if st.button("Send", key="send_button") and user_input:
            try:
                model = gen_ai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(user_input)
                bot_response = response.text if response.text else "Sorry, I couldn't generate a response."

                # Keep only the latest message in session state
                st.session_state.chat_history = [{"user": user_input, "bot": bot_response}]

                # Clear input field after sending
                st.session_state.user_input = ""

                # Refresh UI
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)
