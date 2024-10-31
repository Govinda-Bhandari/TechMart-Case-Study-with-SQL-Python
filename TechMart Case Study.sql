-- Identify the average age of customer for each category
SELECT 
  p.category, 
  AVG(c.age) AS avg_age
FROM TM_Sales s
JOIN TM_Products p ON s.product_id = p.product_id
JOIN TM_Customers c ON s.customer_id = c.customer_id
GROUP BY p.category;
--Analyze customer retention by calculating the number
--of customers who made multiple purchases versus single-purchase customers
SELECT 
    COUNT(DISTINCT CASE WHEN num_purchases = 1 
	THEN customer_id END) AS single_purchase_customers,
    COUNT(DISTINCT CASE WHEN num_purchases > 1 
	THEN customer_id END) AS multi_purchase_customers
FROM (
    SELECT customer_id, COUNT(*) AS num_purchases
    FROM TM_Sales
    GROUP BY customer_id
) AS purchase_counts;

--Average time between signup and purchase 
select customer_id, avg(dt) as Average_Signup_to_Purchase 
from
(select s.customer_id , datediff(day, c.signup_date,min(s.date)) as dt
FROM TM_Sales s
JOIN TM_Customers c ON s.customer_id = c.customer_id
group by s.customer_id,c.signup_date) query
group by customer_id
order by 2 


-- Product performance analysis
-- Average monthly revenue per product (last 6 months)
SELECT 
    product_id, 
    round(AVG(monthly_revenue),2) AS avg_monthly_revenue
FROM (
    SELECT 
        cast(product_id as int) as product_id, 
        month(date) AS sale_month, 
        round(SUM(quantity * unit_price),2) AS monthly_revenue,
		DATEADD(month, -6, max(date))as date
    FROM TM_Sales
    GROUP BY product_id, month(date)
) AS monthly_sales
GROUP BY product_id;

-- Products with declining sales (compare last two quarters)
WITH quarterly_sales AS (
    SELECT 
        cast(product_id as int) as product_id, 
        datepart(quarter,date) AS quarter, 
        SUM(quantity * unit_price) AS revenue
    FROM TM_Sales
    GROUP BY product_id, datepart(quarter,date)
)
SELECT * FROM (SELECT 
    product_id, 
    round(revenue,2) AS last_quarter_revenue,
    LAG(round(revenue,2)) OVER(PARTITION BY product_id ORDER BY quarter) 
	AS previous_quarter_revenue
FROM quarterly_sales) query
where previous_quarter_revenue > last_quarter_revenue;

-- Most popular brand by revenue in each category
SELECT 
    p.category,
    p.brand,
    round(SUM(s.quantity * s.unit_price),2) AS total_revenue
FROM TM_Sales s
JOIN TM_Products p ON s.product_id = p.product_id
GROUP BY p.category, p.brand
ORDER BY total_revenue DESC;
