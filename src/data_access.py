import pandas as pd
from sqlalchemy import text

ORDER_QUERY = text('''
SELECT o.order_id, o.order_date, o.payment_method, o.order_status,
       COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS order_value
FROM orders o LEFT JOIN order_items oi ON oi.order_id=o.order_id
GROUP BY o.order_id, o.order_date, o.payment_method, o.order_status
ORDER BY o.order_date, o.order_id
''')

ITEM_QUERY = text('''
SELECT o.order_id, o.order_date, o.order_status, p.product_id,
       p.product_name, p.category, oi.quantity, oi.unit_price,
       oi.quantity * oi.unit_price AS line_value
FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
JOIN products p ON p.product_id=oi.product_id
ORDER BY o.order_date, o.order_id, oi.item_id
''')

def load_data(engine):
    with engine.connect() as conn:
        orders = pd.read_sql(ORDER_QUERY, conn)
        items = pd.read_sql(ITEM_QUERY, conn)
    if not orders.empty:
        orders["order_date"] = pd.to_datetime(orders["order_date"])
        orders["order_value"] = pd.to_numeric(orders["order_value"])
    if not items.empty:
        items["order_date"] = pd.to_datetime(items["order_date"])
        items["line_value"] = pd.to_numeric(items["line_value"])
    return orders, items
