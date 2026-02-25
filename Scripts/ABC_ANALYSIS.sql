-- Inventory Segmentation & Value (ABC Analysis)

-- These metrics quantify the financial and physical composition of your inventory.



-- total unique products in inventory list
SELECT COUNT(DISTINCT product_id) FROM inventory_analytics; 						-- 3,811

-- total revenue
SELECT SUM(total_revenue) FROM inventory_analytics;									-- 10644578.42


-- count of class A products (high value)
SELECT COUNT(product_id) FROM inventory_analytics WHERE abc_category = "A";	-- 800

-- revenue from class A products
SELECT SUM(total_revenue) FROM inventory_analytics WHERE abc_category = "A";	-- 8514557.48



-- Average revenue per Class A item
SELECT product_id, AVG(total_revenue) as avg_revenue									-- 10,643.19
FROM inventory_analytics WHERE abc_category = "A"; 
													 
													 
													 
-- Count of Class C Products
SELECT COUNT(DISTINCT product_id) FROM inventory_analytics							-- 2,106
WHERE abc_category = "C"; 
 
 

-- Dead Stock Count
SELECT COUNT(DISTINCT product_id) FROM inventory_analytics 							-- 613
WHERE is_dead_stock = 1; 


-- Total Value of Dead Stock 
SELECT SUM(total_revenue) FROM inventory_analytics										-- 67824.19
WHERE is_dead_stock = 1;	
 
 
 
 -- Top 10 products ranked by revenue
SELECT product_id, total_revenue, DESCRIPTION FROM  inventory_analytics			-- ranked
ORDER BY total_revenue DESC LIMIT 10;
 
 													 
-- Count of Active Products
SELECT COUNT(*) FROM inventory_analytics WHERE is_dead_stock = 0;					-- 3300	


												 