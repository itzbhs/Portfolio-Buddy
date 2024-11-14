import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

today = date.today().strftime("%Y-%m-%d")
#Intro to program
print("Welcome to Portfolio Buddy!")
print("Portfolio Buddy is your quick and easy tool to check in on your portfolio progress overtime!")
print("The program lets you search up stock, include information about purchase quantity and price, \n and prepares a graph and chart to show you your overall portfolio performance!")
print("In addition, that information is saved in a CSV file with the date if you want to compile all the dates to get a sense \nof over time trends, or look back on your growth over time.")
# Prompt user input to build the portfolio dictionary
portfolio = {}
try:
    n = int(input("How many stocks are in your portfolio? "))
    if n <= 0:
        raise ValueError("Number of stocks must be a positive integer.")
except ValueError as e:
    print("Invalid input:", e)
    exit()

for i in range(n):
    symbol = str(input("Enter the stock symbol: ")).upper()
    try:
        quantity = int(input("Enter the quantity of stock you purchased: "))
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        purchase_price = float(input("Enter the purchase price: "))
    except ValueError as e:
        print("Invalid input:", e)
        exit()
    portfolio[symbol] = {'Quantity': quantity, 'Purchase Price': purchase_price}

total_investment = 0
current_value = 0

# Retrieve current prices and calculate portfolio value
for symbol in portfolio:
    try:
        stock_data = yf.download(symbol, period='1d')
        if stock_data.empty:
            raise ValueError(f"Failed to retrieve data for symbol '{symbol}'.")
        current_price = stock_data['Close'].iloc[-1]
        portfolio[symbol]['Current Price'] = current_price
        portfolio[symbol]['Value'] = current_price * portfolio[symbol]['Quantity']
        portfolio[symbol]['Gain/Loss'] = portfolio[symbol]['Value'] - (portfolio[symbol]['Purchase Price'] * portfolio[symbol]['Quantity'])
        portfolio[symbol]['Gain/Loss (%)'] = (portfolio[symbol]['Gain/Loss'] / (portfolio[symbol]['Purchase Price'] * portfolio[symbol]['Quantity']) * 100)

        total_investment += portfolio[symbol]['Purchase Price'] * portfolio[symbol]['Quantity']
        current_value += portfolio[symbol]['Value']
    except ValueError as e:
        print("Error:", e)
        exit()

# Calculate portfolio performance
portfolio['Portfolio'] = {'Quantity': '-', 'Purchase Price': '-', 'Current Price': '-', 'Value': current_value, 'Gain/Loss': round(current_value - total_investment, 2), 'Gain/Loss (%)': round(((current_value - total_investment) / total_investment) * 100, 2)}
    
# Create a DataFrame to store portfolio information
portfolio_df = pd.DataFrame.from_dict(portfolio, orient='index')
print("\nPortfolio:")
print(portfolio_df.round(2)) #Limit decimal places with round() function



# Display overall portfolio performance
print(f"\nOverall Portfolio Performance as of {today}:")
print("Total Investment:", total_investment)
print("Current Portfolio Value:", current_value)
print("Gain/Loss:", round(current_value - total_investment, 2))
print("Gain/Loss (%):", round(((current_value - total_investment) / total_investment) * 100, 2))


# Calculate total portfolio value
total_value = portfolio_df['Value'].sum()

# Calculate percentage of each stock in the portfolio
portfolio_df['Percentage'] = (portfolio_df['Value'] / total_value) * 100

# Plotting portfolio composition as a pie chart
stocks = portfolio_df.drop('Portfolio') #Removes the overall portfolio performance calculation from the generated graph
plt.figure(figsize=(8, 8))
plt.pie(stocks['Value'], labels=stocks.index, autopct='%1.1f%%')
plt.title('Portfolio Composition')
plt.savefig(f'{today}_Portfolio_Composition.png')
plt.show()


#Saves the portfolio information in a csv file for review and future reference using the current date
filename = f'{today}Portfolio.csv'
portfolio_df.to_csv(filename)
print(f"\nPortfolio data saved to '{filename}'.")