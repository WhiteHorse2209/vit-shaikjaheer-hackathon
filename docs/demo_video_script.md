# 10-Minute Video Walkthrough Script
**Hackathon:** S&P Global & CRISIL Campus Hackathon 2026  
**Candidate Name:** SHAIK JAHEER AHMED  
**College Email ID:** shaikjaheer.ahmed2023@vitstudent.ac.in  
**College / Campus:** VELLORE INSTITUTE OF TECHNOLOGY CHENNAI  
**Track:** AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing (Module B)  
**Hosting Requirement:** YouTube (Unlisted), permissions set to "Anyone with the link can view".

---

## Video Timeline Breakdown (Total: 10:00 Minutes)

| Segment | Timestamp | Topic / Focus | On-Screen Action |
|---|---|---|---|
| **Part 1: Introduction** | 00:00 – 00:45 | Problem Statement & Objective | Show Title Slide, introduce candidate, VIT Chennai, and hackathon objectives |
| **Part 2: Architecture & Setup** | 00:45 – 01:45 | Quickstart, Setup & Verification | Show terminal running `python run_app.py`, test suite execution `pytest tests/` |
| **Part 3: Phase 1 Data Ingestion** | 01:45 – 03:00 | Multi-Source Ingestion & Clean | Inspect `/data/sample_news.json`, GDELT/NewsAPI schema, deduplication & company mapping |
| **Part 4: Phase 2 AI/NLP Engine** | 03:00 – 05:00 | FinBERT Sentiment & Impact Scoring | Run NLP processing, explain $P(\text{pos}) - P(\text{neg})$ formula, 11 categories, 1–10 impact score |
| **Part 5: Phase 3 Risk Intelligence** | 05:00 – 06:15 | Public Market & Synthetic Portfolio | Show `data/portfolio.csv` (₹100M: Equities, Bonds, Loans, Derivatives) & yfinance metrics |
| **Part 6: Phase 4 Module B Stress** | 06:15 – 08:00 | Strategic Stress Testing Execution | Demonstrate Impact $>7.0$ trigger, asset-level shocks, simulated loss calculation & history |
| **Part 7: Interactive Dashboard** | 08:00 – 09:15 | Live Jury Breaking News Simulator | Type custom breaking news headline live on dashboard, show instant FinBERT & shock results |
| **Part 8: Conclusion & Q&A Prep** | 09:15 – 10:00 | Key Results, Domain Impact & Wrap-up | Summarize business impact for S&P/CRISIL, acknowledge simulation assumptions |

---

## Detailed Step-by-Step Script & Talking Points

### [00:00 – 00:45] Part 1: Introduction & Problem Context
* **Action:** Display Slide 1 (`docs/presentation.pdf`) and the GitHub repository root.
* **Narration:**
  > "Hello respected judges and review committee from S&P Global and CRISIL. My name is Shaik Jaheer Ahmed, an individual participant from Vellore Institute of Technology Chennai. Today, I am thrilled to present my submission for the S&P Global & CRISIL Campus Hackathon 2026: The AI/NLP Financial Risk Engine and Strategic Portfolio Stress Testing Platform, implementing Module B.
  > In today's volatile financial markets, breaking news—such as geopolitical conflicts, central bank surprises, or credit rating downgrades—arrives at breakneck speed. Institutional risk teams struggle to manually translate these unstructured narratives into quantified portfolio shocks. Our platform bridges this gap completely."

### [00:45 – 01:45] Part 2: Quickstart, Setup & System Architecture
* **Action:** Open terminal in VS Code / Command Prompt. Run `python -m pytest tests/` to show all 28 tests passing. Then run `python run_app.py`.
* **Narration:**
  > "Let's first examine our codebase and test suite. The repository is completely self-contained and reproducible. By running `pytest tests/`, we observe 28 automated unit and integration tests passing with 100% success across all five phases.
  > Starting the application requires just one command: `python run_app.py`. This starts our FastAPI backend server on port 8000 and immediately opens our interactive glassmorphism dashboard in the browser."

### [01:45 – 03:00] Part 3: Phase 1 — Data Foundation
* **Action:** Navigate to the code in `src/ingestion/` and view `data/sample_news.json`. Show Swagger docs at `http://127.0.0.1:8000/docs`.
* **Narration:**
  > "Phase 1 establishes our Data Foundation. We ingest financial news from two primary external sources: GDELT 2.0 DOC API and NewsAPI. Every article is normalized into a strict Pydantic schema containing article ID, source, title, content, canonical URL, ISO 8601 UTC timestamp, and corporate entity.
  > We implemented SHA-256 cryptographic deduplication to eliminate redundant feeds, and an automated entity extractor that maps company mentions to standard exchange tickers like Apple to AAPL, Nvidia to NVDA, and JPMorgan to JPM.
  > Crucially, our system supports dual modes: LIVE mode for real-time querying, and DEMO mode using our vetted `/data/sample_news.json` dataset, guaranteeing 100% offline reproducibility without external network dependencies."

