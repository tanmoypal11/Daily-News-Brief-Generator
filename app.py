import streamlit as st
import requests
from groq import Groq
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="India Daily News Brief", page_icon="🗞️", layout="wide")

# Initialize Clients
if "NEWS_API_KEY" not in st.secrets or "GROQ_API_KEY" not in st.secrets:
    st.error("Please set NEWS_API_KEY and GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- FUNCTIONS ---

def fetch_india_news(category, date):
    """Fetches news from multiple Indian sources using NewsAPI."""
    # We use /everything to allow for historical date filtering as per project requirements
    url = "https://newsapi.org/v2/everything"
    
    # Mapping 'Politics' and others to specific queries for better Indian context
    query = f"{category} India"
    
    params = {
        "q": query,
        "from": date.strftime('%Y-%m-%d'),
        "to": date.strftime('%Y-%m-%d'),
        "language": "en",
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])[:5] # Get top 5 articles
    return []

def summarize_brief(articles, category):
    """Uses Groq to summarize the headlines into a concise brief."""
    if not articles:
        return "No news found for this date/category."
    
    # Combine headlines and snippets for the AI
    context = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])
    
    prompt = f"""
    You are an expert news editor. Summarize the following news headlines about '{category}' in India 
    into a concise, 10-bullet point brief for a busy professional. 
    Focus on impact and clarity.
    
    News Data:
    {context}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return completion.choices[0].message.content

# --- UI LAYOUT ---

st.title("🇮🇳 AI Daily News Brief Generator")
st.markdown("---")

# Sidebar for Preferences (Required by Project Doc)
with st.sidebar:
    st.header("Settings")
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    st.info("This app aggregates news from multiple sources and uses Llama-3 to summarize them.")
    
    # Your existing Chatbot logic integrated as a 'News Assistant'
    st.divider()
    st.subheader("🤖 Ask News Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if chat_input := st.chat_input("Ask about today's news..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        # Note: In a production app, you'd pass the current news as context here.
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.rerun()

# Main Tabs (The 6 categories you requested)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Technology", "Business", "Sports", "Health", "Entertainment", "Politics"
])

tabs = {
    "Technology": tab1, "Business": tab2, "Sports": tab3, 
    "Health": tab4, "Entertainment": tab5, "Politics": tab6
}

for category, tab_obj in tabs.items():
    with tab_obj:
        st.header(f"Top {category} Stories")
        
        with st.spinner(f"Aggregating {category} news..."):
            articles = fetch_india_news(category, selected_date)
            
            if articles:
                # 1. AI Summary Section
                st.subheader("✨ AI Summary")
                summary = summarize_brief(articles, category)
                st.write(summary)
                
                # 2. Source List (Required for Multi-Source Aggregation)
                st.divider()
                st.subheader("🔗 Full Articles")
                for art in articles:
                    with st.expander(f"{art['source']['name']}: {art['title']}"):
                        st.write(art['description'])
                        st.link_button("Read Full Story", art['url'])
            else:

                st.warning("No news found for this category on the selected date.")
