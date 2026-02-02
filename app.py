import streamlit as st
import requests
from groq import Groq
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Personalized Daily Brief", page_icon="🗞️", layout="wide")

# Check for API Keys in Secrets
if "GROQ_API_KEY" not in st.secrets or "NEWS_API_KEY" not in st.secrets:
    st.error("Missing API Keys! Please add GROQ_API_KEY and NEWS_API_KEY to your Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- CORE LOGIC ---

def fetch_news(category, date, region="India"):
    """Fetch news from multiple sources via NewsAPI [cite: 151, 152]"""
    url = "https://newsapi.org/v2/everything"
    query = f"{category} {region}"
    
    params = {
        "q": query,
        "from": date.strftime('%Y-%m-%d'),
        "to": date.strftime('%Y-%m-%d'),
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Return top 6 articles to ensure multi-source diversity [cite: 200]
        return response.json().get("articles", [])[:6]
    return []

def generate_ai_brief(articles, category):
    """Consolidated daily brief and article summaries using AI [cite: 157, 158]"""
    if not articles:
        return None, None

    # Prepare context for AI
    context = ""
    for i, art in enumerate(articles):
        context += f"Source {i+1} ({art['source']['name']}): {art['title']} - {art['description']}\n"

    prompt = f"""
    You are an AI news editor. Based on these articles for the '{category}' segment:
    1. Create a 3-sentence 'Consolidated Executive Brief' that synthesizes the main trends.
    2. Provide a 1-sentence punchy summary for each unique story.
    3. Ensure the tone is strictly neutral, professional, and unbiased. 
    4. If stories overlap, merge them into a single insight to avoid duplication.
    
    News Articles:
    {context}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3 # Low temperature for neutrality and factual consistency 
    )
    return completion.choices[0].message.content

# --- UI & USER EXPERIENCE [cite: 137, 165] ---

# 1. User Preference Management (First-time setup/Sidebar) [cite: 141, 189]
with st.sidebar:
    st.title("⚙️ Your Preferences")
    
    # Category selection [cite: 142]
    all_categories = ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics"]
    if "user_prefs" not in st.session_state:
        st.session_state.user_prefs = ["Technology", "Business"]
    
    st.session_state.user_prefs = st.multiselect(
        "Select your preferred segments:", 
        all_categories, 
        default=st.session_state.user_prefs
    )

    region = st.radio("Region focus:", ["India", "Global"], horizontal=True)
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    
    st.divider()
    if st.button("🔄 Refresh Latest Updates"): # [cite: 164]
        st.rerun()

# 2. Main Page Display [cite: 128, 167]
st.title(f"🗞️ Your Daily Brief — {selected_date.strftime('%d %b %Y')}")
st.caption(f"Personalized for {region} interests | Sources include BBC, Reuters, The Hindu, and more ")

if not st.session_state.user_prefs:
    st.warning("Please select at least one news segment in the sidebar to begin.")
else:
    # Section-wise layout [cite: 168]
    for category in st.session_state.user_prefs:
        with st.container():
            st.header(f"🔹 {category}")
            articles = fetch_news(category, selected_date, region)
            
            if articles:
                # Generate AI Summaries [cite: 155]
                with st.spinner(f"Synthesizing {category} brief..."):
                    brief_content = generate_ai_brief(articles, category)
                    st.markdown(brief_content)
                
                # Source references and timestamps [cite: 169]
                with st.expander("🔗 View Primary Sources"):
                    for art in articles:
                        st.markdown(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
                st.divider()
            else:
                st.info(f"No significant updates found for {category} on this date.")
