import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram():
    # 1600 x 950 High-Resolution Canvas
    width, height = 1600, 950
    img = Image.new("RGBA", (width, height), (9, 13, 22, 255))
    draw = ImageDraw.Draw(img)

    # Gradient-like background accents
    for i in range(200):
        alpha = int(25 * (1 - i / 200))
        draw.ellipse([width//2 - 400 - i, 200 - i, width//2 + 400 + i, 600 + i], fill=(15, 23, 42, alpha))

    # Try loading clean font, fallback to default
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 34)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_box_title = ImageFont.truetype("arialbd.ttf", 19)
        font_text = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_box_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    # Main Header
    draw.text((width // 2, 45), "AI/NLP FINANCIAL RISK ENGINE & STRATEGIC STRESS TESTING", font=font_title, fill=(241, 245, 249), anchor="mm")
    draw.text((width // 2, 85), "S&P Global & CRISIL Campus Hackathon 2026 | Candidate: SHAIK JAHEER AHMED (VIT Chennai) | Module B", font=font_sub, fill=(59, 130, 246), anchor="mm")

    # Helper function to draw rounded container cards
    def draw_card(x1, y1, x2, y2, title, subtitle, items, border_color=(59, 130, 246, 120), fill_color=(18, 24, 38, 230), tag=""):
        # Card background & border
        draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=fill_color, outline=border_color, width=2)
        # Header banner inside card
        draw.rounded_rectangle([x1, y1, x2, y1 + 42], radius=10, fill=(30, 41, 59, 180))
        draw.text((x1 + 16, y1 + 21), title, font=font_box_title, fill=(248, 250, 252), anchor="lm")
        if tag:
            draw.rounded_rectangle([x2 - 110, y1 + 10, x2 - 14, y1 + 32], radius=6, fill=(37, 99, 235, 200))
            draw.text((x2 - 62, y1 + 21), tag, font=font_text, fill=(255, 255, 255), anchor="mm")
            
        cur_y = y1 + 56
        if subtitle:
            draw.text((x1 + 16, cur_y), subtitle, font=font_bold, fill=(148, 163, 184))
            cur_y += 24
            
        for itm in items:
            draw.text((x1 + 20, cur_y), f"• {itm}", font=font_text, fill=(203, 213, 225))
            cur_y += 22

    # Draw Connecting Arrows
    def draw_arrow(x1, y1, x2, y2, color=(59, 130, 246, 220), label=""):
        draw.line([x1, y1, x2, y2], fill=color, width=3)
        # Arrowhead pointing right or down
        if x2 > x1 and y1 == y2:
            draw.polygon([(x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)], fill=color)
        elif y2 > y1 and x1 == x2:
            draw.polygon([(x2, y2), (x2 - 6, y2 - 10), (x2 + 6, y2 - 10)], fill=color)
        if label:
            draw.text(((x1 + x2)//2, (y1 + y2)//2 - 12), label, font=font_text, fill=(56, 189, 248), anchor="mm")

    # Column 1: Phase 1 Data Ingestion
    draw_card(60, 130, 360, 480, "PHASE 1: Ingestion", "Multi-Source Intake & Clean", [
        "GDELT 2.0 DOC API (Global Feed)",
        "NewsAPI v2 (Top Financial Desk)",
        "Local Demo Feed (/data/sample_news.json)",
        "Cleaning: HTML & Entities Stripped",
        "Deduplication: SHA-256 Fingerprint",
        "Timestamp Standard: ISO 8601 UTC",
        "Company-to-Ticker Extractor",
        "Dual Mode: LIVE & DEMO fallback",
        "SQLite Persistence: 'articles' table"
    ], border_color=(37, 99, 235, 180), tag="INPUT")

    # Column 2: Phase 2 AI/NLP Risk Engine
    draw_card(420, 130, 780, 480, "PHASE 2: AI/NLP Engine", "Financial Risk Signal Extraction", [
        "ProsusAI / FinBERT Sentiment Model",
        "Score: P(positive) - P(negative) [-1.0, +1.0]",
        "Event Taxonomy Classifier (11 Categories):",
        "  - Geopolitical, Macroeconomic, Crash",
        "  - Credit Event, Bankruptcy, Regulatory",
        "  - Interest Rate, Earnings, M&A, Launch",
        "Calibrated Impact Scorer (1.0 to 10.0)",
        "Composite Confidence Metric [0.0 - 1.0]",
        "JSON & SQLite: 'risk_signals' table"
    ], border_color=(6, 182, 212, 180), tag="CORE NLP")

    # Column 3: Phase 3 Financial Intelligence
    draw_card(840, 130, 1200, 480, "PHASE 3: Risk Intelligence", "Portfolio & Market Analytics", [
        "10 Tracked Mega-Cap Stocks (AAPL..NFLX)",
        "yfinance Integration & Volatility Engine",
        "Offline Market Cache (/data/market_cache.json)",
        "Synthetic Portfolio Total: INR 100M",
        "  - Equities: INR 40M (40%)",
        "  - Bonds: INR 25M (25%)",
        "  - Loans: INR 20M (20%)",
        "  - Derivatives: INR 15M (15%)",
        "Scenario Shock Rules (/data/stress_scenarios.csv)"
    ], border_color=(16, 185, 129, 180), tag="PORTFOLIO")

    # Column 4: Phase 4 Strategic Stress Testing (Module B)
    draw_card(1260, 130, 1540, 480, "PHASE 4: Module B Stress", "Dynamic Scenario Simulation", [
        "Severity Gating: Impact > 7.0 Trigger",
        "Event-Type to Shock Vector Mapping",
        "Predefined Asset-Level Haircuts:",
        "  - Market Crash: Eq -15%, Deriv -18%",
        "  - Geopolitical: Eq -10%, Deriv -12%",
        "  - Credit Event: Eq -8%, Loan -10%",
        "Calculates Valuation Before & After",
        "Computes Simulated Loss & Loss %",
        "Audit Trail: 'stress_test_runs' table"
    ], border_color=(239, 68, 68, 180), tag="MODULE B")

    # Connecting horizontal arrows across top layer
    draw_arrow(360, 300, 420, 300, label="Normalized")
    draw_arrow(780, 300, 840, 300, label="Signals")
    draw_arrow(1200, 300, 1260, 300, label="Trigger >7.0")

    # Bottom Row: API, Database, and Modern Dashboard (Phase 5)
    draw_card(60, 540, 680, 880, "PHASE 5A: FastAPI REST Engine & SQLite Storage", "Exposing Machine-Readable Risk Signals", [
        "GET  /health            -> System Status, Active Mode & Model Status",
        "POST /api/ingest        -> Ingests Live or Demo Articles",
        "POST /api/nlp/process   -> Generates FinBERT Sentiment & Impact Scores",
        "POST /api/nlp/analyze-text -> Live Headline Scoring for Jury Demo",
        "GET  /api/portfolio     -> 100M Synthetic Multi-Asset Allocation",
        "GET  /api/market-data   -> 10 Tracked Companies Historical Metrics",
        "POST /api/stress-test/evaluate-all -> Triggers Asset Shocks on Impact > 7",
        "GET  /api/stress-test/history      -> Full Simulation Audit Trail",
        "Database: SQLite Engine (risk_engine.db) with SQLAlchemy Models"
    ], border_color=(139, 92, 246, 180), tag="REST API")

    draw_card(740, 540, 1540, 880, "PHASE 5B: Interactive Glassmorphism Dashboard", "Single-Pane Financial Risk Intelligence UI", [
        "Top Summary Cards: Base Portfolio Value (INR 100M) vs Post-Stress Valuation & Loss",
        "Chart.js Visualizations: Portfolio Asset Doughnut & Asset-Level Stress Shock Comparison",
        "Interactive Breaking News Simulator: Custom Headline FinBERT Scoring & Instant Stress Trigger",
        "Risk Signals Stream Table: Real-Time Sentiment (-1 to +1), Event Category, Impact Score (1-10)",
        "Audit Trail Table: Detailed Historical Run Log with Loss %, Timestamps, and Scenario Assumptions",
        "Strict Regulatory Notice: Disclaiming Hackathon Simulation vs Empirical Market Prediction"
    ], border_color=(245, 158, 11, 180), tag="FRONTEND")

    # Downward connecting arrows
    draw_arrow(210, 480, 210, 540, label="Persist")
    draw_arrow(600, 480, 600, 540, label="Signals API")
    draw_arrow(1400, 480, 1400, 540, label="Stress Results")
    draw_arrow(680, 710, 740, 710, label="JSON Stream")

    # Bottom Footer
    draw.text((width // 2, 915), "S&P Global & CRISIL Campus Hackathon 2026 | Verified End-to-End Autonomous Implementation | MIT License", font=font_sub, fill=(100, 116, 139), anchor="mm")

    os.makedirs("docs", exist_ok=True)
    out_path = "docs/architecture.png"
    img.save(out_path, format="PNG")
    print(f"Architecture diagram generated successfully at {out_path}")

if __name__ == "__main__":
    create_architecture_diagram()
