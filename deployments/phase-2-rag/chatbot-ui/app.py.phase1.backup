"""
SME Knowledge Graph - Phase 1 Chatbot
Simple chat interface with Ollama local LLM
"""

import streamlit as st
import requests
import os
import json
from datetime import datetime

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:8b")

# Helper function
def check_ollama_connection():
    """Check if Ollama service is reachable"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

# Page configuration
st.set_page_config(
    page_title="SME Knowledge Chatbot",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        color: #1f77b4;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 SME Knowledge Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Local AI Assistant - 100% Private</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your local AI assistant running on your computer. I'm here to help you capture and organize your tribal knowledge. How can I assist you today?"
    })

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(f"""
    **Model**: {MODEL_NAME}
    **Status**: {'🟢 Connected' if check_ollama_connection() else '🔴 Disconnected'}

    ---

    ### Features
    - ✅ 100% Local & Private
    - ✅ Chat History
    - ✅ No Cloud Required

    ### Coming Soon
    - 🔜 RAG Search (Phase 2)
    - 🔜 Knowledge Graph (Phase 3)

    ---

    **Phase 1**: Simple Chatbot
    """)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(f"**Session Started**: {datetime.now().strftime('%H:%M:%S')}")

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Call Ollama API
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": st.session_state.messages,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                assistant_message = response.json()["message"]["content"]
                message_placeholder.markdown(assistant_message)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
            else:
                error_msg = f"Error: API returned status {response.status_code}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

        except requests.exceptions.ConnectionError:
            error_msg = "⚠️ Cannot connect to Ollama. Make sure Ollama service is running."
            message_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
        except requests.exceptions.Timeout:
            error_msg = "⚠️ Request timed out. The model might be processing a complex query."
            message_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
        except Exception as e:
            error_msg = f"⚠️ Unexpected error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
