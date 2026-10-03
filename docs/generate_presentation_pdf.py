import fitz  # PyMuPDF
from pathlib import Path

def create_presentation_deck():
    doc = fitz.open()
    width, height = 960, 540  # 16:9 Presentation Dimensions
    
    # Color palette
    bg_color = (9/255, 13/255, 22/255)
    card_bg = (18/255, 24/255, 38/255)
    border_blue = (59/255, 130/255, 246/255)
    border_cyan = (6/255, 182/255, 212/255)
    border_red = (239/255, 68/255, 68/255)
    border_green = (16/255, 185/255, 129/255)
    text_white = (248/255, 250/255, 252/255)
    text_muted = (148/255, 163/255, 184/255)
    text_accent = (96/255, 165/255, 250/255)

    def add_slide_base(title, slide_num, category="S&P GLOBAL & CRISIL HACKATHON 2026"):
        page = doc.new_page(width=width, height=height)
        # Background
        page.draw_rect(fitz.Rect(0, 0, width, height), color=bg_color, fill=bg_color)
        # Top banner
        page.draw_rect(fitz.Rect(40, 25, width - 40, 75), color=card_bg, fill=card_bg)
        page.draw_line(fitz.Point(40, 75), fitz.Point(width - 40, 75), color=border_blue, width=1.5)
        
        # Category Tag
        page.insert_text(fitz.Point(55, 45), category, fontsize=9, color=text_accent, fontname="helv")
        # Slide Title
        page.insert_text(fitz.Point(55, 65), title, fontsize=16, color=text_white, fontname="hebo")
        
        # Slide Number
        page.insert_text(fitz.Point(width - 85, 55), f"0{slide_num} / 07", fontsize=11, color=text_muted, fontname="hebo")
        
        # Bottom Footer
        page.draw_line(fitz.Point(40, height - 30), fitz.Point(width - 40, height - 30), color=(30/255, 41/255, 59/255), width=1)
        page.insert_text(fitz.Point(45, height - 16), "Candidate: SHAIK JAHEER AHMED | Vellore Institute of Technology Chennai | Module B", fontsize=8, color=text_muted, fontname="helv")
        page.insert_text(fitz.Point(width - 240, height - 16), "Confidentiality: Public / Synthetic Data Only", fontsize=8, color=text_muted, fontname="helv")
        return page

    # ==================== SLIDE 1: TITLE SLIDE ====================
    p1 = doc.new_page(width=width, height=height)
    p1.draw_rect(fitz.Rect(0, 0, width, height), color=bg_color, fill=bg_color)
    
    # Outer decorative frame
    p1.draw_rect(fitz.Rect(40, 40, width - 40, height - 40), color=card_bg, fill=card_bg)
    p1.draw_line(fitz.Point(40, 40), fitz.Point(width - 40, 40), color=border_cyan, width=3)
    
    # Badge
    p1.draw_rect(fitz.Rect(60, 65, 340, 95), color=border_blue, fill=(30/255, 58/255, 138/255))
    p1.insert_text(fitz.Point(75, 84), "S&P GLOBAL & CRISIL CAMPUS HACKATHON 2026", fontsize=9, color=text_white, fontname="hebo")
    
    p1.insert_text(fitz.Point(60, 150), "AI/NLP Financial Risk Engine &", fontsize=28, color=text_white, fontname="hebo")
    p1.insert_text(fitz.Point(60, 190), "Strategic Portfolio Stress Testing", fontsize=28, color=border_cyan, fontname="hebo")
    p1.insert_text(fitz.Point(60, 225), "Module B: Autonomous Multi-Asset Crisis Simulation Engine", fontsize=14, color=text_muted, fontname="helv")
    
    p1.draw_line(fitz.Point(60, 245), fitz.Point(width - 60, 245), color=(30/255, 41/255, 59/255), width=1)
    
    # Candidate details card
    p1.draw_rect(fitz.Rect(60, 265, 460, 450), color=(30/255, 41/255, 59/255), fill=(15/255, 23/255, 42/255))
    p1.insert_text(fitz.Point(80, 295), "CANDIDATE INFORMATION", fontsize=10, color=border_cyan, fontname="hebo")
    p1.insert_text(fitz.Point(80, 325), "Candidate Name:", fontsize=11, color=text_muted, fontname="helv")
    p1.insert_text(fitz.Point(210, 325), "SHAIK JAHEER AHMED", fontsize=11, color=text_white, fontname="hebo")
    p1.insert_text(fitz.Point(80, 355), "College Email ID:", fontsize=11, color=text_muted, fontname="helv")
    p1.insert_text(fitz.Point(210, 355), "shaikjaheer.ahmed2023@vitstudent.ac.in", fontsize=10, color=text_white, fontname="helv")
    p1.insert_text(fitz.Point(80, 385), "College / Campus:", fontsize=11, color=text_muted, fontname="helv")
    p1.insert_text(fitz.Point(210, 385), "VELLORE INSTITUTE OF TECHNOLOGY CHENNAI", fontsize=10, color=text_white, fontname="hebo")
    p1.insert_text(fitz.Point(80, 415), "Track / Module:", fontsize=11, color=text_muted, fontname="helv")
    p1.insert_text(fitz.Point(210, 415), "MODULE B (Strategic Portfolio Stress Testing)", fontsize=10, color=border_green, fontname="hebo")

    # Key Highlights Card
    p1.draw_rect(fitz.Rect(490, 265, width - 60, 450), color=(30/255, 41/255, 59/255), fill=(15/255, 23/255, 42/255))
    p1.insert_text(fitz.Point(510, 295), "SYSTEM HIGHLIGHTS AT A GLANCE", fontsize=10, color=border_blue, fontname="hebo")
    p1.insert_text(fitz.Point(510, 325), "• FinBERT NLP: P(pos) - P(neg) Sentiment Scoring [-1.0 to +1.0]", fontsize=10, color=text_white, fontname="helv")
    p1.insert_text(fitz.Point(510, 355), "• 11-Category Financial Event Taxonomy & Calibrated Impact Scoring (1-10)", fontsize=10, color=text_white, fontname="helv")
    p1.insert_text(fitz.Point(510, 385), "• Multi-Asset Synthetic Portfolio (INR 100M: Equities, Bonds, Loans, Derivs)", fontsize=10, color=text_white, fontname="helv")
    p1.insert_text(fitz.Point(510, 415), "• Autonomous Stress Trigger on Severity > 7.0 with Predefined Asset Shocks", fontsize=10, color=text_white, fontname="helv")

    # ==================== SLIDE 2: PROBLEM & APPROACH ====================
    p2 = add_slide_base("Problem Statement & Solution Approach", 2)
    
    # Left Card: Problem
    p2.draw_rect(fitz.Rect(50, 95, 480, 480), color=(239/255, 68/255, 68/255, 0.4), fill=card_bg)
    p2.draw_rect(fitz.Rect(50, 95, 480, 130), fill=(185/255, 28/255, 28/255, 0.25))
    p2.insert_text(fitz.Point(65, 118), "THE BUSINESS PROBLEM", fontsize=12, color=(248/255, 113/255, 113/255), fontname="hebo")
    
    problem_points = [
        "Unstructured Financial Noise: Financial news and disclosures arrive at",
        "  unprecedented velocity across GDELT and NewsAPI feeds.",
        "Lagging Traditional Indicators: Standard financial ratios reflect past",
        "  performance rather than forward-looking black-swan risk events.",
        "Disconnected Stress Testing: Institutional risk models rarely link incoming",
        "  geopolitical or credit headlines to immediate multi-asset shocks.",
        "Need for Machine-Readable Signals: Financial analysts need quantified,",
        "  reproducible severity metrics and automated stress simulation."
    ]
    y = 155
    for line in problem_points:
        p2.insert_text(fitz.Point(65, y), line, fontsize=10, color=text_white, fontname="helv")
        y += 24

    # Right Card: Solution Approach
    p2.draw_rect(fitz.Rect(510, 95, width - 50, 480), color=(16/255, 185/255, 129/255, 0.4), fill=card_bg)
    p2.draw_rect(fitz.Rect(510, 95, width - 50, 130), fill=(4/255, 120/255, 87/255, 0.25))
    p2.insert_text(fitz.Point(525, 118), "OUR FIVE-PHASE SOLUTION APPROACH", fontsize=12, color=border_green, fontname="hebo")
    
    solution_points = [
        "Phase 1: Ingests & normalizes news from GDELT & NewsAPI with SHA-256",
        "  deduplication and entity-to-ticker mapping.",
        "Phase 2: Fine-tuned ProsusAI FinBERT delivers sentiment P(pos)-P(neg),",
        "  11-class event taxonomy, and calibrated 1-10 severity impact scoring.",
        "Phase 3: Integrates public market volatility (yfinance) across 10 benchmark",
        "  tickers and creates an INR 100M synthetic 4-tier portfolio.",
        "Phase 4 (Module B): Automates stress test execution when Impact > 7.0,",
        "  applying predefined shocks to Equities, Bonds, Loans, and Derivatives.",
        "Phase 5: Exposes machine-readable FastAPI REST endpoints & a glassmorphic",
        "  dashboard with interactive breaking-news stress simulation."
    ]
    y = 155
    for line in solution_points:
        p2.insert_text(fitz.Point(525, y), line, fontsize=10, color=text_white, fontname="helv")
        y += 23

    # ==================== SLIDE 3: SYSTEM DESIGN ====================
    p3 = add_slide_base("System Design & End-to-End Architecture", 3)
    
    boxes = [
        ("1. Data Ingestion", ["GDELT 2.0 DOC API", "NewsAPI v2 / Everything", "Local Sample News Dataset", "SHA-256 Deduplication", "ISO 8601 Timestamps"], border_blue),
        ("2. AI/NLP Risk Engine", ["ProsusAI FinBERT Model", "P(pos) - P(neg) Score [-1, +1]", "11-Category Taxonomy", "Calibrated Impact (1-10)", "Composite Confidence"], border_cyan),
        ("3. Risk Intelligence", ["10 Mega-Cap Equities", "yfinance 30-Day Volatility", "INR 100M Multi-Asset Basket", "Equities, Bonds, Loans, Derivs", "Shock Matrix Predefinition"], border_green),
        ("4. Module B Stress Test", ["Gating: Impact Score > 7.0", "Event-to-Shock Mapping", "Asset Haircut Simulations", "Pre vs Post Valuation Calc", "Loss % & Audit Logging"], border_red),
    ]
    
    x = 50
    for title, items, b_color in boxes:
        p3.draw_rect(fitz.Rect(x, 105, x + 205, 340), color=b_color, fill=card_bg)
        p3.draw_rect(fitz.Rect(x, 105, x + 205, 140), fill=(30/255, 41/255, 59/255))
        p3.insert_text(fitz.Point(x + 10, 127), title, fontsize=11, color=text_white, fontname="hebo")
        y = 165
        for itm in items:
            p3.insert_text(fitz.Point(x + 12, y), f"• {itm}", fontsize=9, color=text_white, fontname="helv")
            y += 24
        x += 220

    # Bottom Foundation Card
    p3.draw_rect(fitz.Rect(50, 360, width - 50, 480), color=(59/255, 130/255, 246/255, 0.4), fill=card_bg)
    p3.insert_text(fitz.Point(70, 385), "PERSISTENCE, REST APIS & PRESENTATION LAYER", fontsize=11, color=border_blue, fontname="hebo")
    p3.insert_text(fitz.Point(70, 412), "• SQLite Database (SQLAlchemy): 'articles', 'risk_signals', and 'stress_test_runs' tables provide full reproducibility & zero-setup portability.", fontsize=9, color=text_white, fontname="helv")
    p3.insert_text(fitz.Point(70, 434), "• FastAPI Web Server: 10 REST endpoints exposing machine-readable JSON signals, portfolio metrics, custom text analysis, and audit trails.", fontsize=9, color=text_white, fontname="helv")
    p3.insert_text(fitz.Point(70, 456), "• Glassmorphism Dashboard: Chart.js interactive charts, real-time stress testing triggers, and live jury custom headline simulator.", fontsize=9, color=text_white, fontname="helv")

    # ==================== SLIDE 4: IMPLEMENTATION HIGHLIGHTS ====================
    p4 = add_slide_base("Implementation Highlights & Key Tech Choices", 4)
    
    tech_cards = [
        ("FinBERT Sentiment Analysis", "Hugging Face / ProsusAI FinBERT", [
            "Trained specifically on financial text corpora (Financial PhraseBank).",
            "Formula: Sentiment = P(positive) - P(negative) bounded in [-1.0, +1.0].",
            "Captures financial nuances (e.g. 'unhedged default', 'margin calls').",
            "Resilient fallback ensures zero crashes during offline evaluation."
        ]),
        ("Calibrated Impact Scoring", "Domain-Specific Severity Formula", [
            "Calibrated scale from 1.0 to 10.0 reflecting systemic disruption potential.",
            "Base category weights: Market Crash (8.5), Bankruptcy (8.2), Geopolitics (7.6).",
            "Sentiment amplification: Negative sentiment increases downside shock severity.",
            "Explicit disclaimer: Scenario analysis metric, NOT a market prediction."
        ]),
        ("Module B Strategic Stress Testing", "Multi-Asset Scenario Engine", [
            "Triggered autonomously when AI Impact Score > 7.0 threshold.",
            "Synthetic Portfolio: Equities (₹40M), Bonds (₹25M), Loans (₹20M), Derivatives (₹15M).",
            "Applies distinct asset-class shock vectors (e.g. Crash: Eq -15%, Deriv -18%).",
            "Calculates pre/post valuations, rupee losses, and persists audit trail."
        ]),
        ("Production Architecture", "FastAPI + Pydantic + Pytest", [
            "Strict schema validation via Pydantic v2 BaseSettings and BaseModel.",
            "Comprehensive 28-test automated regression suite covering all 5 phases.",
            "One-command launcher (python run_app.py) with dual LIVE & DEMO modes.",
            "Self-contained zero-binary repository with complete public datasets."
        ])
    ]
    
    positions = [(50, 100), (510, 100), (50, 295), (510, 295)]
    for i, (title, badge, points) in enumerate(tech_cards):
        bx, by = positions[i]
        p4.draw_rect(fitz.Rect(bx, by, bx + 440, by + 180), color=(30/255, 41/255, 59/255), fill=card_bg)
        p4.draw_rect(fitz.Rect(bx, by, bx + 440, by + 34), fill=(30/255, 41/255, 59/255))
        p4.insert_text(fitz.Point(bx + 14, by + 22), title, fontsize=11, color=text_white, fontname="hebo")
        p4.insert_text(fitz.Point(bx + 260, by + 22), badge, fontsize=8, color=text_accent, fontname="helv")
        y = by + 54
        for pt in points:
            p4.insert_text(fitz.Point(bx + 16, y), f"• {pt}", fontsize=8.5, color=text_white, fontname="helv")
            y += 23

    # ==================== SLIDE 5: KEY RESULTS ====================
    p5 = add_slide_base("Key Results & Stress Testing Simulations", 5)
    
    # Table header
    p5.draw_rect(fitz.Rect(50, 100, width - 50, 130), fill=(30/255, 41/255, 59/255))
    headers = [("Event Type", 60), ("Headline Scenario", 170), ("FinBERT Sent.", 420), ("Impact", 530), ("Pre-Stress", 610), ("Post-Stress", 710), ("Simulated Loss", 820)]
    for h, x_pos in headers:
        p5.insert_text(fitz.Point(x_pos, 120), h, fontsize=9, color=border_cyan, fontname="hebo")
        
    table_rows = [
        ("MARKET_CRASH", "Algorithmic Cascade Flash Crash", "-0.85", "8.8 / 10", "₹100.0M", "₹89.05M", "-₹10.95M (-10.95%)", border_red),
        ("GEOPOLITICAL", "Taiwan Strait Semiconductor Blockade", "-0.75", "8.2 / 10", "₹100.0M", "₹92.35M", "-₹7.65M (-7.65%)", border_red),
        ("CREDIT_EVENT", "Commercial Real Estate Rating Downgrade", "-0.78", "7.9 / 10", "₹100.0M", "₹91.45M", "-₹8.55M (-8.55%)", border_red),
        ("BANKRUPTCY", "Fintech Credit Lender Chapter 11 Run", "-0.82", "8.1 / 10", "₹100.0M", "₹89.50M", "-₹10.50M (-10.50%)", border_red),
        ("REGULATORY", "Antitrust Mandatory Breakup Lawsuit", "-0.68", "7.5 / 10", "₹100.0M", "₹94.45M", "-₹5.55M (-5.55%)", border_red),
        ("EARNINGS", "Apple Record Enterprise Revenue Beat", "+0.65", "4.5 / 10", "₹100.0M", "₹100.0M", "₹0.0 (Monitoring)", border_green),
        ("PRODUCT_LAUNCH", "Tesla Autonomous Robotaxi Fleet Rollout", "+0.55", "4.0 / 10", "₹100.0M", "₹100.0M", "₹0.0 (Monitoring)", border_green)
    ]
    
    y = 152
    for event, desc, sent, imp, pre, post, loss, col in table_rows:
        p5.draw_rect(fitz.Rect(50, y - 14, width - 50, y + 14), fill=(18/255, 24/255, 38/255) if (y//30)%2==0 else (12/255, 17/255, 28/255))
        p5.insert_text(fitz.Point(60, y), event, fontsize=8, color=text_accent, fontname="hebo")
        p5.insert_text(fitz.Point(170, y), desc, fontsize=8, color=text_white, fontname="helv")
        p5.insert_text(fitz.Point(420, y), sent, fontsize=8, color=(248/255, 113/255, 113/255) if "-" in sent else border_green, fontname="hebo")
        p5.insert_text(fitz.Point(530, y), imp, fontsize=8, color=(248/255, 113/255, 113/255) if "8." in imp or "7." in imp else border_green, fontname="hebo")
        p5.insert_text(fitz.Point(610, y), pre, fontsize=8, color=text_white, fontname="helv")
        p5.insert_text(fitz.Point(710, y), post, fontsize=8, color=text_white, fontname="hebo")
        p5.insert_text(fitz.Point(820, y), loss, fontsize=8, color=col, fontname="hebo")
        y += 28

    # Bottom summary metric bar
    p5.draw_rect(fitz.Rect(50, 420, width - 50, 480), color=border_blue, fill=(15/255, 23/255, 42/255))
    p5.insert_text(fitz.Point(70, 442), "TESTING ACCURACY & VALIDATION METRICS", fontsize=10, color=border_cyan, fontname="hebo")
    p5.insert_text(fitz.Point(70, 464), "• 100% Test Suite Coverage across 28 automated tests (pytest). Zero unhandled runtime exceptions.", fontsize=8.5, color=text_white, fontname="helv")
    p5.insert_text(fitz.Point(520, 464), "• Deterministic, explainable trigger rule: Impact > 7.0 prevents false positive stress runs.", fontsize=8.5, color=text_white, fontname="helv")

    # ==================== SLIDE 6: DOMAIN IMPACT ====================
    p6 = add_slide_base("Domain Impact & Financial Relevance", 6)
    
    pillars = [
        ("Credit Risk Underwriting", border_cyan, [
            "Early Liquidity Run Warning: Identifies credit deterioration and margin call pressures before financial statements publish.",
            "Loan Portfolio Sensitivity: Enables syndication desks to assess asset write-downs on commercial facilities (₹20M exposure).",
            "Counterparty Contagion Mapping: Links regional banking stresses directly to derivative counterparty exposures."
        ]),
        ("Asset & Wealth Management", border_blue, [
            "Proactive Tail-Risk Hedging: Gives portfolio managers real-time visibility into post-shock valuations (up to -10.95% tail loss).",
            "Cross-Asset Stress Correlation: Moves beyond single-stock betas to systemic multi-asset impact across Equities, Bonds, and Derivatives.",
            "Explainable Decision Support: Every stress shock maintains documented simulation assumptions for investment committees."
        ]),
        ("Regulatory & Capital Adequacy", border_green, [
            "Autonomous Scenario Generation: Automates CCAR / Basel-style scenario construction from live geopolitical & economic bulletins.",
            "Audit Trail Compliance: Every evaluated headline records Run ID, pre/post valuations, and exact timestamps in SQLite.",
            "Interactive Jury Simulator: Allows chief risk officers to test 'What-If' scenarios instantaneously without manual recalculation."
        ])
    ]
    
    x = 50
    for title, b_col, points in pillars:
        p6.draw_rect(fitz.Rect(x, 105, x + 275, 465), color=b_col, fill=card_bg)
        p6.draw_rect(fitz.Rect(x, 105, x + 275, 145), fill=(30/255, 41/255, 59/255))
        p6.insert_text(fitz.Point(x + 14, 130), title, fontsize=11, color=text_white, fontname="hebo")
        y = 175
        for pt in points:
            # Word wrap simulation for bullet points
            words = pt.split(" ")
            line = ""
            for w in words:
                if len(line + " " + w) > 34:
                    p6.insert_text(fitz.Point(x + 14, y), line, fontsize=8.5, color=text_white, fontname="helv")
                    y += 16
                    line = "  " + w
                else:
                    line = line + (" " if line else "• ") + w
            if line:
                p6.insert_text(fitz.Point(x + 14, y), line, fontsize=8.5, color=text_white, fontname="helv")
                y += 24
        x += 295

    # ==================== SLIDE 7: LIMITATIONS & NEXT STEPS ====================
    p7 = add_slide_base("Assumptions, Limitations & Future Roadmap", 7)
    
    p7.draw_rect(fitz.Rect(50, 105, 480, 465), color=(245/255, 158/255, 11/255, 0.4), fill=card_bg)
    p7.draw_rect(fitz.Rect(50, 105, 480, 140), fill=(180/255, 83/255, 9/255, 0.25))
    p7.insert_text(fitz.Point(65, 128), "CURRENT ASSUMPTIONS & BOUNDARIES", fontsize=11, color=(251/255, 191/255, 36/255), fontname="hebo")
    
    limits = [
        "1. Simulation vs Prediction: Impact scores and stress tests represent",
        "   predefined scenario sensitivity shocks, NOT empirical forecasts.",
        "2. Public / Synthetic Data Only: Relies strictly on public news (GDELT, NewsAPI)",
        "   and synthetic asset portfolios (₹100M). Zero proprietary data used.",
        "3. Uniform Class Shocks: Asset classes experience uniform percentage shocks",
        "   rather than security-specific non-linear derivative greeks.",
        "4. GDELT Content Truncation: Live GDELT artlist queries provide titles",
        "   and domain snippets rather than full unpaywalled news text."
    ]
    y = 165
    for l in limits:
        p7.insert_text(fitz.Point(65, y), l, fontsize=9, color=text_white, fontname="helv")
        y += 24

    p7.draw_rect(fitz.Rect(510, 105, width - 50, 465), color=border_blue, fill=card_bg)
    p7.draw_rect(fitz.Rect(510, 105, width - 50, 140), fill=(30/255, 58/255, 138/255, 0.25))
    p7.insert_text(fitz.Point(525, 128), "FUTURE ENHANCEMENTS & ROADMAP", fontsize=11, color=border_cyan, fontname="hebo")
    
    roadmap = [
        "1. Real-Time WebSocket Streaming: Push instant alert notifications to trading",
        "   terminals when breaking events exceed Impact > 7.0 threshold.",
        "2. Non-Linear Derivatives Greeks: Incorporate Black-Scholes Delta, Gamma,",
        "   and Vega recalculations under market crash volatility spikes.",
        "3. Knowledge Graph Entity Linking: Connect global supply chain nodes (e.g.",
        "   TSMC to NVDA/AAPL) for cross-company cascade risk tracking.",
        "4. Historical Backtesting Engine: Validate predicted stress losses against",
        "   actual market drawdowns during 2020 COVID and 2008 Lehman events."
    ]
    y = 165
    for r in roadmap:
        p7.insert_text(fitz.Point(525, y), r, fontsize=9, color=text_white, fontname="helv")
        y += 24

    out_path = Path("docs/presentation.pdf")
    doc.save(str(out_path))
    doc.close()
    print(f"Presentation deck successfully compiled to {out_path}")

if __name__ == "__main__":
    create_presentation_deck()
