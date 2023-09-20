

WITH ProductSales AS (
    SELECT
        p.product_id,
        p.name AS product_name,
        SUM(oi.quantity) AS total_quantity,
        SUM(oi.quantity * p.price) AS total_revenue,
        RANK() OVER (ORDER BY SUM(oi.quantity * p.price) DESC) AS sales_rank
    FROM
        products p
    JOIN
        order_items oi ON p.product_id = oi.product_id
    GROUP BY
        p.product_id, p.name
),
UserOrderStats AS (
    SELECT
        u.user_id,
        u.username,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity) AS total_items_ordered,
        SUM(oi.quantity * p.price) AS total_spent
    FROM
        users u
    LEFT JOIN
        orders o ON u.user_id = o.user_id
    LEFT JOIN
        order_items oi ON o.order_id = oi.order_id
    LEFT JOIN
        products p ON oi.product_id = p.product_id
    GROUP BY
        u.user_id, u.username
    HAVING
        COUNT(DISTINCT o.order_id) >= 5
),
TopCategories AS (
    SELECT
        c.category_id,
        c.category_name,
        COUNT(p.product_id) AS product_count
    FROM
        categories c
    LEFT JOIN
        products p ON c.category_id = p.category_id
    WHERE
        p.price >= 100
    GROUP BY
        c.category_id, c.category_name
    ORDER BY
        product_count DESC

)

SELECT
    ps.product_id,
    ps.product_name,
    ps.total_quantity,
    ps.total_revenue,
    ps.sales_rank,
    u.username,
    tc.category_name,
    tc.product_count
FROM
    ProductSales ps
JOIN
    users u ON ps.sales_rank % u.user_id = 0
JOIN
    TopCategories tc ON ps.product_id % tc.category_id = 0
WHERE
    ps.sales_rank <= 20
ORDER BY
    ps.sales_rank;
