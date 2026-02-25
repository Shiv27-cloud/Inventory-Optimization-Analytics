# Supply Chain Diagnostics: Inventory Health & Risk Optimization
## Project Overview
This project provides a centralized data ecosystem for a high-volume UK online retailer processing over 500,000 annual transactions. By transitioning from static spreadsheets to an automated ETL pipeline, the analysis identifies hidden operational risks and capital inefficiencies that standard revenue reporting overlooks.

## The "Triple Threat" to Profitability
The system is designed to solve three critical business "pain points":


1. Capital Lock-up (Dead Stock): Identifies items unsold for 90+ days, quantifying frozen capital and warehouse inefficiency.
2. The "Toxic Asset" Blind Spot: Flags "Best Sellers" with Return Rates >10%, exposing defective products that erode margins.
3. Customer Concentration Risk: Highlights high-revenue items purchased by only 1-2 unique customers, indicating high vulnerability to demand collapse

## Technical Architecture
The solution utilizes a modern data stack to move the business from reactive reporting to proactive optimization:


Storage (MariaDB SQL): Serves as the "Single Source of Truth," replacing disparate Excel files with a structured relational database.


Processing (Python/Pandas): An automated ETL script that cleans raw transaction logs, calculates complex ratios, and performs statistical ABC Segmentation.



Visualization (Power BI): An interactive dashboard allowing stakeholders to filter inventory by Risk, Quality, and Value dimensions.

## The analysis aims to answer the following questions:
Which 20% of items generate 80% of total revenue?(Using Pareto Principle) 

	
What should we liquidate immediately to free up cash? (By creating dead stock flags)


Which items have technical defects or misleading descriptions?(By analysing return rates) 

	
Are we relying on too few customers for this product's success?(Ensuring stability in customer concentration)
