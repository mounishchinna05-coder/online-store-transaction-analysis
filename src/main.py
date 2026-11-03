import json
from pathlib import Path
from config import get_engine
from data_access import load_data
from analysis import build_reports
from visualizations import create_charts

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "outputs" / "reports"
CHARTS = ROOT / "outputs" / "charts"

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    engine = get_engine()
    try:
        orders, items = load_data(engine)
    finally:
        engine.dispose()
    reports = build_reports(orders, items)
    for name, data in reports.items():
        if name != "stats":
            data.to_csv(REPORTS / f"{name}.csv", index=False)
    (REPORTS / "transaction_metrics.json").write_text(
        json.dumps(reports["stats"], indent=2), encoding="utf-8")
    create_charts(reports, CHARTS)
    print("Transaction summary:")
    for key, value in reports["stats"].items():
        print(f"{key}: {value}")
    print(f"Reports: {REPORTS}")
    print(f"Charts: {CHARTS}")

if __name__ == "__main__":
    main()
