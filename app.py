import streamlit as st
import requests
from groq import Groq
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Personalized India News Brief", page_icon="🗞️", layout="wide")

# Check for API Keys
if "GROQ_API_KEY" not in st.secrets or "NEWS_API_KEY" not in st.secrets:
    st.error("Missing API Keys! Please add GROQ_API_KEY and NEWS_API_KEY to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- CORE LOGIC ---

def fetch_news(query_term, date, region="India"):
    """
    Fetch news from multiple sources via NewsAPI
    """
    url = "https://newsapi.org/v2/everything"
    search_query = f"{query_term} {region}"
    
    params = {
        "q": search_query,
        "from": date.strftime('%Y-%m-%d'),
        "to": date.strftime('%Y-%m-%d'),
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("articles", [])[:6]
    except Exception:
        return []
    return []

def generate_ai_brief(articles, category):
    """Generates the specific format requested: Brief, Punchy Summaries, and Merging Note"""
    if not articles:
        return None

    context = ""
    for i, art in enumerate(articles):
        context += f"Source {i+1} ({art['source']['name']}): {art['title']} - {art['description']}\n"

    # Strict formatting instructions
    prompt = f"""
    You are an AI news editor. Based on these articles for '{category}':
    
    1. Start with 'Consolidated Executive Brief: ' followed by a 3-sentence synthesis.
    2. Then write 'Punchy Summaries:' followed by a list of 1-sentence summaries for each unique story.
    3. End with a 'Note: ' explaining if you merged overlapping stories (be specific about which sources).
    
    Tone: Strictly neutral, professional, and unbiased.
    
    News Articles:
    {context}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return completion.choices[0].message.content

# --- UI & STATE MANAGEMENT ---

if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "search_query" not in st.session_state:
    st.session_state.search_query = None

# Sidebar for Preferences
with st.sidebar:
    st.title("⚙️ Personalization")
    
    all_categories = ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics","Everything"]
    user_prefs = st.multiselect("Your preferred segments:", all_categories, default=["Technology", "Business"])
    
    region = st.radio("Region:", ["India", "Global"], horizontal=True)
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    
    st.divider()
    
    st.subheader("🤖 News Assistant")
    chat_input = st.chat_input("Ask about a specific topic...")
    
    if chat_input:
        with st.spinner(f"Searching for '{chat_input}'..."):
            results = fetch_news(chat_input, selected_date, region)
            if results:
                st.session_state.search_query = chat_input
                st.session_state.search_result = {
                    "brief": generate_ai_brief(results, chat_input),
                    "sources": results
                }
            else:
                st.session_state.search_query = chat_input
                st.session_state.search_result = "No news found."

# --- MAIN SCREEN DISPLAY ---

st.title(f"🗞️ Daily News Briefing")
st.caption(f"Showing results for {selected_date.strftime('%d %b %Y')} | Region: {region}")

# 1. Display Chat Search Result First
if st.session_state.search_result:
    st.markdown(f"## 🔍 Search: {st.session_state.search_query}")
    if isinstance(st.session_state.search_result, dict):
        st.markdown(st.session_state.search_result["brief"])
        
        with st.expander("🔗 View Sources & Timestamps"):
            for art in st.session_state.search_result["sources"]:
                st.markdown(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
    else:
        st.info(st.session_state.search_result)
    
    if st.button("Clear Search Results"):
        st.session_state.search_result = None
        st.rerun()
    st.divider()

# 2. Display Categorized News
for category in user_prefs:
    st.markdown(f"### 🔹 {category}")
    articles = fetch_news(category, selected_date, region)
    
    if articles:
        with st.spinner(f"Summarizing {category}..."):
            brief = generate_ai_brief(articles, category)
            st.markdown(brief)
        
        with st.expander("🔗 View Sources & Timestamps"):
            for art in articles:
                st.markdown(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
        st.divider()
    else:
        st.info(f"No news found for {category}.")

