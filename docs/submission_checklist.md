# Hackathon Deliverables & Submission Compliance Checklist
**Hackathon:** S&P Global & CRISIL Campus Hackathon 2026  
**Candidate Name:** SHAIK JAHEER AHMED  
**College Email ID:** shaikjaheer.ahmed2023@vitstudent.ac.in  
**College / Campus:** VELLORE INSTITUTE OF TECHNOLOGY CHENNAI  
**Module Selected:** MODULE B — Strategic Portfolio Stress Testing  

---

## 1. Core Deliverables Verification Matrix

| # | Required Deliverable | Repository Location | Format / Verification Status |
|---|---|---|---|
| **1** | **Source Code & Architecture** | `src/` (`ingestion/`, `nlp/`, `risk/`, `api/`, `database/`) | 100% Complete; 28/28 automated pytest tests passing |
| **2** | **Architecture Flow Diagram** | [`docs/architecture.png`](file:///c:/Users/my%20pc/Desktop/S&P/docs/architecture.png) | High-Resolution 1600x950 PNG diagram |
| **3** | **Presentation Deck** | [`docs/presentation.pdf`](file:///c:/Users/my%20pc/Desktop/S&P/docs/presentation.pdf) | Exact 7 slides (16:9 PDF format); outline in [`presentation_content.md`](file:///c:/Users/my%20pc/Desktop/S&P/docs/presentation_content.md) |
| **4** | **Demo Video Walkthrough** | Link in [`README.md`](file:///c:/Users/my%20pc/Desktop/S&P/README.md) (YouTube Unlisted) | 10-Minute script in [`demo_video_script.md`](file:///c:/Users/my%20pc/Desktop/S&P/docs/demo_video_script.md) |
| **5** | **All Data Used** | `data/` (`sample_news.json`, `portfolio.csv`, `stress_scenarios.csv`, `market_cache.json`, `risk_signals.json`) | Public / synthetic datasets only; zero proprietary data |
| **6** | **Open Source License** | [`LICENSE`](file:///c:/Users/my%20pc/Desktop/S&P/LICENSE) | MIT License; Mandatory compliance satisfied |
| **7** | **Dependencies Specification** | [`requirements.txt`](file:///c:/Users/my%20pc/Desktop/S&P/requirements.txt) | Python dependencies specified with minimum version bounds |
| **8** | **Environment Template** | [`.env.example`](file:///c:/Users/my%20pc/Desktop/S&P/.env.example) | Clean environment variable documentation |
| **9** | **Live Jury Pitch Preparation** | [`docs/jury_qa_preparation.md`](file:///c:/Users/my%20pc/Desktop/S&P/docs/jury_qa_preparation.md) | Detailed responses to expected jury questions |

---

## 2. Rule-by-Rule Compliance Check

- [x] **Individual Submission:** Single candidate (SHAIK JAHEER AHMED).
- [x] **Public GitHub Repository:** Code contains zero binary dumps or huge models; repository is prepared for public GitHub publication.
- [x] **Confidentiality:** Zero S&P Global, CRISIL, or private client data used. Only public (GDELT, NewsAPI, yfinance) and synthetic data.
- [x] **No Hardcoded API Keys:** API keys use environment variables (`NEWSAPI_KEY` via `.env`).
- [x] **Module B Requirements Met:**
  - Consumes Event Classification and Impact Score: **Yes**.
  - Synthetic portfolio with equities, bonds, loans, and derivatives: **Yes (₹100M total)**.
  - Detects high-impact events: **Yes**.
  - Triggers stress test when Impact Score $>7.0$: **Yes**.
  - Applies predefined financial shocks depending on event type: **Yes**.
  - Calculates portfolio value before and after stress test: **Yes**.
  - Visualizes results through a dashboard: **Yes (Modern Glassmorphism UI)**.
- [x] **Explicit Assumptions Documented:** All stress test calculations labeled as scenario simulations rather than market predictions.
- [x] **Test Suite Coverage:** All 5 phases tested using `pytest tests/` with 100% pass rate.
