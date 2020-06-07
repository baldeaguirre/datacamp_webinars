import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import the data
Url = 'https://github.com/adelnehme/python-for-excel-users-webinar/blob/master/sales_data_dirty.xlsx?raw=true'

def allSheets(Url):
    data = pd.ExcelFile(Url)
    sales = data.parse('sales')
    customers = data.parse('customers')
    dates = data.parse('dates')
    employees = data.parse('employees')
    # Drop status column from sales
    sales.drop('Status', axis=1, inplace=True)
    # Replace OnlineOrderFlag to offline and online
    sales['OnlineOrderFlag'] = sales['OnlineOrderFlag'].replace({0: "offline", 1: "online"})
    # Convert data columns to datetime while keeping only Y,m,d
    dates['OrderDate'] = pd.to_datetime(dates['OrderDate'], format='%Y-%m-%d')
    dates['ShipDate'] = pd.to_datetime(dates['ShipDate'], format='%Y-%m-%d')
    # Impute missing values based on key business assumptions
    customers.loc[customers['EmployeeFirstName'].isnull(), 'ChannelType'] = "B2C"
    customers.loc[customers['EmployeeFirstName'].notnull(), 'ChannelType'] = "B2B"
    # Combine first and last name in customers
    customers['EmployeeFullName'] = customers['EmployeeFirstName'] + ' ' + customers['EmployeeLastName']
    # Combine first and last name in employees
    employees['EmployeeFullName'] = employees['FirstName'] + ' ' + employees['LastName']
    return sales, customers, dates, employees

def revenue(sales):
    # Merge data - the VLOOKUP of Excel
    sales_date = sales.merge(dates, on="SalesOrderID", how="left")
    # Create column for year and month
    sales_date['Order_Year'] = sales_date['OrderDate'].dt.year
    sales_date['Order_YM'] = sales_date['OrderDate'].dt.strftime('%Y-%m')
    # Extract revenue by year
    sales_by_year = sales_date.groupby('Order_Year').sum().reset_index()
    # Visualize it
    sns.barplot(x='Order_Year', y='TotalDue', data=sales_by_year)
    plt.xlabel("Years")
    plt.ylabel("Revenue")
    plt.title("Revenue over the years")
    # Is there seasonality?
    sales_by_year_month = sales_date.groupby('Order_YM').sum().reset_index()
    # Visualize it
    plt.figure(figsize=(18, 6))
    sns.lineplot(x='Order_YM', y='TotalDue', data=sales_by_year_month)
    plt.xticks(rotation=45)
    plt.xlabel("Years")
    plt.ylabel("Revenue")
    plt.title("Revenue over the years")
    plt.show()

def split_revenue(sales):
    # Merge sales and customer data
    sales_customers = sales.merge(customers, on="SalesOrderID", how="left")
    # Identify revenue and amount sold by channel
    sales_by_channel = sales_customers.groupby('ChannelType').sum().reset_index()
    # Visualize
    sns.barplot(x='ChannelType', y='TotalDue', data=sales_by_channel)
    plt.xlabel("Channel Type")
    plt.ylabel("Revenue")
    plt.title("Revenue by Channel Type")
    plt.show()
    sales_date = sales.merge(dates, on="SalesOrderID", how="left")
    # Create column for year
    sales_date['Order_Year'] = sales_date['OrderDate'].dt.year
    # Merge sales, dates and customers data
    sales_customers_date = sales_date.merge(customers, on="SalesOrderID", how="left")
    # Group by year by channel type
    sales_by_channel_date = sales_customers_date.groupby(['Order_Year', 'ChannelType']).sum().reset_index()
    # Visualize
    sns.barplot(x='Order_Year', y='TotalDue', hue="ChannelType", data=sales_by_channel_date)
    plt.xlabel("Channel Type")
    plt.ylabel("Revenue")
    plt.title("Revenue by Channel Type")
    plt.show()

def employees_sales(sales):
    # Merge sales and dates
    sales_date = sales.merge(dates, on="SalesOrderID", how="left")
    # Create column for year
    sales_date['Order_Year'] = sales_date['OrderDate'].dt.year
    # Merge sales, dates and customers data
    sales_customers_date = sales_date.merge(customers, on="SalesOrderID", how="left")
    # Group by employee performance
    sales_employees = sales_customers_date.groupby('EmployeeFullName').sum().reset_index()
    # Sort it so we visualize it correctly
    sales_employees.sort_values('TotalDue', ascending=True, inplace=True)
    # Visualize
    plt.figure(figsize=(18, 6))
    sns.barplot(x='EmployeeFullName', y='TotalDue', data=sales_employees)
    plt.xticks(rotation=45)
    plt.xlabel("Channel Type")
    plt.ylabel("Revenue")
    plt.title("B2B Revenue by Sales Person")
    plt.show()
    # Group by employee performance and year
    sales_employees = sales_customers_date.groupby(['EmployeeFullName', 'Order_Year']).sum().reset_index()
    # Sort to make it easier to visualize
    sales_employees.sort_values(['Order_Year', 'TotalDue'], ascending=True, inplace=True)
    # Who was the best last year?
    sales_employees_2013 = sales_employees[sales_employees['Order_Year'] == 2013]
    # Visualize
    plt.figure(figsize=(18, 6))
    sns.barplot(x='EmployeeFullName', y='TotalDue', data=sales_employees_2013)
    plt.xticks(rotation=45)
    plt.xlabel("Channel Type")
    plt.ylabel("Revenue")
    plt.title("B2B Revenue by Sales Person in 2013")
    plt.show()

def highest_earning_employee(sales, year):
    #Merge sales and dates
    sales_date = sales.merge(dates, on="SalesOrderID", how="left")
    # Create column for year
    sales_date['Order_Year'] = sales_date['OrderDate'].dt.year
    # Merge sales, dates and customers data
    sales_customers_date = sales_date.merge(customers, on="SalesOrderID", how="left")
    # Group by employee performance and year
    sales_employees = sales_customers_date.groupby(['EmployeeFullName', 'Order_Year']).sum().reset_index()
    # Sort to make it easier to visualize
    sales_employees.sort_values(['Order_Year', 'TotalDue'], ascending=True, inplace=True)
    # Filter sales_employees by year (2012)
    sales_employees_2012 = sales_employees[sales_employees['Order_Year'] == year]
    # Merge sales_employees_2012 and employees
    sales_employees_compensation = sales_employees_2012.merge(employees, on='EmployeeFullName', how='left')
    # Create column for compensation (totalDue * commissionPct)
    sales_employees_compensation['Compensation'] = sales_employees_compensation['TotalDue'] * sales_employees_compensation['CommissionPct']
    # Sort employees by highest earnings (compensation)
    sales_employees_compensation.sort_values('Compensation', ascending=True, inplace=True)
    # Visualize it
    plt.figure(figsize=(18, 6))
    sns.barplot(x='EmployeeFullName', y='Compensation', data=sales_employees_compensation)
    plt.xticks(rotation=45)
    plt.xlabel("Sales Person")
    plt.ylabel("Compensation")
    plt.title("Highest Earning Employee in " + str(year) + " (compensation)")
    plt.show()

sales, customers, dates, employees = allSheets(Url)
# Q1: How did we do in revenue over the years?
revenue(sales)
# Q2: How is revenue divided by channel type overall and over time?
split_revenue(sales)
# Q3: Who are the employees responsible for the most B2B sales overall and in 2013?
employees_sales(sales)
# Q4: Who were the highest earning (in compensation) employees in 2012?
highest_earning_employee(sales, year=2012)