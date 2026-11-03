from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def save_bar(labels, values, title, xlabel, ylabel, path, rotate=0):
    if len(labels) == 0:
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=rotate)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

def create_charts(reports, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    p = reports["payment_report"]
    save_bar(p["payment_method"].astype(str).tolist(), p["order_count"].tolist(),
             "Orders by Payment Method", "Payment method", "Orders", out/"payment_method_distribution.png")
    s = reports["status_report"]
    save_bar(s["order_status"].astype(str).tolist(), s["order_count"].tolist(),
             "Order Status Distribution", "Status", "Orders", out/"order_status_distribution.png")
    d = reports["daily_orders"]
    save_bar(d["day"].astype(str).tolist(), d["order_count"].tolist(),
             "Daily Order Volume", "Date", "Orders", out/"daily_order_volume.png", 45)
    m = reports["monthly_orders"]
    save_bar(m["month"].astype(str).tolist(), m["order_count"].tolist(),
             "Monthly Order Volume", "Month", "Orders", out/"monthly_order_volume.png", 45)
    products = reports["product_units"].head(15)
    save_bar(products["product_name"].astype(str).tolist(), products["units_sold"].tolist(),
             "Top Products by Units Sold (Completed Orders)", "Product", "Units sold",
             out/"product_units_sold.png", 45)
