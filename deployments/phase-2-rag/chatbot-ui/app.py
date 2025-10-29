"""
SME Knowledge Graph - Phase 2 Chatbot with RAG
Chat interface with Ollama + ChromaDB for semantic search
"""

import streamlit as st
import requests
import os
import chromadb
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# --- Configuration ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")
CHROMADB_URL = os.getenv("CHROMADB_URL", "http://chromadb:8000")
parsed_url = urlparse(CHROMADB_URL)
CHROMADB_HOST = parsed_url.hostname
CHROMADB_PORT = parsed_url.port
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"
KNOWLEDGE_VAULT_PATH = Path(os.getenv("KNOWLEDGE_VAULT_PATH", "/knowledge-vault"))
COLLECTION_NAME = "knowledge_vault"

# --- Helper Functions ---
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
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT, tenant="default_tenant", database="default_database")
        client.heartbeat()
        return True
    except:
        return False

@st.cache_resource
def get_chroma_client():
    """Get a ChromaDB client"""
    return chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT, tenant="default_tenant", database="default_database")

def get_ollama_embedding(text):
    """Get embedding from Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBEDDING_MODEL, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        st.error(f"Error getting embedding: {e}")
        return None

def index_knowledge_vault():
    """Index all markdown files in the knowledge vault"""
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    files = list(KNOWLEDGE_VAULT_PATH.glob("*.md"))
    if not files:
        st.warning("No markdown files found in the knowledge vault.")
        return

    with st.spinner(f"Indexing {len(files)} files..."):
        for file in files:
            try:
                content = file.read_text(encoding="utf-8")
                title = content.split("\n")[0].replace("#", "").strip()
                # Simple chunking by paragraph
                chunks = [p.strip() for p in content.split("\n\n") if p.strip()]
                
                if not chunks:
                    continue

                # Add title to each chunk
                chunks_with_title = [f"Document: {title}\n\n{chunk}" for chunk in chunks]

                embeddings = [get_ollama_embedding(chunk) for chunk in chunks_with_title]
                
                collection.add(
                    ids=[f"{file.name}-{i}" for i in range(len(chunks))],
                    documents=chunks_with_title,
                    embeddings=embeddings,
                    metadatas=[{"source": file.name} for _ in chunks]
                )
            except Exception as e:
                st.error(f"Error indexing {file.name}: {e}")
        st.success(f"Indexed {len(files)} files.")

# --- UI ---
st.set_page_config(page_title="SME Knowledge Chatbot - Phase 2", page_icon="🧠", layout="wide")

st.markdown('<div style="font-size: 2.5rem; font-weight: bold; text-align: center; padding: 1rem 0; color: #1f77b4;">🧠 SME Knowledge Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Phase 2: Semantic Search & RAG</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your local AI assistant. Use the sidebar to index your knowledge vault."}]

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
    st.header("📚 Knowledge Vault")
    if st.button("Index Knowledge Vault"):
        index_knowledge_vault()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if ENABLE_RAG and chromadb_status:
            with st.spinner("Searching knowledge vault..."):
                try:
                    client = get_chroma_client()
                    collection = client.get_collection(name=COLLECTION_NAME)
                    
                    query_embedding = get_ollama_embedding(prompt)
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=3
                    )
                    
                    context = "\n".join(results['documents'][0])
                    sources = list(set(meta['source'] for meta in results['metadatas'][0]))
                    
                    st.write(f"Retrieved context:\n{context}")
                    rag_prompt = f"Based on the following context, answer the user's question.\n\nContext:\n{context}\n\nQuestion: {prompt}"
                    
                    st.session_state.messages.append({"role": "user", "content": rag_prompt})

                except Exception as e:
                    st.error(f"Error during RAG retrieval: {e}")
                    context = ""
                    sources = []
        
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={"model": MODEL_NAME, "messages": st.session_state.messages, "stream": False},
                    timeout=60
                )
                response.raise_for_status()
                assistant_message = response.json()["message"]["content"]
                
                if ENABLE_RAG and sources:
                    assistant_message += f"\n\n*Sources: {', '.join(sources)}*"

                message_placeholder.markdown(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})

            except Exception as e:
                error_msg = f"⚠️ An error occurred: {e}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})