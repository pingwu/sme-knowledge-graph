"""
SME Knowledge Graph - Phase 2 Chatbot with RAG
Chat interface with Ollama + ChromaDB for semantic search
"""

import streamlit as st
import requests
import os
from datetime import datetime
from pathlib import Path

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")
CHROMADB_URL = os.getenv("CHROMADB_URL", "http://chromadb:8000")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"
KNOWLEDGE_VAULT_PATH = os.getenv("KNOWLEDGE_VAULT_PATH", "/knowledge-vault")

# Note: ChromaDB client initialization will be added when chromadb package is installed
# For now, we'll use REST API directly

# Helper functions
def check_ollama_connection():
    """Check if Ollama service is reachable"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def check_chromadb_connection():
    """Check if ChromaDB service is reachable"""
    try:
        response = requests.get(f"{CHROMADB_URL}/api/v1/heartbeat", timeout=2)
        return response.status_code == 200
    except:
        return False

# Page configuration
st.set_page_config(
    page_title="SME Knowledge Chatbot - Phase 2",
    page_icon="🧠",
    layout="wide"
)

# Header
st.markdown('<div style="font-size: 2.5rem; font-weight: bold; text-align: center; padding: 1rem 0; color: #1f77b4;">🧠 SME Knowledge Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Phase 2: Semantic Search & RAG - Your Local AI with Memory</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = """Hello! I'm your Phase 2 AI assistant with RAG capabilities.

**New in Phase 2:**
- 🔍 Semantic search through your knowledge vault
- 📚 Answers with source citations
- 🎯 Understanding meaning, not just keywords

**Note**: RAG indexing features coming soon. For now, enjoy enhanced chat capabilities!
"""
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_msg
    })

# Sidebar
with st.sidebar:
    st.header("ℹ️ System Status")

    ollama_status = check_ollama_connection()
    chromadb_status = check_chromadb_connection() if ENABLE_RAG else None

    st.markdown(f"""
    **LLM Model**: {MODEL_NAME}
    **Ollama**: {'🟢 Connected' if ollama_status else '🔴 Disconnected'}

    **RAG Status**: {'🟢 Enabled' if ENABLE_RAG else '⚪ Disabled'}
    **ChromaDB**: {'🟢 Connected' if chromadb_status else '🔴 Disconnected' if ENABLE_RAG else 'N/A'}
    **Embedding Model**: {EMBEDDING_MODEL if ENABLE_RAG else 'N/A'}
    """)

    st.markdown("---")

    st.header("✨ Phase 2 Features")
    st.markdown("""
    - ✅ 100% Local & Private
    - ✅ ChromaDB Integration
    - 🚧 Semantic Search (In Progress)
    - 🚧 Source Citations (In Progress)

    ### Coming in Phase 3
    - 🔜 Knowledge Graph (Neo4j)
    - 🔜 Relationship Mapping
    - 🔜 MCP Integration
    """)

    st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

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

                # Add to chat history
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
            error_msg = "⚠️ Request timed out. Try a simpler query."
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
