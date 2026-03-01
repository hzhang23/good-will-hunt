# 📋 Good Will Hunt: Task Tracker

## Phase 1: Authentication & Identity
- [x] **Task 1.1:** Setup Google OAuth 2.0 flow in Streamlit.
- [x] **Task 1.2:** Implement token persistence in `st.session_state`.
- [x] **Task 1.3:** Handle login/logout UI states in `app.py`.
- [ ] **Task 1.4:** Prompt user to grant Drive/Sheets permissions if missing.

## Phase 2: Dynamic Database (Google Drive/Sheets)
- [x] **Task 2.1:** Build `google_manager.py` to interface with Drive and Sheets APIs.
- [x] **Task 2.2:** Implement "Auto-Setup" logic: Check for existing `Good Will Hunt DB` and create it if missing.
- [x] **Task 2.3:** Map Streamlit data editors to live Google Sheet tabs (`Job Profiles` & `Jobs Tracker`).

## Phase 3: The Gemini Agent Brain
- [ ] **Task 3.1:** Initialize Gemini 1.5 Pro/Flash via `langchain-google-genai`.
- [ ] **Task 3.2:** Define the Agent's system prompt and reasoning loop (ReAct).
- [ ] **Task 3.3:** Implement structured output for job analysis and match scoring.

## Phase 4: Agent Toolset
- [ ] **Task 4.1:** **Search Tool:** Integrate Tavily/Google Search for finding job listings.
- [ ] **Task 4.2:** **Scraper Tool:** Implement Playwright logic to extract clean JDs from URLs.
- [ ] **Task 4.3:** **Resume Tailor Tool:** LLM logic to generate tailored content based on a "Base Resume".

## Phase 5: Integration & Automation
- [ ] **Task 5.1:** Connect the "Search Strategy" UI to trigger the Agent loop.
- [ ] **Task 5.2:** Implement the "Human-in-the-loop" approval flow (Syncing edits back to Sheets).
- [ ] **Task 5.3:** Final end-to-end testing and styling.
