# Live Jury Pitch: Technical Q&A Preparation
**Hackathon:** S&P Global & CRISIL Campus Hackathon 2026  
**Candidate Name:** SHAIK JAHEER AHMED (VIT Chennai)  
**Track:** AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing (Module B)

---

## 1. NLP & FinBERT Architecture Questions

### Q1: Why did you choose ProsusAI FinBERT instead of standard BERT, RoBERTa, or GPT-4?
* **Answer:**
  > "Standard language models like BERT-base or RoBERTa are trained on general web corpora (Wikipedia/BookCorpus) where financial terminology has completely different sentiment semantics. For instance, in general English, words like 'liability', 'debt', 'shares', 'downgrade', or 'depreciation' are treated neutrally or ambiguously. ProsusAI FinBERT is specifically pre-trained and fine-tuned on financial text corpora (including Financial PhraseBank), capturing precise domain nuances. Furthermore, FinBERT runs locally with deterministic latency (under 50ms per sentence on CPU), requires zero external API cost, and does not risk leaking sensitive query data to external commercial LLM APIs."

### Q2: How exactly is the sentiment score calculated, and how do you guarantee it stays within $[-1.0, +1.0]$?
* **Answer:**
  > "FinBERT outputs three raw classification logits corresponding to `[positive, negative, neutral]`. We apply a Softmax activation function across these logits to compute probability distributions:
  > $$P(\text{positive}) + P(\text{negative}) + P(\text{neutral}) = 1.0$$
  > In strict accordance with the hackathon specification, we calculate:
  > $$\text{Sentiment Score} = P(\text{positive}) - P(\text{negative})$$
  > Because probabilities are non-negative and sum to at most 1, if $P(\text{pos}) = 1.0$ and $P(\text{neg}) = 0.0$, the score is $+1.0$. If $P(\text{neg}) = 1.0$ and $P(\text{pos}) = 0.0$, the score is $-1.0$. If the text is purely neutral ($P(\text{neu}) = 1.0$), both $P(\text{pos})$ and $P(\text{neg})$ approach 0, yielding a score near $0.0$. Thus, it is mathematically bounded strictly between $-1.0$ and $+1.0$."

### Q3: How does your Event Classification taxonomy work? Is it keyword-based, zero-shot, or machine learning?
* **Answer:**
  > "Our Event Classifier combines a domain-specific financial semantic ontology with regularized token boundary matching across 11 key financial categories: Geopolitical, Macroeconomic, Credit Event, Merger/Acquisition, Product Launch, Earnings, Regulatory, Bankruptcy, Interest Rate, Market Crash, and Other. We prioritized an explainable, deterministic taxonomy over an opaque black-box classifier because regulatory risk management demands auditability: risk officers and auditors must know exactly which phrases and triggers categorized an event."

---

## 2. Impact Scoring & Risk Methodology Questions

### Q4: Explain your Impact Scoring methodology. How do you derive the 1 to 10 score?
* **Answer:**
  > "Our Impact Score is an AI-derived event severity metric designed to quantify systemic market disruption potential for scenario analysis. The calculation is structured as:
  > $$\text{Raw Score} = \text{Base Severity} + \text{Sentiment Modifier} + \text{Keyword Intensity}$$
  > 1. **Base Severity:** Historical systemic disruption potential by event type (e.g., Market Crash: 8.5, Bankruptcy: 8.2, Geopolitical: 7.6, Credit Event: 7.3 down to Product Launch: 4.0).
  > 2. **Sentiment Modifier:** When sentiment is negative, downside risk is amplified ($+1.8 \times |\text{sentiment}|$). When positive, downside shock potential is tempered ($-0.8 \times \text{sentiment}$).
  > 3. **Keyword Intensity:** Detection of systemic crisis terms ('catastrophic', 'liquidity freeze', 'margin calls', 'blockade', 'run on') adds $+0.4$ to $+1.0$.
  > 4. **Clamping:** The final score is clamped strictly between $1.0$ and $10.0$."