### [03:00 – 05:00] Part 4: Phase 2 — AI/NLP Financial Risk Engine
* **Action:** Open `src/nlp/sentiment.py` and `src/nlp/impact_scorer.py`. Show `/api/nlp/process` in Swagger or on the dashboard.
* **Narration:**
  > "Phase 2 is the core AI/NLP Risk Engine. For sentiment analysis, rather than generic sentiment models, we deploy ProsusAI FinBERT, a transformer model pre-trained specifically on financial text.
  > Following the hackathon guidelines, our sentiment score is calculated strictly as: Probability of Positive minus Probability of Negative, bounded smoothly between -1.0 and +1.0.
  > Next, our Event Classifier categorizes news into 11 distinct financial taxonomies, including Geopolitical, Macroeconomic, Credit Event, Market Crash, Bankruptcy, Regulatory, and Earnings.
  > Finally, our Impact Scorer calculates an AI-derived event severity score from 1.0 to 10.0. The formula combines base event severity with sentiment amplification—where negative sentiment amplifies downside risk—and keyword severity modifiers. Any event scoring above 7.0 is flagged as a high-impact crisis trigger."

### [05:00 – 06:15] Part 5: Phase 3 — Financial Risk Intelligence & Synthetic Portfolio
* **Action:** Open `data/portfolio.csv` and show the portfolio breakdown doughnut chart on the dashboard.
* **Narration:**
  > "In Phase 3, we incorporate public financial intelligence. Using yfinance, we track 10 benchmark mega-cap equities—including AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, V, and NFLX—calculating 30-day historical returns and annualized volatility.
  > We constructed a synthetic multi-asset portfolio totaling ₹100 Million INR, structured across four asset tiers:
  > Equities: ₹40 Million (40%) across our 10 tracked companies;
  > Bonds: ₹25 Million (25%) in sovereign Treasuries and corporate fixed income;
  > Loans: ₹20 Million (20%) in syndicated commercial credit; and
  > Derivatives: ₹15 Million (15%) in equity index puts, rate swaps, and CDS baskets.
  > All predefined shock matrices are maintained transparently in `data/stress_scenarios.csv`."

### [06:15 – 08:00] Part 6: Phase 4 — Module B: Strategic Portfolio Stress Testing
* **Action:** Click "Execute Stress Tests (>7.0)" on the dashboard. Point out the summary cards and the asset comparison bar chart.
* **Narration:**
  > "Now let us examine Module B: Strategic Portfolio Stress Testing. When a risk signal arrives, the engine evaluates its impact score. If the score is less than or equal to 7.0, the event is treated as routine and maintained in monitoring mode with zero portfolio shock.
  > However, if Impact is greater than 7.0, the stress test triggers automatically!
  > The engine identifies the event category, loads the scenario shocks, and computes asset-level write-downs. For example, during an Algorithmic Market Crash (Impact 8.8), our Equities suffer a -15% shock, Bonds -5%, Loans -5%, and Derivatives -18%.
  > The portfolio value drops from ₹100 Million to ₹89.05 Million, reflecting a simulated crisis loss of ₹10.95 Million (-10.95%).
  > Every execution is recorded with a unique Run ID, parameters, and UTC timestamp into our SQLite audit trail."

### [08:00 – 09:15] Part 7: Interactive Dashboard & Custom Headline Simulator
* **Action:** Scroll to the "Live Interactive Headline Stress Test Simulator" on the dashboard. Enter a custom headline (e.g., "Catastrophic sovereign debt default and bank run in European credit syndicate"). Click "Run AI Signal & Shock". Show the real-time card and updated audit table.
* **Narration:**
  > "To make this prototype truly dynamic for the jury, we built a Live Interactive Headline Simulator into the dashboard.
  > Let's test a custom breaking event right now: 'Catastrophic sovereign debt default and bank run in European credit syndicate'.
  > When I click 'Run AI Signal & Shock', the backend immediately calls FinBERT. The sentiment score is calculated as -0.84, the event is classified as CREDIT_EVENT, and the impact score reaches 8.3 out of 10.
  > Because 8.3 is greater than 7.0, the stress engine triggers immediately! It applies our predefined credit shock—reducing Equities by -8%, Bonds -7%, Loans -10%, and Derivatives -10%—resulting in a simulated loss of ₹8.55 Million (-8.55%). The audit trail updates in real time!"

### [09:15 – 10:00] Part 8: Conclusion, Domain Impact & Wrap-Up
* **Action:** Switch back to Slide 6 & 7 in `docs/presentation.pdf`.
* **Narration:**
  > "In summary, our solution delivers immense business value for institutions like S&P Global and CRISIL. It converts qualitative news into quantitative risk signals, provides early warning indicators for credit underwriters, and enables dynamic tail-risk hedging for asset managers.
  > All assumptions, datasets, and code are completely open-source under the MIT license, cleanly structured, and 100% reproducible.
  > Thank you so much for your time and consideration. I am excited and ready for the live jury pitch!"
