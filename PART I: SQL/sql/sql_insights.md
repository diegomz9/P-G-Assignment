1- How much do bad weather conditions impact on delivery times?
Calculate average delivery time for each weather condiction, it help us quantify the impact of the weather. 

SELECT 
    weather_condition, 
    COUNT(delivery_id) as total_deliveries, 
    AVG(delivery_time_min) as average_delivery_time
FROM
    deliveries
GROUP BY
    weather_condition
ORDER BY
    average_delivery_time DESC;

2- Was the delivery late or was the restaurant fault? 
Shows top 10 restaurants with the highest delivery time and the average preparation time. 

SELECT
    r.name AS restaurant_name,
    r.area AS restaurant_area,
    COUNT(d.delivery_id) AS total_deliveries,
    AVG(r.avg_preparation_time_min) AS avg_prep_time,
    AVG(d.delivery_time_min) AS average_total_delivery_time
FROM
    deliveries AS d
JOIN
    orders AS o ON d.delivery_id = o.delivery_id
JOIN
    restaurants AS r ON o.restaurant_id = r.restaurant_id
GROUP BY
    r.name, r.area
ORDER BY
    average_total_delivery_time DESC
LIMIT 10;

