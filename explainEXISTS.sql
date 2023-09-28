EXPLAIN ANALYZE
SELECT DISTINCT username
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.user_id
);