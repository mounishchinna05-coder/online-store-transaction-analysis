
import json
from pathlib import Path

import pandas as pd
import streamlit as st

# Project folders
BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"

st.set_page_config(
    page_title="Online Store Transaction Analysis",
    page_icon="🛒",
    layout="wide"
)

# Styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 Online Store Transaction Analysis")
st.caption("Sales, orders, payment methods and product performance")

# Load transaction metrics
metrics_file = REPORTS_DIR / "transaction_metrics.json"

metrics = {}

if metrics_file.exists():
    with open(metrics_file, "r", encoding="utf-8") as file:
        metrics = json.load(file)

def show_metric(label, key, prefix=""):
    value = metrics.get(key, "N/A")

    if isinstance(value, (int, float)):
        if key in ["completed_sales_value", "average_order_value"]:
            value = f"₹{value:,.2f}"
        elif key == "median_completed_order_value":
            value = f"₹{value:,.2f}"
        elif key == "std_completed_order_value":
            value = f"₹{value:,.2f}"
        else:
            value = f"{prefix}{value:,}"

    st.metric(label, value)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section",
    ["Dashboard", "Charts", "Reports"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Online Store Transaction Analysis")

if page == "Dashboard":

    st.subheader("Transaction Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric("Total Orders", "total_orders")

    with col2:
        show_metric("Completed Orders", "completed_orders")

    with col3:
        show_metric("Completed Sales", "completed_sales_value")

    with col4:
        show_metric("Average Order Value", "average_order_value")

    st.markdown("---")
    st.subheader("Order Status Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric("Cancelled Orders", "cancelled_orders")

    with col2:
        show_metric("Refunded Orders", "refunded_orders")

    with col3:
        show_metric("Pending Orders", "pending_orders")

    with col4:
        show_metric("Median Order Value", "median_completed_order_value")

    st.markdown("---")
    st.subheader("Transaction Analysis")

    col1, col2 = st.columns(2)

    with col1:
        show_metric(
            "Standard Deviation",
            "std_completed_order_value"
        )

    with col2:
        st.metric("Project Status", "Analysis Completed")

    st.info(
        "Sales metrics include completed orders only. "
        "Cancelled, refunded and pending orders are excluded "
        "from completed-sales calculations."
    )

elif page == "Charts":

    st.subheader("Data Visualization")

    charts = {
        "Daily Order Volume": "daily_order_volume.png",
        "Monthly Order Volume": "monthly_order_volume.png",
        "Order Status Distribution": "order_status_distribution.png",
        "Payment Method Distribution": "payment_method_distribution.png",
        "Product Units Sold": "product_units_sold.png"
    }

    for title, filename in charts.items():
        image_path = CHARTS_DIR / filename

        st.markdown(f"### {title}")

        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.warning(f"Chart not found: {filename}")

elif page == "Reports":

    st.subheader("Generated CSV Reports")

    report_files = sorted(REPORTS_DIR.glob("*.csv"))

    if report_files:

        selected_report = st.selectbox(
            "Select a report",
            [file.name for file in report_files]
        )

        report_path = REPORTS_DIR / selected_report

        df = pd.read_csv(report_path)

        st.markdown(f"### {selected_report}")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="Download CSV Report",
            data=report_path.read_bytes(),
            file_name=selected_report,
            mime="text/csv"
        )

    else:
        st.warning("No CSV reports found.")

    st.markdown("---")
    st.subheader("Transaction Metrics JSON")

    if metrics:
        st.json(metrics)
    else:
        st.warning("Transaction metrics file not found.")

st.markdown("---")
st.caption("Online Store Transaction Analysis | Python • Pandas • NumPy • MySQL • Matplotlib • Streamlit")
