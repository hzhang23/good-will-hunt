# Good Will Hunt: AI Job Hunter App

## 🚀 Project Overview
**Good Will Hunt** is a lightweight, agentic Web App designed to automate the most tedious parts of the job application process: scraping job descriptions (JD), analyzing fit, and generating tailored resumes. 

The system uses a **Google Gemini-powered Agent** that integrates directly with the user's Google account for storage (Sheets) and document generation (Docs).

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Auth:** Google OAuth 2.0 (User-centric data ownership)
* **Agent Framework:** [LangChain](https://www.langchain.com/)
* **Brain:** Google Gemini 1.5 Pro / Flash
* **Database:** Google Sheets (Created automatically in User's Drive)
* **Tools:** Playwright (Scraping), Tavily/Google (Search)

---

## 1. System Architecture (Flowchart)

```mermaid
graph TD
    User(["👤 User"]) -->|1. Google Login| Auth["🔑 OAuth 2.0"]
    Auth -->|2. Check/Create DB| GDrive[("📂 User's Google Drive")]
    GDrive -->|3. Load Data| UI["💻 Streamlit Dashboard"]
    
    UI -->|Sets Search Criteria| P_DB[("📋 Sheet: Job Profiles")]

    subgraph Automation_Engine ["Daily Automated Engine"]
        Agent{"🧠 Gemini Agent Brain"} -->|4. Fetch Active Profiles| P_DB
        
        subgraph Processing_Loop ["Search & Analysis"]
            Agent -->|5. Search & Scrape| Tools["🛠️ Scraper Tools"]
            Tools -.->|Returns JDs| Agent
            Agent -->|6. Tailor Resume| LLM(("🤖 Gemini 1.5 API"))
        end
    end

    Agent -->|7. Archive Results| T_DB[("📊 Sheet: Jobs Tracker")]
    T_DB -->|8. Ready for Review| UI
```

## 2. Sequence Diagram (Initial Setup & Loop)

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant App as 💻 Streamlit App
    participant G as 🔑 Google Auth/API
    participant A as 🧠 Gemini Agent
    participant S as 📊 Google Sheets (DB)

    U->>App: Clicks "Login with Google"
    App->>G: Request OAuth Token
    G-->>App: Return User Credentials
    
    App->>G: Search for "Good Will Hunt DB" in Drive
    alt File Not Found
        App->>G: Create Spreadsheet "Good Will Hunt DB"
        App->>G: Create Tabs: 'Job Profiles', 'Jobs Tracker'
    end
    
    App->>U: Show Dashboard (Profiles & Tracker)
    
    Note over App, A: Automation Triggered (Manual or Scheduled)
    
    A->>S: Read active profiles
    A->>A: Scrape & Analyze via Gemini
    A->>S: Append found jobs to 'Jobs Tracker'
```

## 3. Data Schema (Google Sheets)
The database is a Google Sheet created in the **user's own account**.

### Tab: Job Profiles
| Column | Description |
| :--- | :--- |
| **Profile ID** | Unique ID |
| **Title** | Target Job Title (e.g. AI Engineer) |
| **Location** | Remote, Hybrid, etc. |
| **Keywords** | Key tech stack |
| **Status** | Active / Paused |

### Tab: Jobs Tracker
| Column | Description |
| :--- | :--- |
| **Date** | Timestamp |
| **Company** | Hiring Org |
| **Position** | Extracted Title |
| **Match Score** | Gemini's assessment (0-100) |
| **Resume URL** | Link to tailored Doc |
| **Status** | Pending, Applied, Interview, etc. |