import streamlit as st

st.set_page_config(page_title="Project Documentation", layout="wide", page_icon="📑")

st.title("📑 Project Documentation & Overview")

# 1. Project Essence
st.header("1. Project Essence")
col1, col2 = st.columns(2)
with col1:
    st.info("**Purpose:** To help readers efficiently consume relevant news in a world of information overload.")
with col2:
    st.warning("**Problem:** Users struggle to filter interests and avoid generic, long-form articles.")

st.divider()

# 2. Technical Implementation Details
st.header("2. Technical Implementation")

tab1, tab2, tab3 = st.tabs(["Preference Handling", "News Aggregation", "AI & Neutrality"])

with tab1:
    st.subheader("Logic: User Preference Handling")
    st.write("""
    The application prioritizes user choice to provide a personalized experience:
    - **Session State Management:** The app uses `st.session_state` to store user-selected segments (e.g., Technology, Business) and regions. This ensures that the personalized brief remains consistent even if the page is refreshed during a single session.
    - **Sidebar Integration:** Preferences are collected via a sidebar `st.multiselect`. The main application loop reads these selections to trigger specific API calls for each chosen category.
    - **Persistence:** By default, the app initializes with "Technology" and "Business," allowing judges to see immediate value while offering full control to change them.
    """)

with tab2:
    st.subheader("Approach: News Aggregation")
    st.write("""
    To ensure diverse and reliable data, the app follows a multi-step aggregation pipeline:
    - **Multi-Source Fetching:** The system utilizes **NewsAPI** to query 'Everything' within the last 24 hours. This allows it to pull from global outlets like BBC, Reuters, and Al Jazeera, as well as local Indian sources.
    - **Query Construction:** For every category, the app constructs a targeted search query (e.g., `Technology India`).
    - **Data Filtering:** We limit results to the top 6 most relevant articles per category to maintain a "brief" format and stay within AI token limits.
    """)

with tab3:
    st.subheader("Logic: AI Synthesis & Neutrality")
    st.write("""
    - **Deduplication:** The Llama-3 model is explicitly prompted to identify and merge overlapping stories from different sources, preventing the user from reading the same fact twice.
    - **Neutrality:** The system prompt mandates a "strictly neutral, professional, and unbiased" tone. By using a low `temperature` (0.3), we ensure the AI sticks to the facts provided by the news sources.
    """)

st.divider()

# 3. Sample User Flows
st.header("3. Sample User Flows")

# Visualizing the flow


with st.expander("🚀 View Step-by-Step Flow"):
    st.markdown("""
    **Step 1: Landing & Initialization**
    - The user opens the URL. 
    - The app detects default preferences and automatically generates a "Technology" and "Business" brief.
    
    **Step 2: Personalization**
    - The user opens the sidebar and adds "Sports" to their preferred segments.
    - The app instantly reruns, fetches sports news, and adds a new summarized section to the dashboard.
    
    **Step 3: Deep Dive (AI Assistant)**
    - The user wants to know about a specific event not in the brief (e.g., "Budget 2024").
    - They type the query into the **News Assistant** chat box.
    - The app fetches the latest articles on that specific topic and generates a custom executive summary.
    
    **Step 4: Source Verification**
    - The user clicks the **"View Sources"** expander under any summary to see the original article links and verify the information.
    """)

st.divider()

# 4. Judge Q&A Section
st.header("4. Judge's Corner (Quick Answers)")
qa_col1, qa_col2 = st.columns(2)

with qa_col1:
    st.markdown("**Q: How do you handle conflicting news?**")
    st.write("A: The AI editor is instructed to note discrepancies if they exist but primarily focuses on synthesizing shared facts across sources to provide a 'Consolidated Executive Brief'.")

with qa_col2:
    st.markdown("**Q: Is this scalable?**")
    st.write("A: Yes. By using a modular `fetch_news` function and an LLM for synthesis, we can add more sources (RSS, GNews) or categories without changing the core UI.")
