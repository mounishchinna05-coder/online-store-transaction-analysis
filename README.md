# Online Store Transaction Analysis

Intermediate project: MySQL + Python + Pandas + NumPy + Matplotlib.

## Scope
Analyze order composition, transaction values, payment methods, order statuses, daily/monthly order volume, and product units sold. No customer segmentation or executive KPI dashboard.

## Business rules
- Order value = sum of `quantity * order_items.unit_price` for each order.
- Only `COMPLETED` orders count toward completed sales, average order value, and units sold.
- `CANCELLED`, `REFUNDED`, and `PENDING` orders remain in status/payment/order-volume reports but are excluded from completed-sales metrics.
- Store the order-item unit price at sale time; do not recalculate it from the current product price.

## Setup
1. Install Python 3.10+, MySQL 8+, and Git.
2. Create a virtual environment and run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`, then fill in your MySQL credentials.
4. Run `sql/schema.sql` in MySQL.
5. Run `python scripts/load_sample_data.py` to add synthetic demo data.
6. Run `python src/main.py`.
7. CSV reports appear in `outputs/reports/`; charts appear in `outputs/charts/`.

Sample data is synthetic. Use authorized real data for real conclusions.
