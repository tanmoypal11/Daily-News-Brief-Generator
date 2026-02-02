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

def fetch_news(query_term, date, region="India"):
    """Fetch news from multiple sources via NewsAPI [cite: 35, 36]"""
    url = "https://newsapi.org/v2/everything"
    
    # Refined query for better search results
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
    """Consolidated daily brief and article summaries using AI [cite: 42, 43]"""
    if not articles:
        return None

    context = ""
    for i, art in enumerate(articles):
        context += f"Source {i+1} ({art['source']['name']}): {art['title']} - {art['description']}\n"

    prompt = f"""
    You are an AI news editor. Based on these articles for '{category}':
    1. Create a 3-sentence 'Consolidated Executive Brief'.
    2. Provide a 1-sentence punchy summary for each unique story.
    3. Ensure the tone is strictly neutral, professional, and unbiased. 
    4. Merge overlapping stories to avoid duplication. 
    
    News Articles:
    {context}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return completion.choices[0].message.content

# --- UI & USER EXPERIENCE ---

# 1. Sidebar: Preferences & Grounded News Assistant
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Personalization Logic [cite: 25, 26, 33]
    all_categories = ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics"]
    if "user_prefs" not in st.session_state:
        st.session_state.user_prefs = ["Technology", "Business"]
    
    st.session_state.user_prefs = st.multiselect(
        "Select segments:", 
        all_categories, 
        default=st.session_state.user_prefs
    )

    region = st.radio("Region focus:", ["India", "Global"], horizontal=True)
    selected_date = st.date_input("Select Date", datetime.now() - timedelta(days=1))
    
    if st.button("🔄 Refresh Latest"):
        st.rerun()

    st.divider()
    
    # --- GROUNDED CHATBOT LOGIC ---
    st.subheader("🤖 News Assistant")
    st.info("Ask me about specific topics (e.g., 'Cricket' or 'S25') and I'll search for today's news!")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if chat_input := st.chat_input("Ask about today's news..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        st.chat_message("user").write(chat_input)

        with st.chat_message("assistant"):
            # Step 1: Search for real-time context based on user question [cite: 114]
            with st.spinner("Searching latest news..."):
                real_time_news = fetch_news(chat_input, selected_date, region)
            
            # Step 2: Build the grounded prompt
            if real_time_news:
                context_info = "\n".join([f"- {a['title']}: {a['description']}" for a in real_time_news])
                system_instruction = f"""
                You are a News Assistant. Answer using this REAL-TIME data:
                {context_info}
                If the data doesn't answer the question, say so, but don't use old knowledge.
                """
            else:
                system_instruction = "I couldn't find specific news for that topic today. Please try another query."

            # Step 3: Call AI with context
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_instruction}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            
            response_text = chat_completion.choices[0].message.content
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# 2. Main Page: Personalized Brief [cite: 12, 51]
st.title(f"🗞️ Daily Brief — {selected_date.strftime('%d %b %Y')}")
st.caption(f"Personalized for {region} | Aggregated from multiple sources [cite: 70]")

if not st.session_state.user_prefs:
    st.warning("Please select a news segment in the sidebar.")
else:
    for category in st.session_state.user_prefs:
        with st.container():
            st.header(f"🔹 {category}")
            articles = fetch_news(category, selected_date, region)
            
            if articles:
                with st.spinner(f"Generating {category} brief..."):
                    brief = generate_ai_brief(articles, category)
                    st.markdown(brief)
                
                with st.expander("🔗 View Sources & Timestamps [cite: 53]"):
                    for art in articles:
                        st.markdown(f"**{art['source']['name']}**: [{art['title']}]({art['url']})")
                st.divider()
            else:
                st.info(f"No {category} updates found for this date.")
