import streamlit as st

st.set_page_config(page_title="Project Documentation", layout="wide", page_icon="📑")

# Professional Styling
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 Project Overview & Documentation")
st.caption("Daily News Brief Generator | Technical Deep-Dive")

st.divider()

# --- SECTION 1: CORE ESSENCE ---
st.header("1. Project Essence")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="System Focus", value="Personalization")
with m_col2:
    st.metric(label="Primary LLM", value="Llama-3.3 70B")
with m_col3:
    st.metric(label="Data Source", value="NewsAPI (Live)")

st.info("**Problem Statement:** Readers face information overload. This app filters global news into a 1-minute 'Executive Brief' tailored specifically to user-defined segments.")

st.divider()

# --- SECTION 2: JUDGE'S Q&A (Personalization, Conflicts, Neutrality) ---
st.header("🎯 Judge's Technical Q&A")
st.write("Direct answers to key evaluation criteria:")

q_col1, q_col2, q_col3 = st.columns(3)

with q_col1:
    st.success("### 👤 Personalization")
    st.markdown("""
    **Q: How is it implemented?**
    - **Selection:** Users pick segments (Tech, Politics, etc.) in the sidebar.
    - **Persistence:** Choices are stored in `st.session_state` to keep the brief consistent.
    - **Dynamic Queries:** The backend crafts specific search strings (e.g., 'Business + India') based on these preferences.
    """)

with q_col2:
    st.warning("### ⚖️ Conflicts & Duplicates")
    st.markdown("""
    **Q: How are duplicates handled?**
    - **AI Synthesis:** The LLM is prompted to identify overlapping facts across the 6 source articles.
    - **Deduplication:** It merges similar stories into a single 'Consolidated Brief' and notes the merged sources at the bottom.
    """)

with q_col3:
    st.error("### 🛡️ Neutrality & Bias")
    st.markdown("""
    **Q: How is bias mitigated?**
    - **Low Temperature:** Set to `0.3` to ensure factual grounding over creativity.
    - **Source Diversity:** Aggregating from 6 different outlets prevents a single-source narrative.
    - **Strict Prompting:** The AI is forbidden from using emotive or opinionated language.
    """)

st.divider()

# --- SECTION 3: DOCUMENTATION (Aggregation & Flows) ---
st.header("🏗️ Technical Documentation")



tab1, tab2 = st.tabs(["Aggregation Approach", "Sample User Flows"])

with tab1:
    st.subheader("News Aggregation Strategy")
    st.write("""
    We use a **Context-Injection Pipeline**:
    1. **Fetch:** The app calls NewsAPI using the user's selected category, region, and date.
    2. **Filter:** We extract the Title, Source Name, and Description of the top 6 most relevant articles.
    3. **Augment:** This raw data is injected into the AI prompt, allowing the model to summarize news that happened *today*, bypassing its training cutoff.
    """)

with tab2:
    st.subheader("Step-by-Step User Flow")
    
    st.markdown("""
    1. **Landing:** User sees a default personalized brief.
    2. **Customization:** User adds "Health" in the sidebar and changes the region to "Global."
    3. **Regeneration:** The app fetches global health news and updates the main screen instantly.
    4. **Assistance:** User types "Latest on S25 Ultra" in the chat box to get a specific targeted summary.
    5. **Verification:** User expands the 'Sources' section to see original links for further reading.
    """)
