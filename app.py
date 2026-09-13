import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_config import get_summary

load_dotenv()
APP_PASSWORD = os.getenv("APP_PASSWORD")

st.set_page_config(page_title="Equity Research News Tool", page_icon="📈", layout="centered")

# --- Simple password gate ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login Required")
    password_input = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if password_input == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# --- Keep a history list across reruns ---
if "history" not in st.session_state:
    st.session_state.history = []  # each item: {"query": ..., "summary": ..., "time": ...}

# --- Sidebar ---
with st.sidebar:
    st.header("ℹ️ About this tool")
    st.write(
        "Enter a company name, ticker, or topic to get a quick "
        "AI-generated summary of the latest related news."
    )
    st.write("**Examples:** Tesla, Infosys, Artificial Intelligence")
    st.divider()

    st.header("🕘 Past Searches")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            with st.expander(f"{item['query']} — {item['time']}"):
                st.write(item['summary'])
    else:
        st.caption("No searches yet this session.")

    st.divider()
    if st.button("Log out"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main app ---
st.title('📈 Equity Research News Tool')
st.write('Enter your query to get the latest news articles summarized.')

query = st.text_input('Query', placeholder="e.g. Reliance Industries")

col1, col2 = st.columns([1, 4])
with col1:
    search_clicked = st.button('Get News', type="primary")

if search_clicked:
    if query:
        with st.spinner(f'Searching news for "{query}" and summarizing...'):
            response = get_summary(query)
        st.success("Summary ready!")
        st.write('### 📝 Summary')
        st.write(response)

        # Save to session history
        st.session_state.history.append({
            "query": query,
            "summary": response,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        # Download button
        st.download_button(
            label="⬇️ Download this summary",
            data=f"Query: {query}\n\nSummary:\n{response}",
            file_name=f"summary_{query.replace(' ', '_')}.txt",
            mime="text/plain"
        )
    else:
        st.warning('Please enter a query.')