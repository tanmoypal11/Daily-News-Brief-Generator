import streamlit as st

st.set_page_config(page_title="Technical Documentation", layout="wide", page_icon="📑")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; }
    .sub-header { font-size: 1.5rem; font-weight: 600; color: #1E40AF; margin-top: 20px; }
    .highlight { background-color: #EFF6FF; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">📑 Technical Overview & Judge Documentation</div>', unsafe_allow_html=True)
st.caption("AI Daily News Brief Generator | Multi-Source Personalization Engine")

st.divider()

# --- SECTION 1: CORE SYSTEM ARCHITECTURE ---
st.header("1. Core System Architecture")
st.write("Our system follows a **Retrieval-Augmented Generation (RAG)** pattern designed for real-time news.")



col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Data Refresh Rate", value="1 Hour (Cached)")
with col2:
    st.metric(label="Primary Model", value="Llama-3.3-70B")
with col3:
    st.metric(label="Processing Layer", value="Async Python/Groq")

st.markdown("""
### 🛠️ The Tech Stack
- **Frontend:** Streamlit for high-reactivity UI.
- **Aggregation:** NewsAPI fetching from 150,000+ sources including BBC, Reuters, and The Hindu.
- **Synthesis:** Groq-hosted Llama-3.3-70B for near-instant 1-minute summaries.
- **Performance:** `@st.cache_data` implementation to ensure API rate limits are never exceeded.
""")

st.divider()

# --- SECTION 2: JUDGE'S EVALUATION CRITERIA ---
st.header("🎯 Evaluation Criteria: Deep Dive")

# Personalization Section
st.subheader("👤 Personalization & State Management")
st.info("""
**How it works:** The application uses `st.session_state` to persist user-selected 'segments' (e.g., Tech, Business). 
1. **Default Load:** On launch, the app auto-generates a brief for the user's favorite categories.
2. **Dynamic Querying:** Queries are reconstructed in real-time based on the 'Region' and 'Segment' inputs.
3. **Reading Preference:** A custom slider allows users to choose between 'Short', 'Concise', or 'Detailed' synthesis.
""")

# Conflict & Duplicate Handling
st.subheader("⚖️ Conflict & Duplicate Management")
with st.container():
    st.write("""
    One of the major challenges of news aggregation is **redundancy**. Our Llama-3 system prompt includes specific logic for:
    - **Deduplication:** The AI identifies multiple sources reporting the same event and merges them into a single coherent paragraph.
    - **Consensus vs. Conflict:** The system is instructed to highlight consensus across sources while neutrally noting any conflicting facts (e.g., 'Source A reports 50 casualties while Source B reports 42').
    """)
    st.code("""
# Excerpt from our Deduplication Prompt
"If stories overlap, merge them into one narrative. 
If sources conflict, neutrally state the discrepancy."
    """)

# Neutrality Section
st.subheader("🛡️ Neutrality & Bias Mitigation")
st.warning("""
**Mitigation Strategy:**
- **Temperature Control:** We set the model temperature to **0.3**. High temperature leads to 'creative' but potentially biased summaries; low temperature ensures factual grounding.
- **Neutral Persona:** The AI is strictly role-played as a 'Neutral News Editor.'
- **Source Transparency:** We provide a 'Verified Sources' expander under every summary so users can verify the raw data themselves.
""")

st.divider()

# --- SECTION 3: USER FLOW ---
st.header("🏗️ Sample User Flows")
tab1, tab2 = st.tabs(["Standard Daily Brief", "Targeted AI Search"])

with tab1:
    st.markdown("""
    1. **User opens app:** Preferences for 'Tech' and 'Business' are loaded from state.
    2. **Aggregation:** System fetches 10 articles per category from NewsAPI.
    3. **Summarization:** AI synthesizes the articles into a 3-sentence Executive Brief.
    4. **Exploration:** User uses the 'Summary Detail' slider to expand the brief.
    """)

with tab2:
    
    st.markdown("""
    1. **Query:** User types "Latest on ISRO Moon Mission" into the News Assistant.
    2. **Focus:** System bypasses standard segments to fetch specific mission data.
    3. **Insight:** AI generates a targeted brief focused exclusively on that specific topic.
    """)

st.success("Documentation Complete. Ready for evaluation.")
