import streamlit as st
import requests
from groq import Groq
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Daily News Brief", page_icon="🗞️", layout="wide")

# Check for API Keys
if "GROQ_API_KEY" not in st.secrets or "NEWS_API_KEY" not in st.secrets:
    st.error("Missing API Keys! Please add them to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- CORE LOGIC WITH CACHING ---

@st.cache_data(ttl=3600) # Cache news for 1 hour
def fetch_news(query_term, date, region="India"):
    url = "https://newsapi.org/v2/everything"
    # Improved query for better quality results
    search_query = f"{query_term} AND {region}"
    
    params = {
        "q": search_query,
        "from": date.strftime('%Y-%m-%d'),
        "to": date.strftime('%Y-%m-%d'),
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("articles", [])
    except Exception as e:
        st.error(f"Error fetching news: {e}")
    return []

def generate_ai_brief(articles, category, detail_level="Concise"):
    if not articles:
        return None

    # Filter out removed articles
    valid_articles = [a for a in articles if a['title'] != "[Removed]"]
    
    context = ""
    for i, art in enumerate(valid_articles[:6]):
        context += f"Source {i+1} ({art['source']['name']}): {art['title']} - {art['description']}\n"

    # Enhanced logic for neutrality and conflict resolution
    prompt = f"""
    You are a professional, neutral AI news editor. Your task is to summarize news for the '{category}' segment.
    
    FORMATTING RULES:
    1. Start with '### 📌 Consolidated Executive Brief'
    2. Provide a 3-sentence synthesis of the most important developments.
    3. If different sources report conflicting facts, note the discrepancy neutrally (e.g., 'While Source A reports X, Source B suggests Y').
    4. Group overlapping stories together to avoid repetition.
    5. List 'Punchy Summaries' for unique stories.
    6. Detail Level: {detail_level}.
    
    TONE: Third-person, objective, no inflammatory language, no personal opinions.
    
    NEWS DATA:
    {context}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a neutral news aggregator that deduplicates information."},
                      {"role": "user", "content": prompt}],
            temperature=0.3 # Low temperature for factual consistency
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# --- UI & STATE MANAGEMENT ---

# Initialize session state for personalization
if "prefs" not in st.session_state:
    st.session_state.prefs = ["Technology", "Business"]

with st.sidebar:
    st.title("⚙️ Personalization")
    
    all_categories = ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics", "Science", "Everything"]
    st.session_state.prefs = st.multiselect("Your preferred segments:", all_categories, default=st.session_state.prefs)
    
    region = st.radio("Focus Region:", ["India", "Global"], horizontal=True)
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    detail_level = st.select_slider("Reading Preference:", options=["Bullet Points", "Concise", "Detailed"], value="Concise")
    
    st.divider()
    st.subheader("🤖 News Assistant")
    chat_input = st.chat_input("Ask about a specific topic...")

# --- MAIN DASHBOARD ---

st.title("🗞️ Your Daily News Brief")
st.caption(f"Personalized for you | {selected_date.strftime('%d %B %Y')} | {region} Edition")

# Assistant Results (Top priority)
if chat_input:
    with st.status(f"Searching for '{chat_input}'...", expanded=True) as status:
        results = fetch_news(chat_input, selected_date, region)
        if results:
            brief = generate_ai_brief(results, chat_input, detail_level)
            st.markdown(f"## 🔍 Custom Insight: {chat_input}")
            st.markdown(brief)
            
            # --- ADDED THIS PART TO LIST SOURCES FOR SEARCH ---
            with st.expander("🔗 Verified Sources for this Search"):
                for art in results[:5]:
                    if art['title'] != "[Removed]":
                        st.write(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
            
            status.update(label="Search complete!", state="complete")
        else:
            st.warning(f"No recent news found for '{chat_input}'.")
    
    # Optional: Add a button to clear the search result and see categories again
    if st.button("❌ Clear Search Results"):
        st.rerun()
    st.divider()

# Personalized Segments
for category in st.session_state.prefs:
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.subheader(f"🔹 {category}")
        
        articles = fetch_news(category, selected_date, region)
        
        if articles:
            brief = generate_ai_brief(articles, category, detail_level)
            st.markdown(brief)
            
            with st.expander("🔗 Verified Sources"):
                for art in articles[:5]:
                    if art['title'] != "[Removed]":
                        st.write(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
        else:
            st.info(f"No updates for {category} on this date.")


