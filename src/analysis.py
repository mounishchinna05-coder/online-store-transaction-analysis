import numpy as np
import pandas as pd

def build_reports(orders: pd.DataFrame, items: pd.DataFrame):
    # Only completed orders count as sales; other statuses remain in status/order reports.
    if orders.empty:
        raise ValueError("No orders found. Load data into MySQL before running analysis.")

    df = orders.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["order_value"] = pd.to_numeric(df["order_value"], errors="coerce").fillna(0)
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["day"] = df["order_date"].dt.strftime("%Y-%m-%d")
    completed = df[df["order_status"] == "COMPLETED"].copy()

    transaction = df[["order_id","order_date","payment_method","order_status","order_value"]].copy()
    transaction["order_value"] = transaction["order_value"].round(2)

    status = df.groupby("order_status").size().rename("order_count").reset_index()
    status["percentage"] = (status["order_count"] / len(df) * 100).round(2)
    status = status.sort_values("order_count", ascending=False)

    payment = df.groupby("payment_method").size().rename("order_count").reset_index()
    payment["percentage"] = (payment["order_count"] / len(df) * 100).round(2)
    payment = payment.sort_values("order_count", ascending=False)

    daily = df.groupby("day").size().rename("order_count").reset_index().sort_values("day")
    monthly = df.groupby("month").size().rename("order_count").reset_index().sort_values("month")

    if items.empty:
        products = pd.DataFrame(columns=["product_name", "units_sold"])
    else:
        completed_items = items[items["order_status"] == "COMPLETED"]
        products = (completed_items.groupby("product_name")["quantity"].sum()
                    .rename("units_sold").reset_index()
                    .sort_values("units_sold", ascending=False))

    values = completed["order_value"].to_numpy(dtype=float)
    stats = {
        "total_orders": int(len(df)),
        "completed_orders": int(len(completed)),
        "completed_sales_value": round(float(completed["order_value"].sum()), 2),
        "average_order_value": round(float(completed["order_value"].mean()), 2) if len(completed) else 0.0,
        "median_completed_order_value": round(float(np.median(values)), 2) if len(values) else 0.0,
        "std_completed_order_value": round(float(np.std(values)), 2) if len(values) else 0.0,
        "cancelled_orders": int((df["order_status"] == "CANCELLED").sum()),
        "refunded_orders": int((df["order_status"] == "REFUNDED").sum()),
        "pending_orders": int((df["order_status"] == "PENDING").sum()),
    }
    return {"transaction_summary": transaction, "status_report": status,
            "payment_report": payment, "daily_orders": daily,
            "monthly_orders": monthly, "product_units": products, "stats": stats}
