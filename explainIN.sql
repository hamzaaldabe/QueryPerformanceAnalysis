EXPLAIN ANALYZE
SELECT DISTINCT username
FROM users
WHERE user_id IN (
    SELECT DISTINCT user_id
    FROM orders
);