🗞️ Daily News Brief Generator
A Personalized, AI-Driven News Synthesis System

The Daily News Brief Generator is an intelligent news aggregator designed to combat information overload. Instead of scrolling through endless headlines, users receive a Consolidated Executive Brief tailored to their specific interests (Tech, Business, Politics, etc.), region, and date.

By leveraging Llama-3.3-70B via Groq and NewsAPI, the system fetches real-time data, deduplicates overlapping stories, and presents a neutral, high-impact summary.

🚀 Live Demo
[https://daily-news-brief-generator-jeappevnrnyqz4xabvr9bx6.streamlit.app/]

✨ Key Features
Personalized Dashboards: Defaults to your favorite segments on load using st.session_state.

Multi-Source Synthesis: Aggregates data from global and local Indian sources (BBC, Reuters, The Hindu, etc.).

AI News Assistant: A "Chat-style" search box on the main screen for specific, real-time queries.

Smart Deduplication: AI logic identifies and merges duplicate news stories from different outlets into a single narrative.

Source Transparency: Every summary includes a "View Sources" expander with direct links and timestamps.

🛠️ Tech Stack
Frontend: Streamlit (Python-based Web Framework)

AI Engine: Groq Cloud (Llama-3.3-70B-Versatile)

News Data: NewsAPI

Deployment: Streamlit Cloud

📁 Repository Structure
Plaintext
├── app.py                 # Main application (News Briefing Dashboard)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── pages/                 # Multi-page directory
    └── overview.py  # Technical deep-dive & Judge Q&A
⚙️ Setup & Installation
Clone the Repository:

Bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Secrets: Create a .streamlit/secrets.toml file (for local testing) or add these to your Streamlit Cloud secrets:

Ini, TOML
GROQ_API_KEY = ""
NEWS_API_KEY = ""
Run the App:

Bash
streamlit run app.py
🧠 Technical Logic (For Judges)
1. Personalization Logic
The app uses a Reactivity Loop. When a user selects a category (e.g., "Technology"), the app dynamically constructs a search query combined with the user's selected region and date. Preferences are stored in the session state to ensure a seamless "Default Home Page" experience.

2. Conflict & Duplicate Handling
We utilize the high reasoning capability of Llama-3.3-70B. We feed it a context of 6 articles per category. The system prompt instructs the AI to:

Identify overlapping facts.

Merge them into a single coherent paragraph.

Highlight consensus and note discrepancies between sources.

3. Neutrality & Bias Mitigation
To ensure the reports remain unbiased:

Low Temperature: The LLM temperature is set to 0.3 to prevent "hallucinations" or creative opinions.

Source Diversity: By pulling from 6 different publishers, we prevent a single-source narrative from dominating the brief.

Journalistic Prompting: The system role is defined as a "Strictly Neutral News Editor."

📬 Contact & Submission
Developer: Tanmoy Pal

Project Goal: Submission for the AI Daily News Brief Challenge.