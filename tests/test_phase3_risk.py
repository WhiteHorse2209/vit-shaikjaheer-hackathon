import pytest
from src.risk.portfolio import PortfolioManager
from src.risk.scenario_loader import ScenarioLoader
from src.risk.market_data import MarketDataProvider, TRACKED_TICKERS

def test_portfolio_structure_and_valuation():
    pm = PortfolioManager()
    total_val = pm.get_total_value()
    assert total_val == 100_000_000.0, f"Expected 100M INR, got {total_val}"
    
    breakdown = pm.get_asset_class_breakdown()
    assert "Equities" in breakdown
    assert "Bonds" in breakdown
    assert "Loans" in breakdown
    assert "Derivatives" in breakdown
    
    assert breakdown["Equities"]["base_value"] == 40_000_000.0
    assert breakdown["Bonds"]["base_value"] == 25_000_000.0
    assert breakdown["Loans"]["base_value"] == 20_000_000.0
    assert breakdown["Derivatives"]["base_value"] == 15_000_000.0

def test_scenario_loader():
    loader = ScenarioLoader()
    
    # Test Geopolitical scenario with impact > 7
    geo_scen = loader.get_scenario("GEOPOLITICAL", 8.2)
    assert geo_scen is not None
    assert geo_scen["shocks"]["Equities"] == -10.0
    assert geo_scen["shocks"]["Bonds"] == -5.0
    assert geo_scen["shocks"]["Loans"] == -3.0
    assert geo_scen["shocks"]["Derivatives"] == -12.0
    
    # Test sub-threshold scenario (impact <= 7.0 should NOT trigger)
    low_scen = loader.get_scenario("GEOPOLITICAL", 6.5)
    assert low_scen is None

def test_market_data_tracked_universe():
    provider = MarketDataProvider()
    all_metrics = provider.get_all_tracked_metrics(use_live=False)
    assert len(all_metrics) == 10
    
    tickers = [m["ticker"] for m in all_metrics]
    for t in TRACKED_TICKERS:
        assert t in tickers
        
    nvda = provider.get_ticker_metrics("NVDA")
    assert nvda["ticker"] == "NVDA"
    assert nvda["current_price"] > 0
    assert nvda["annualized_volatility_pct"] > 0

def test_stress_shock_math():
    pm = PortfolioManager()
    # Shocks: Eq -10%, Bond -5%, Loan -3%, Deriv -12%
    shocks = {
        "Equities": -10.0,
        "Bonds": -5.0,
        "Loans": -3.0,
        "Derivatives": -12.0
    }
    result = pm.simulate_stress_shock(shocks)
    
    assert result["portfolio_before"] == 100_000_000.0
    assert result["simulated_loss"] == 7_650_000.0
    assert result["portfolio_after"] == 92_350_000.0
    assert result["loss_pct"] == 7.65
