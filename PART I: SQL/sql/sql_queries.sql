-- 1. Top 5 customer areas with highest average delivery time in the last 30 days.
SELECT 
    customer_area,
    AVG(delivery_time_min) AS average_delivery_time_min
FROM 
    deliveries
WHERE 
    order_placed_at >= DATETIME('now', '-30 days')
GROUP BY 
    customer_area
ORDER BY 
    average_delivery_time_min DESC 
LIMIT 5;

-- 2. Average delivery time per traffic condition, by restaurant area and cuisine type.
--VER ESTO--------------------------------
SELECT
    d.traffic_condition,
    r.area AS restaurant_area,
    r.cuisine_type,
    AVG(d.delivery_time_min) AS average_delivery_time
FROM 
    deliveries AS d
JOIN 
    orders AS o ON d.delivery_id = o.delivery_id
JOIN 
    restaurants AS r ON o.restaurant_id = r.restaurant_id
GROUP BY 
    d.traffic_condition, 
    r.area, 
    r.cuisine_type
ORDER BY 
    d.traffic_condition, 
    r.area, 
    r.cuisine_type;


-- 3. Top 10 delivery people with the fastest average delivery time, considering only those with at least 50 deliveries and who are still active.
SELECT 
    dp.name,
    AVG(d.delivery_time_min) AS average_delivery_time
FROM 
    deliveries AS d
JOIN
    delivery_persons AS dp ON d.delivery_person_id = dp.delivery_person_id
WHERE
    dp.is_active = TRUE
GROUP BY 
    dp.name
HAVING
    COUNT(d.delivery_id) >= 50
ORDER BY 
    average_delivery_time ASC
LIMIT 10;




-- 4. The most profitable restaurant area in the last 3 months, defined as the area with the highest total order value.



-- 5. Identify whether any delivery people show an increasing trend in average delivery time.