### Q5: Is the Impact Score a guaranteed market prediction?
* **Answer:**
  > "No, absolutely not, and we explicitly document this disclaimer across our code, API, and dashboard. The impact score is an AI-derived scenario severity indicator used for stress testing and sensitivity analysis, NOT an empirical market forecast. Making predictive claims without decades of validated statistical backtesting would violate professional financial standards."

---

## 3. Financial Portfolio & Stress Testing Questions (Module B)

### Q6: Walk us through the structure of your ₹100M synthetic portfolio.
* **Answer:**
  > "Our portfolio is defined in `data/portfolio.csv` and totals ₹100,000,000 across four distinct asset classes:
  > 1. **Equities (₹40M / 40%):** Diversified across 10 benchmark companies (AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, V, NFLX).
  > 2. **Bonds (₹25M / 25%):** US 10-Year Sovereign Treasuries, Investment Grade Corporate Debt, and High-Yield debt baskets.
  > 3. **Loans (₹20M / 20%):** Syndicated commercial real estate facilities, SME working capital revolvers, and automotive asset-backed facilities.
  > 4. **Derivatives (₹15M / 15%):** S&P 500 index put hedges, 5-year fixed-to-float interest rate swaps, and CDX investment-grade credit default swaps."

### Q7: Why did you set the trigger threshold at Impact > 7.0? What happens if an event scores 6.8?
* **Answer:**
  > "The $>7.0$ threshold was specified by S&P Global and CRISIL in the hackathon brief to distinguish routine market noise from tail-risk crisis events. If an event scores 6.8 (such as a standard corporate earnings report or a minor regulatory inquiry), our engine treats it as a sub-threshold event: it remains in monitoring status, records zero shock to the portfolio, and produces ₹0 simulated loss. This eliminates false-positive stress test churn."

### Q8: How are asset-level shocks applied during a stress test?
* **Answer:**
  > "When Impact $>7.0$, the engine retrieves the predefined shock vector from `data/stress_scenarios.csv`. For example, for an Algorithmic Market Crash (Impact 8.8):
  > - Equities shock: $-15\%$ on ₹40M $\rightarrow$ Loss: ₹6.0M
  > - Bonds shock: $-5\%$ on ₹25M $\rightarrow$ Loss: ₹1.25M
  > - Loans shock: $-5\%$ on ₹20M $\rightarrow$ Loss: ₹1.0M
  > - Derivatives shock: $-18\%$ on ₹15M $\rightarrow$ Loss: ₹2.7M
  > Total Simulated Loss = ₹6.0M + ₹1.25M + ₹1.0M + ₹2.7M = ₹10.95M ($-10.95\%$).
  > Post-Stress Portfolio Valuation = ₹89.05M."

---

## 4. Engineering, Data & Production Questions

### Q9: How do you handle cases where GDELT or NewsAPI APIs are down, rate-limited, or run offline?
* **Answer:**
  > "Our system implements a resilient dual-mode architecture. In LIVE mode, it queries GDELT and NewsAPI with configurable timeouts. If network errors or rate limits occur, the pipeline gracefully logs a warning and falls back to our curated offline dataset in `/data/sample_news.json`. In DEMO mode, the system runs 100% offline with zero external network dependencies, ensuring an uninterrupted live jury demo."

### Q10: How do you handle article deduplication?
* **Answer:**
  > "We compute a deterministic 16-character SHA-256 hash using the cleaned lowercase article title and canonical URL:
  > `hashlib.sha256(f'{title}|{url}'.encode('utf-8')).hexdigest()[:16]`
  > When identical stories are syndicated across multiple RSS feeds or domains, the pipeline filters out duplicates before they reach the NLP engine, preventing double-counting."

### Q11: What is the database schema and why SQLite?
* **Answer:**
  > "We use SQLite via SQLAlchemy ORM. SQLite requires zero configuration, zero daemon processes, and stores data in a single portable file (`data/risk_engine.db`). The schema includes:
  > - `articles`: Stores ingested titles, cleaned text, source, ISO timestamps, and tickers.
  > - `risk_signals`: Stores FinBERT sentiment score, event classification, impact score, and confidence.
  > - `stress_test_runs`: Maintains an immutable audit trail of Run IDs, pre/post valuations, and asset breakdown JSON."
