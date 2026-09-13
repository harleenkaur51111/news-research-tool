# Equity Research News Tool 📈

A password-protected, AI-powered tool that fetches recent news articles on 
a given query and generates a concise summary using an LLM — built for 
quick equity research.

## Features
- 🔒 Simple password-protected login
- 🔎 Search news by company, ticker, or topic
- 🤖 AI-generated summaries of the latest related articles
- 🕘 Session history of past searches (viewable in the sidebar)
- ⬇️ Download any summary as a `.txt` file

## Tech Stack
- **Streamlit** – web interface
- **NewsAPI.org** – fetches recent news articles
- **Groq (LLM)** + **LangChain** – summarizes the articles

## Setup

1. Clone or download this project folder.
2. Create a virtual environment:

python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the project root with:
GROQ_API_KEY=your-groq-key-here
NEWSAPI_KEY=your-newsapi-org-key-here
APP_PASSWORD=choose-any-password-here

5. Run the app:

## Usage
1. Enter the password you set in `.env` to log in.
2. Enter a company name, topic, or keyword in the query box and click 
   **Get News** to receive an AI-generated summary of recent related articles.
3. View past searches from this session in the sidebar.
4. Click **Download this summary** to save any result as a text file.
5. Click **Log out** in the sidebar to end your session.

## Notes
- Uses NewsAPI.org's free tier (100 requests/day, dev use only).
- Uses Groq's free tier (`openai/gpt-oss-20b` model).
- Search history is session-based only — it resets when the app restarts.


