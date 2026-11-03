from pathlib import Path
import sys
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from config import get_engine

PRODUCTS = [
    ("Wireless Mouse","Electronics",799.00), ("USB-C Cable","Electronics",299.00),
    ("Notebook","Stationery",99.00), ("Water Bottle","Lifestyle",349.00),
    ("Desk Lamp","Home",1299.00),
]
ORDERS = [
    ("2026-01-03 10:15:00","UPI","COMPLETED"), ("2026-01-04 12:30:00","CARD","COMPLETED"),
    ("2026-01-05 17:40:00","CASH","CANCELLED"), ("2026-02-02 09:05:00","UPI","COMPLETED"),
    ("2026-02-14 20:10:00","WALLET","REFUNDED"), ("2026-03-01 14:25:00","NET_BANKING","PENDING"),
    ("2026-03-09 18:00:00","CARD","COMPLETED"), ("2026-03-19 11:45:00","UPI","COMPLETED"),
    ("2026-04-07 16:20:00","CARD","COMPLETED"), ("2026-04-21 13:15:00","WALLET","COMPLETED"),
    ("2026-05-02 19:35:00","UPI","CANCELLED"), ("2026-05-18 08:50:00","CASH","COMPLETED"),
]
# (order_id, product_id, quantity, unit_price-at-sale)
ITEMS = [
    (1,1,1,799.00),(1,2,2,299.00),(2,3,5,99.00),(2,4,1,349.00),
    (3,1,1,799.00),(4,5,1,1299.00),(4,2,1,299.00),(5,4,2,349.00),
    (6,3,3,99.00),(7,1,2,799.00),(7,5,1,1299.00),(8,2,3,299.00),
    (8,3,2,99.00),(9,4,2,349.00),(9,1,1,799.00),(10,5,1,1299.00),
    (10,3,4,99.00),(11,2,1,299.00),(12,4,3,349.00),(12,3,2,99.00),
]

def main():
    engine = get_engine()
    with engine.begin() as conn:
        if conn.execute(text("SELECT COUNT(*) FROM products")).scalar_one() or conn.execute(text("SELECT COUNT(*) FROM orders")).scalar_one():
            raise RuntimeError("Sample loader expects empty tables. Do not run it twice without clearing demo data.")
        conn.execute(text("INSERT INTO products (product_name,category,unit_price) VALUES (:n,:c,:p)"),
                     [{"n":n,"c":c,"p":p} for n,c,p in PRODUCTS])
        conn.execute(text("INSERT INTO orders (order_date,payment_method,order_status) VALUES (:d,:p,:s)"),
                     [{"d":d,"p":p,"s":s} for d,p,s in ORDERS])
        conn.execute(text("INSERT INTO order_items (order_id,product_id,quantity,unit_price) VALUES (:o,:p,:q,:u)"),
                     [{"o":o,"p":p,"q":q,"u":u} for o,p,q,u in ITEMS])
    engine.dispose()
    print(f"Loaded {len(PRODUCTS)} products, {len(ORDERS)} orders, {len(ITEMS)} order items.")

if __name__ == "__main__":
    main()
