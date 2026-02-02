import streamlit as st

st.set_page_config(page_title="Project Overview: Daily News Brief Generator", layout="wide")

st.title("🗞️ Project Overview: Daily News Brief Generator")
st.subheader("AI-Driven Personalized Insight Delivery")

# --- NAVIGATION ---
tabs = st.tabs(["📌 Project Essence", "⚙️ Implementation Details", "🤖 Judge Q&A", "🚀 User Flow"])

with tabs[0]:
    st.header("Project Purpose & Problem Statement")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**The Purpose:** To help readers consume relevant information efficiently in an era of information overload[cite: 7].")
    with col2:
        st.warning("**The Problem:** Users struggle to filter news by interest, track updates across segments, and avoid long, generic articles[cite: 3, 6, 7].")

    st.header("Core Objectives")
    st.markdown("""
    - **Personalization:** Build a system that understands and caters to specific reader preferences[cite: 18].
    - **Multi-Source Synthesis:** Aggregate and summarize news from diverse, reliable outlets[cite: 19].
    - **UX Excellence:** Provide a clean, intuitive, and publicly accessible interface[cite: 21, 22].
    """)

with tabs[1]:
    st.header("Technical Requirements & Stack")
    
    st.markdown("### Functional Features")
    cols = st.columns(3)
    cols[0].write("**User Management:** Preference selection for segments like Tech, Business, and Politics[cite: 25, 26].")
    cols[1].write("**News Collection:** Multi-source fetching via NewsAPI and search queries[cite: 34, 35].")
    cols[2].write("**AI Summarization:** Consolidated briefs and punchy 1-sentence summaries[cite: 39, 40].")

    st.markdown("### Technical Stack")
    st.code("""
    - Backend: Python
    - Frontend: Streamlit
    - AI Engine: Groq (Llama-3.3-70b-versatile)
    - News Source: NewsAPI
    - Deployment: Streamlit Cloud
    """)

with tabs[2]:
    st.header("Addressing Critical Project Questions")
    
    with st.expander("🔍 1. How is personalization implemented?"):
        st.markdown("""
        **Implementation:** [cite: 25, 33, 51]
        - **Sidebar Controls:** Users dynamically select news segments (e.g., Technology, Sports) and regions (India vs. Global).
        - **Session State:** The app uses `st.session_state` and a default selection system to ensure the home page displays the user's preferred brief immediately upon loading.
        - **Date-Specific Logic:** Users can choose a specific date, allowing the AI to regenerate content for "past or alternate" interests[cite: 47].
        """)

    with st.expander("⚖️ 2. How is conflicting or duplicate news handled?"):
        st.markdown("""
        **Implementation:** [cite: 115]
        - **AI Synthesis:** The prompt sent to the Llama-3 model specifically instructs it to "merge overlapping stories to avoid duplication." 
        - **Contextual Awareness:** By feeding the AI 6 articles at once, the model identifies thematic overlaps and creates a "Consolidated Executive Brief" that combines facts from multiple sources into one cohesive narrative.
        - **Transparency:** The app includes a specific "Note" at the end of summaries explaining which sources were merged[cite: 42].
        """)

    with st.expander("🛡️ 3. How are summaries kept neutral and unbiased?"):
        st.markdown("""
        **Implementation:** [cite: 116]
        - **Strict Prompt Engineering:** The system prompt mandates a "strictly neutral, professional, and unbiased" tone.
        - **Multi-Source Aggregation:** By pulling from various outlets (e.g., BBC, Reuters, The Hindu), the AI is exposed to different perspectives, preventing single-source bias[cite: 35, 70].
        - **Low Temperature Setting:** The AI's `temperature` is set to 0.3 to minimize "creativity" and ensure the model remains grounded in the provided factual data.
        """)

with tabs[3]:
    st.header("Expected Application Flow")
    st.markdown(f"""
    1. **Landing:** User opens the application[cite: 72].
    2. **Setup:** User selects segments (e.g., Business, Health) in the sidebar[cite: 73].
    3. **Briefing:** The app automatically loads the personalized brief on the home page[cite: 74].
    4. **Interaction:** User can change dates or refresh the feed to get the latest updates[cite: 77, 78].
    5. **Deep Dive:** User explores concise summaries or uses the **News Assistant** for specific real-time queries.
    """)
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
