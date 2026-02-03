# 🗞️ Daily News Brief Generator

An AI-powered, personalized news aggregation and summarization platform that delivers **concise, neutral, and relevant daily news briefs** tailored to individual user preferences.

---

## 📌 Overview

In an era of information overload, the **Daily News Brief Generator** helps users stay informed without the noise. The application aggregates news from multiple trusted sources and uses large language models to generate **clear, unbiased, and easy-to-read summaries** based on user-selected interests.

The platform prioritizes:

* Personalization
* Multi-source aggregation
* Neutral AI summarization
* Clean and intuitive UX

---

## 🎯 Key Features

### 👤 Personalized News Experience

* Select preferred news segments (Technology, Business, Sports, Health, etc.)
* Preferences persist using session state
* Personalized brief loads automatically on home page

### 📰 Multi-Source News Aggregation

* Fetches news from **NewsAPI** (BBC, Reuters, The Hindu, and more)
* Supports region-based filtering (India / Global)
* Cached for performance and API efficiency

### 🤖 AI-Powered Summarization

* Uses **LLaMA 3.3 (70B)** via Groq for ultra-fast inference
* Generates:

  * Consolidated executive briefs
  * Bullet-level summaries
* Deduplicates overlapping stories
* Neutrally highlights conflicting reports across sources

### ⚙️ Customization Options

* Change:

  * News category
  * Date (explore past briefs)
  * Reading depth (Bullet / Concise / Detailed)
* On-demand topic search via AI News Assistant

### 🏠 Home Page Experience

* Section-wise personalized layout
* Timestamped briefs
* Verified source references with links

---

## 🧠 System Architecture

**Design Pattern:** Retrieval-Augmented Generation (RAG)

**Flow:**

1. Fetch news articles from APIs
2. Cache results for 1 hour
3. Feed cleaned data into LLM
4. Generate neutral, consolidated summaries
5. Render results in Streamlit UI

---

## 🛠️ Tech Stack

| Layer        | Technology       |
| ------------ | ---------------- |
| Frontend     | Streamlit        |
| Backend      | Python           |
| News Sources | NewsAPI          |
| AI / NLP     | LLaMA 3.3 (Groq) |
| Caching      | Streamlit Cache  |
| Storage      | Session State    |
| Deployment   | Streamlit Cloud  |

---

## 📂 Project Structure

```
Daily-News-Brief-Generator/
│
├── app.py                 # Main application logic
├── pages/
│   └── overview.py        # Technical documentation & judge guide
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Daily-News-Brief-Generator.git
cd Daily-News-Brief-Generator
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Secrets

Create `.streamlit/secrets.toml`

```toml
NEWS_API_KEY = "your_newsapi_key"
GROQ_API_KEY = "your_groq_api_key"
```

### 4️⃣ Run Locally

```bash
streamlit run app.py
```

---

## 🌐 Deployment

The application is deployed using **Streamlit Cloud**.

Judges and users can:

* Select news segments
* Change date and reading preferences
* Generate real-time AI summaries
* Explore targeted topic-based insights

🔗 **Public URL:** *(Add deployed app link here)*

---

## 🔍 Sample Output

**Your Daily Tech Brief – 14 Nov 2025**

* AI regulation discussions intensify across global markets
* Major tech firm releases new open-source AI framework
* Cybersecurity concerns rise after recent data breaches

**Business Highlights:**

* Markets show mixed trends amid inflation worries
* Startup funding slows in Q4

Sources: BBC, Reuters, The Hindu

---

## ⚖️ Neutrality & Bias Mitigation

* Low temperature setting (0.3) for factual consistency
* Explicit system role: *Neutral News Editor*
* Conflicting reports highlighted without opinion
* Full source transparency via verified links

---

## 🧪 Evaluation Alignment

| Criteria        | Implementation            |
| --------------- | ------------------------- |
| Personalization | Session-based preferences |
| Insight Quality | AI executive synthesis    |
| Multi-Source    | NewsAPI aggregation       |
| AI Utilization  | LLaMA 3.3 summarization   |
| UX              | Clean Streamlit UI        |
| Deployment      | Public Streamlit app      |

---

## 🚀 Future Enhancements

* User authentication & persistent profiles
* Multi-language news support
* Sentiment indicators
* Email-based daily brief delivery
* Offline dataset mode

---

## 📜 License

This project is intended for educational and evaluation purposes.

---

✅ **Ready for evaluation. Built for clarity, speed, and insight.**
