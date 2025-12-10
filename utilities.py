#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    stock_list.sort(key=lambda stock: stock.symbol)


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
     for stock in stock_list:
        stock.DataList.sort(key=lambda data: data.date)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    stock = None
    for s in stock_list:
        if s.symbol == symbol:
            stock = s
            break
    if not stock:
        print("Stock symbol not found.")
        return
    if not stock.DataList:
        print("No daily data to display.")
        return
    # sort data first by calling function and then get data and prices to plot
    stock.DataList.sort(key=lambda data: data.date)
    dates = [data.date for data in stock.DataList]
    prices = [data.close for data in stock.DataList]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o', linestyle='-', color='blue')
    # dots use o marker
    plt.title(f"Closing Prices Over Time For {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    # rotating xticks for visability
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()