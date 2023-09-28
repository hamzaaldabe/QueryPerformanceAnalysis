SELECT
    p.product_id,
    p.name AS product_name,
    COUNT(oi.order_id) AS order_count
FROM
    products p
JOIN
    order_items oi ON p.product_id = oi.product_id
GROUP BY
    p.product_id, p.name
ORDER BY
    order_count DESC;