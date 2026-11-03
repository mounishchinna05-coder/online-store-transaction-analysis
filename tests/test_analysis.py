import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analysis import build_reports

def test_status_rules_and_average_order_value():
    orders = pd.DataFrame([
        {"order_id":1,"order_date":"2026-01-01","payment_method":"UPI","order_status":"COMPLETED","order_value":100},
        {"order_id":2,"order_date":"2026-01-02","payment_method":"CARD","order_status":"CANCELLED","order_value":500},
        {"order_id":3,"order_date":"2026-01-03","payment_method":"UPI","order_status":"COMPLETED","order_value":300},
        {"order_id":4,"order_date":"2026-02-01","payment_method":"CASH","order_status":"REFUNDED","order_value":200},
    ])
    items = pd.DataFrame([
        {"order_id":1,"order_date":"2026-01-01","order_status":"COMPLETED","product_name":"Pen","quantity":2},
        {"order_id":2,"order_date":"2026-01-02","order_status":"CANCELLED","product_name":"Pen","quantity":9},
        {"order_id":3,"order_date":"2026-01-03","order_status":"COMPLETED","product_name":"Book","quantity":3},
    ])
    r = build_reports(orders, items)
    assert r["stats"]["total_orders"] == 4
    assert r["stats"]["completed_orders"] == 2
    assert r["stats"]["average_order_value"] == 200
    assert r["stats"]["completed_sales_value"] == 400
    assert dict(zip(r["product_units"]["product_name"], r["product_units"]["units_sold"])) == {"Book":3,"Pen":2}
