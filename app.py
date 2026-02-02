import streamlit as st
import requests
from groq import Groq
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Global & India News Brief", page_icon="🗞️", layout="wide")

# Initialize Clients
if "NEWS_API_KEY" not in st.secrets or "GROQ_API_KEY" not in st.secrets:
    st.error("Please set NEWS_API_KEY and GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- FUNCTIONS ---

def fetch_news(category, date, region):
    """Fetches news based on category and region (India vs World)."""
    url = "https://newsapi.org/v2/everything"
    
    # Logic to switch query based on toggle
    query = f"{category} India" if region == "India" else f"{category}"
    
    params = {
        "q": query,
        "from": date.strftime('%Y-%m-%d'),
        "to": date.strftime('%Y-%m-%d'),
        "language": "en",
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("articles", [])[:5]
    except Exception as e:
        st.error(f"Error fetching news: {e}")
    return []

def summarize_brief(articles, category, region):
    """Uses Groq to summarize headlines into a 10-bullet point brief."""
    if not articles:
        return "No news found for this date/category."
    
    context = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])
    
    prompt = f"""
    You are an expert news editor. Summarize the following {region} news headlines about '{category}' 
    into a concise, 10-bullet point brief for a busy professional. 
    Ensure the tone is neutral and professional.
    
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

# Sidebar for Preferences
with st.sidebar:
    st.header("⚙️ Personalization")
    
    # --- THE TOGGLE ---
    region_toggle = st.radio("Select News Region:", ["India", "World"], index=0, horizontal=True)
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    
    st.divider()
    st.info(f"Currently viewing **{region_toggle}** news for **{selected_date}**.")
    
    # Integrated Chatbot Logic
    st.subheader("🤖 News Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if chat_input := st.chat_input("Ask about the news..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.rerun()

# Dynamic Title
flag = "🇮🇳" if region_toggle == "India" else "🌐"
st.title(f"{flag} AI {region_toggle} Daily Brief")
st.markdown(f"Generated for {selected_date.strftime('%B %d, %Y')}")
st.markdown("---")

# Main Tabs
tabs_list = ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics"]
tabs = st.tabs(tabs_list)

for i, category in enumerate(tabs_list):
    with tabs[i]:
        st.header(f"Top {category} Stories")
        
        with st.spinner(f"Gathering {region_toggle} {category} news..."):
            articles = fetch_news(category, selected_date, region_toggle)
            
            if articles:
                st.subheader("✨ AI Insights (10-Point Brief)")
                summary = summarize_brief(articles, category, region_toggle)
                st.markdown(summary)
                
                st.divider()
                st.subheader("🔗 Primary Sources")
                for art in articles:
                    with st.expander(f"{art['source']['name']} | {art['title']}"):
                        st.write(art['description'])
                        st.link_button("Read Original Article", art['url'])
            else:
                st.warning(f"No {category} news found for this date in the {region_toggle} region.")
