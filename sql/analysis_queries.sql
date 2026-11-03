USE online_store;

-- Calculate each order total from its order items.
SELECT o.order_id, o.order_date, o.payment_method, o.order_status,
       COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS order_value
FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.order_date, o.payment_method, o.order_status
ORDER BY o.order_date;

SELECT order_status, COUNT(*) AS order_count
FROM orders GROUP BY order_status ORDER BY order_count DESC;

SELECT payment_method, COUNT(*) AS order_count
FROM orders GROUP BY payment_method ORDER BY order_count DESC;

SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS order_count
FROM orders GROUP BY DATE_FORMAT(order_date, '%Y-%m') ORDER BY month;

SELECT p.product_name, SUM(oi.quantity) AS units_sold
FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
JOIN products p ON p.product_id=oi.product_id
WHERE o.order_status='COMPLETED'
GROUP BY p.product_id,p.product_name ORDER BY units_sold DESC;
