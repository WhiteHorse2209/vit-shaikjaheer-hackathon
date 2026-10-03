# Presentation Deck Content & Speaker Notes (7 Slides)
**Event:** S&P Global & CRISIL Campus Hackathon 2026  
**Candidate Name:** SHAIK JAHEER AHMED  
**College Email ID:** shaikjaheer.ahmed2023@vitstudent.ac.in  
**College / Campus:** VELLORE INSTITUTE OF TECHNOLOGY CHENNAI  
**Module Selected:** MODULE B — Strategic Portfolio Stress Testing  
**Document File:** [`docs/presentation.pdf`](file:///c:/Users/my%20pc/Desktop/S&P/docs/presentation.pdf)

---

## Slide 1: Title Slide
* **Slide Title:** AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing
* **Subtitle:** Module B: Autonomous Multi-Asset Crisis Simulation Engine
* **Candidate Info:**
  * Candidate Name: SHAIK JAHEER AHMED
  * College Email ID: shaikjaheer.ahmed2023@vitstudent.ac.in
  * College/Campus: Vellore Institute of Technology Chennai
  * Module: Module B (Strategic Portfolio Stress Testing)
* **Highlights:**
  * FinBERT NLP: $P(\text{positive}) - P(\text{negative})$ Sentiment Scoring $[-1.0, +1.0]$
  * 11-Category Financial Event Taxonomy & Calibrated Impact Scoring (1–10)
  * Multi-Asset Synthetic Portfolio (₹100M: Equities, Bonds, Loans, Derivatives)
  * Autonomous Stress Trigger on Severity $>7.0$ with Predefined Asset Shocks
* **Speaker Notes:**
  > "Respected jury members, my name is Shaik Jaheer Ahmed from VIT Chennai. Today, I am proud to present our AI/NLP Financial Risk Engine and Strategic Portfolio Stress Testing platform. This solution addresses a critical institutional problem: bridging the gap between unstructured, real-time financial news and immediate, quantitative multi-asset stress testing."

---

## Slide 2: Problem Statement & Solution Approach
* **The Business Problem:**
  * **Unstructured Financial Noise:** High-velocity news from global feeds (GDELT, NewsAPI) is overwhelming for human analysts.
  * **Lagging Traditional Indicators:** Financial statements and quarterly ratios reflect past data rather than sudden black-swan geopolitical or liquidity shocks.
  * **Disconnected Stress Testing:** Institutional stress testing cycles are traditionally periodic (annual or quarterly) and disconnected from live newsflow.
  * **Need for Quantified Machine-Readable Signals:** Risk desks need an explainable, automated bridge from breaking text to portfolio impact.
* **Our Five-Phase Approach:**
  * **Phase 1 (Data Foundation):** Dual-mode ingestion (GDELT + NewsAPI), SHA-256 deduplication, ISO 8601 normalization, and company-to-ticker mapping.
  * **Phase 2 (AI/NLP Risk Engine):** Fine-tuned ProsusAI FinBERT for financial sentiment, 11-category event taxonomy, and a calibrated 1–10 impact scoring engine.
  * **Phase 3 (Financial Risk Intelligence):** Public market tracking of 10 benchmark stocks via yfinance, and construction of an INR 100M 4-asset synthetic portfolio.
  * **Phase 4 (Module B Stress Testing):** Automatic threshold trigger for Impact $>7.0$, loading predefined shock scenarios and calculating pre/post valuations and loss.
  * **Phase 5 (Productization):** High-performance FastAPI REST backend, SQLite audit storage, and a modern glassmorphism dashboard.
* **Speaker Notes:**
  > "Traditional risk workflows are reactive. When a geopolitical crisis or a sudden credit rating downgrade hits the wire, portfolio managers often wait days for scenario risk teams to model the exposure. Our system solves this by building an autonomous pipeline that digests breaking news, extracts structured signals, and triggers multi-asset stress testing in sub-seconds."

---

## Slide 3: System Design & End-to-End Architecture
* **Data Ingestion Layer:**
  * Primary: GDELT 2.0 DOC API (`mode=artlist`, `format=json`).
  * Secondary: NewsAPI v2 (`/v2/everything` with financial queries).
  * Offline Resilience: Local `/data/sample_news.json` ensuring 100% test reproducibility.
* **Preprocessing & Normalization:**
  * HTML tag stripping, entity decoding, SHA-256 deterministic article hashing, ISO 8601 UTC timestamp parser.
* **Core NLP Engine:**
  * ProsusAI FinBERT: Softmax output yielding $P(\text{pos}) - P(\text{neg})$ bounded in $[-1.0, +1.0]$.
  * Event Classifier: 11 categories (Geopolitical, Macroeconomic, Credit Event, Merger/Acquisition, Product Launch, Earnings, Regulatory, Bankruptcy, Interest Rate, Market Crash, Other).
  * Impact Scorer: 1.0 to 10.0 calibrated event severity metric based on base risk, sentiment modifier, and keyword multipliers.
* **Strategic Stress Testing (Module B):**
  * Impact Check: If Impact $>7.0$, initiates stress shock.
  * Scenario Matrix: Predefined shocks across Equities, Bonds, Loans, and Derivatives.
* **Storage & Presentation:**
  * SQLite DB (`risk_engine.db`), FastAPI REST API (10 endpoints), Glassmorphism UI with Chart.js.
* **Speaker Notes:**
  > "Here is our complete system architecture. Data enters through GDELT and NewsAPI, undergoes strict normalization and deduplication, and feeds into our FinBERT engine. Notice the clean separation of concerns: the NLP engine outputs machine-readable JSON signals, which are then consumed by Module B to simulate shocks across our ₹100M portfolio."

---

## Slide 4: Implementation Highlights & Tech Stack
* **FinBERT Financial Sentiment Analysis:**
  * Why FinBERT? General-purpose models (VADER or BERT-base) fail on financial vernacular where words like 'liability', 'downgrade', or 'default' carry distinct risk connotations.
  * Strict formula: $\text{Sentiment Score} = P(\text{positive}) - P(\text{negative})$.
* **Calibrated Impact Scoring (1 to 10):**
  * Base Category Weights: Market Crash (8.5), Bankruptcy (8.2), Geopolitical (7.6), Credit Event (7.3), Macroeconomic (6.8), Regulatory (6.5).
  * Sentiment Amplification: Downside risk amplifies when sentiment is negative ($+1.8 \times |\text{sentiment}|$).
  * Explicit Assumption: AI-derived severity metric for scenario stress analysis, NOT an empirical market prediction.
* **Module B Strategic Stress Engine:**
  * Synthetic Portfolio: Equities (₹40M, 10 stocks), Bonds (₹25M, Treasuries & IG), Loans (₹20M, Syndicated CRE), Derivatives (₹15M, Index Puts & Swaps).
  * Predefined Asset Shocks: e.g., Market Crash triggers Equities $-15\%$, Bonds $-5\%$, Loans $-5\%$, Derivatives $-18\%$.
* **Robust Software Engineering:**
  * FastAPI + Pydantic v2 for typed validation, SQLAlchemy ORM with SQLite, 28 comprehensive automated pytest tests.
* **Speaker Notes:**
  > "For our NLP model, we selected ProsusAI FinBERT because it was pre-trained on Financial PhraseBank corpora. In finance, context is critical. Furthermore, our impact scoring formula is mathematically grounded and bounded strictly between 1.0 and 10.0, providing a clear deterministic trigger for stress simulations."

---

## Slide 5: Key Results & Stress Testing Simulations
* **Simulation Results Table:**
  * **Market Crash (Impact 8.8):** Portfolio moves from ₹100.0M to ₹89.05M $\rightarrow$ Simulated Loss: ₹10.95M ($-10.95\%$) [Triggered]
  * **Geopolitical Conflict (Impact 8.2):** Portfolio moves from ₹100.0M to ₹92.35M $\rightarrow$ Simulated Loss: ₹7.65M ($-7.65\%$) [Triggered]
  * **Credit Event Downgrade (Impact 7.9):** Portfolio moves from ₹100.0M to ₹91.45M $\rightarrow$ Simulated Loss: ₹8.55M ($-8.55\%$) [Triggered]
  * **Fintech Bankruptcy (Impact 8.1):** Portfolio moves from ₹100.0M to ₹89.50M $\rightarrow$ Simulated Loss: ₹10.50M ($-10.50\%$) [Triggered]
  * **Regulatory Antitrust (Impact 7.5):** Portfolio moves from ₹100.0M to ₹94.45M $\rightarrow$ Simulated Loss: ₹5.55M ($-5.55\%$) [Triggered]
  * **Quarterly Earnings Beat (Impact 4.5):** Sub-threshold $\rightarrow$ Loss: ₹0.0 [Monitoring Only]
  * **Robotaxi Launch (Impact 4.0):** Sub-threshold $\rightarrow$ Loss: ₹0.0 [Monitoring Only]
* **Validation & Testing:**
  * 100% test coverage across 28 automated tests.
  * Verified exact mathematical shock accounting across all 4 asset classes.
* **Speaker Notes:**
  > "This slide showcases our empirical simulation outputs. For high-impact tail events, such as an algorithmic flash crash or a Taiwan strait supply chain blockade, the engine immediately flags the severity as $>7.0$, applies the shock vector, and demonstrates a severe drawdown of up to ₹10.95M. Routine earnings and product releases remain safely below the threshold in monitoring mode."

---

## Slide 6: Domain Impact & Financial Relevance
* **Credit Risk Underwriting & Banking:**
  * **Early Warning Indicator:** Alerts credit committees to borrower liquidity stress and potential debt haircut risks before quarterly filings.
  * **Syndicated Loan Vulnerability:** Instantly isolates risk on our ₹20M syndicated loan portfolio during commercial real estate rating downgrades.
* **Asset & Wealth Management:**
  * **Dynamic Cross-Asset Hedging:** Provides portfolio managers with pre-calculated post-shock valuations, enabling timely derivative put-option rebalancing.
  * **Beyond Single-Stock Betas:** Models multi-asset contagion across Equities, Fixed Income, Loans, and Derivatives.
* **Regulatory Compliance & Enterprise Governance:**
  * **Automated Scenario Generation:** Accelerates internal capital adequacy assessment processes (ICAAP/CCAR) using live global news.
  * **Immutable Audit Trail:** Every simulated run records a unique Run ID, parameter breakdown, and UTC timestamp in SQLite for internal auditors.
* **Speaker Notes:**
  > "From a domain perspective, this directly empowers both CRISIL rating analysts and S&P risk managers. It transforms breaking qualitative news into instant scenario analysis, giving credit officers and investment committees proactive visibility into tail-risk vulnerabilities before liquidity freezes occur."

---

## Slide 7: Assumptions, Limitations & Future Roadmap
* **Simulation Assumptions:**
  * 1. The stress test is a scenario sensitivity simulation based on predefined rules, not an empirical market prediction.
  * 2. Public and synthetic data only: No proprietary or confidential client information used.
  * 3. Uniform asset-class shocks: Assumes uniform percentage haircuts across securities within an asset tier.
* **Future Roadmap:**
  * 1. **Non-Linear Derivatives Greeks:** Integrate Black-Scholes Delta, Gamma, and Vega sensitivity modeling.
  * 2. **Supply-Chain Knowledge Graph:** Map multi-tier corporate dependencies (e.g., TSMC to NVDA/AAPL).
  * 3. **Historical Backtesting Engine:** Backtest simulated stress shocks against real historical market drawdowns (e.g., March 2020, 2008).
* **Speaker Notes:**
  > "To ensure academic integrity, we emphasize that our stress test is a scenario simulation rather than a guaranteed market prediction. In future work, we plan to incorporate non-linear option Greeks and multi-tier supply chain knowledge graphs to further enhance institutional risk modeling. Thank you, and I look forward to your questions."
