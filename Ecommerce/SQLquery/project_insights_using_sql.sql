-------------------------------------
-- PROJECT -> 3 ANALYSIS USING SQL---
-------------------------------------

use projects;
select count(*) from data;


-- 1. Identify which customer states have the highest average delivery time and how many orders they handle.
SELECT customer_state,
ROUND(AVG(delivery_time),2) AS avg_delivery_days,
COUNT(*) AS total_orders
FROM data
GROUP BY customer_state
ORDER BY avg_delivery_days DESC;


-- 2. find top 5 product categories which generated the highest total revenue.
SELECT category,ROUND(SUM(total_payment),2) AS total_revenue
FROM data
GROUP BY category
ORDER BY total_revenue DESC LIMIT 5;


-- 3. Analyze the relationship between delivery time and customer ratings.
SELECT round(AVG(rating),2) AS avg_rating,
CASE
	WHEN delivery_time <= 5 THEN 'Fast (<=5 days)'
	WHEN delivery_time BETWEEN 6 AND 10 THEN 'Moderate (6-10 days)'
	ELSE 'Slow (>10 days)'
END AS delivery_speed
FROM data
GROUP BY delivery_speed
ORDER BY avg_rating DESC;


-- 4. Compare financial behaviour for different payment methods
SELECT payment_type,
ROUND(AVG(total_payment),2) AS avg_payment,
ROUND(AVG(total_installment),2) AS avg_installments,
COUNT(*) AS total_orders
FROM data
GROUP BY payment_type
ORDER BY avg_payment DESC;


-- 5. Which seller regions have the best average customer ratings.
SELECT seller_state,
ROUND(AVG(rating),2) AS avg_rating,
COUNT(*) AS total_orders
FROM data
GROUP BY seller_state
ORDER BY avg_rating DESC;


-- 6 Which product categories have the highest average rating and how many total orders do they have?
SELECT category,
ROUND(AVG(rating),2) AS avg_rating,
COUNT(*) AS total_orders
FROM data
GROUP BY category
ORDER BY avg_rating DESC LIMIT 5;


-- 7 Which states generate the highest total revenue and their average rating?
SELECT customer_state,
ROUND(SUM(total_payment),2) AS total_revenue,
ROUND(AVG(rating),2) AS avg_rating
FROM data
GROUP BY customer_state
ORDER BY total_revenue DESC LIMIT 10;


-- 8 find top 10 orders which have the longest delivery times and what were their payment types and total payments?
SELECT order_id, delivery_time, total_payment, payment_type,rating
FROM data
ORDER BY delivery_time DESC LIMIT 10;


-- 9 Which seller states handle the highest number of multi-item orders (more than 1 item in a single order)?
SELECT seller_state,
COUNT(*) AS total_multi_item_orders FROM data
WHERE items_in_order > 1
GROUP BY seller_state
ORDER BY total_multi_item_orders DESC;


-- 10️ Find top 5 product categories that have the highest revenue-to-delivery-charge ratio.
SELECT category,
ROUND(SUM(total_payment)/SUM(delivery_charge),2) AS revenue_per_charge_ratio
FROM data
WHERE delivery_charge > 0
GROUP BY category
ORDER BY revenue_per_charge_ratio DESC LIMIT 5;


-- 11️ Find the top 3 customer states that generate maximum average total payment per order.
SELECT customer_state,
ROUND(AVG(total_payment),2) AS avg_payment FROM data
GROUP BY customer_state
ORDER BY avg_payment DESC LIMIT 3;


-- 12 Identify product categories whose total revenue is higher than the average category revenue.
SELECT category, ROUND(SUM(total_payment),2) AS total_revenue
FROM data
GROUP BY category
HAVING SUM(total_payment) > (SELECT AVG(category_revenue) 
                             FROM (SELECT SUM(total_payment) AS category_revenue 
                                   FROM data 
                                   GROUP BY category) AS t)
ORDER BY total_revenue DESC;


-- 13️ Which product categories have the highest average delivery charges and average prices?
SELECT category,
ROUND(AVG(delivery_charge),2) AS avg_delivery_charge,
ROUND(AVG(price),2) AS avg_price
FROM data
GROUP BY category
ORDER BY avg_delivery_charge DESC LIMIT 10;


-- 14️ Analyze how the number of installments affects the average customer rating and average order value.
SELECT 
CASE 
	WHEN total_installment = 1 THEN 'one_time'
	WHEN total_installment BETWEEN 2 AND 5 THEN 'medium(2-5)'
	ELSE 'large(>5)'
END AS installments,
ROUND(AVG(rating),2) AS avg_rating,
ROUND(AVG(total_payment),2) AS avg_order_value,
COUNT(*) AS total_orders
FROM data
GROUP BY installments
ORDER BY avg_rating DESC;


-- 15️ Determine which seller states have the highest delivery cost per day of delivery, along with their average delivery time and average delivery charge.
SELECT seller_state,
ROUND(SUM(delivery_charge)/SUM(delivery_time),2) AS cost_per_day_of_delivery,
ROUND(AVG(delivery_time),2) AS avg_delivery_time,
ROUND(AVG(delivery_charge),2) AS avg_delivery_charge
FROM data
WHERE delivery_time > 0
GROUP BY seller_state
ORDER BY cost_per_day_of_delivery DESC;