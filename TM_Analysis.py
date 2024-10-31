import pandas as pd
## Load data
sales = pd.read_csv('Sales.csv')
products = pd.read_csv('Products.csv')
customers = pd.read_csv('Customers.csv')

# 1 Customer Analysis
# 1.1  finding customer average age for each category
merged_data = sales.merge(products, on='product_id').merge(customers, on='customer_id')
avg_age_by_category = merged_data.groupby('category')['age'].mean()
print(avg_age_by_category)
###########################################################################################
#1.2 Customer retention Multiple Purchase and Single Purchase
# Count purchases per customer
purchase_counts = sales.groupby("customer_id").size()

# Classify and count
retention_summary = purchase_counts.apply(lambda x: "single_order" if x == 1 else "multiple_Orders").value_counts()
print(retention_summary)

##########################################################################################
#1.3 Identifying day difference from signup date to first purchase date.
# Converting dates to pandas datetime format
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
sales["date"] = pd.to_datetime(sales["date"])

# Find first purchase date per customer
first_purchase_date = sales.groupby("customer_id")["date"].min().reset_index()
first_purchase_date.columns = ["customer_id", "first_purchase_date"]

# Merge customers with first_purchase_date on 'customer_id'
merged_df = pd.merge(customers, first_purchase_date, on="customer_id", how="left")

# Calculate the difference in days between signup_date and first_purchase_date
merged_df["days_to_first_purchase"] = (merged_df["first_purchase_date"] - merged_df["signup_date"]).dt.days

# Drop rows where the difference is NaN (for customers with no purchase) if needed
merged_df = merged_df.dropna(subset=["days_to_first_purchase"])

# Display customer_id and days_to_first_purchase for clarity
result_df = merged_df[["customer_id", "days_to_first_purchase"]]
print("\nTime to First Purchase (Days) per Customer:")
print(result_df.head())
# Calculate the average time to first purchase
average_time_to_first_purchase = result_df["days_to_first_purchase"].mean()
print("\nAverage_First Purchase (in Days):", average_time_to_first_purchase)
##########################################################################################

#2 Product performance analysis
#2.1 Average Monthly revenue per product 
# First lets convert the 'date' column to datetime format
sales["date"] = pd.to_datetime(sales["date"])
# Add month column to group by product and month
sales["sale_month"] = sales["date"].dt.to_period("M")

# Calculate monthly revenue per product
sales["monthly_revenue"] = (sales["quantity"] * sales["unit_price"]).round(2)

# Group by product_id and sale_month to get total monthly revenue
monthly_sales = (
    sales.groupby(["product_id", "sale_month"])["monthly_revenue"].sum().reset_index()
)
# Calculate average monthly revenue per product
avg_monthly_revenue = (
    monthly_sales.groupby("product_id")["monthly_revenue"]
    .mean()
    .reset_index()
)
#Round the average revenue to 2 decimal places
avg_monthly_revenue["avg_monthly_revenue"] = avg_monthly_revenue["monthly_revenue"].round(2)
# Final Output
avg_monthly_revenue = avg_monthly_revenue[["product_id", "avg_monthly_revenue"]]
print(avg_monthly_revenue)
#####################################################################################################
## 2.2 Identify products with declining sales by comparing revenue over the last two quarters:
# Convert the 'date' column to datetime format
sales["date"] = pd.to_datetime(sales["date"])
# Add quarter column to group by product and quarter
sales["quarter"] = sales["date"].dt.to_period("Q").astype(str)  # Convert to string for easier display
# Calculate total revenue per product per quarter
quarterly_sales = (
    sales.groupby(["product_id", "quarter"])["quantity", "unit_price"]
    .apply(lambda x: (x["quantity"] * x["unit_price"]).sum()).reset_index(name="revenue"))
# Lag previous quarter revenue
quarterly_sales["previous_quarter_revenue"] = (
    quarterly_sales.groupby("product_id")["revenue"].shift(1))
# Filter products with declining sales
declining_sales = quarterly_sales[
    quarterly_sales["previous_quarter_revenue"] > quarterly_sales["revenue"]]
# Step 5: Round the revenue values
declining_sales["last_quarter_revenue"] = declining_sales["revenue"].round(2)
declining_sales["previous_quarter_revenue"] = declining_sales["previous_quarter_revenue"].round(2)

# Final Output
result_df = declining_sales[["product_id", "last_quarter_revenue", "previous_quarter_revenue"]]
print(result_df)
#############################################################################################################

# 2.3 Most popular brad by revenue
# Merge sales and products DataFrames
merged_data = pd.merge(sales, products, on='product_id')
#Calculate total revenue for each sale
merged_data['total_revenue'] = merged_data['quantity'] * merged_data['unit_price']

# Group by category and brand, summing total revenue
popular_brands = (
    merged_data.groupby(['category', 'brand'])['total_revenue'].sum().reset_index())
# Round total revenue to 2 decimal places
popular_brands['total_revenue'] = popular_brands['total_revenue'].round(2)

# Sort by total revenue in descending order
popular_brands = popular_brands.sort_values(by='total_revenue', ascending=False)
# Final Output
print(popular_brands)













