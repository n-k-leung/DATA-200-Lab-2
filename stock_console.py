# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    # option = ""
    # while option != "0":
    #     pass
     while True:
        clear_screen()
        print("Add New Stock ---")
        symbol = input("Enter stock symbol to add (or 0 to cancel): ").upper()
        if symbol == "0":
            break
        # check for stock symbol repeat first and then check for number of shares to detect this issue earlier on
        if any(stock.symbol == symbol for stock in stock_list):
            print("Stock already exists, cannot add it again.")
            input("Press Enter to return.")
            return
        
        # take out white spaces cause sometime cause errros
        name = input("Enter company name: ").strip()
        try:
            shares = float(input("Enter number of shares: "))
        except ValueError:
            print("Invalid input for number of shares (must be number), please try again.")
            input("Press Enter to continue.")
            continue
        
        stock_list.append(Stock(symbol, name, shares))
        stock_data.save_stock_data(stock_list)
        print(f"{symbol} added to stock list.")
        input("Press Enter to continue.")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option != "0":
            print("Invalid Option, must be 1, 2, or 0")
            input("Press Enter to continue.")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    # print("Stock List: [",end="")
    print("Stock List:")
    for s in stock_list:
        print(f"- {s.symbol}: {s.name}, Shares: {s.shares}")
    symbol = input("Enter stock symbol to buy (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    exists = False
    for s in stock_list:
        if s.symbol == symbol:
            stock = s
            exists = True
            break
    # check if stock exists first then it should return back to update shares menu afterwards
    if not exists:
        print("Stock does not exists")
    # if stock exists
    if exists:
        try:
            shares = int(input("Enter number of shares to buy: "))
            if shares <= 0:
                print("Please enter a positive number of shares to buy, if want to subtract, you must sell stock")
                return
            stock.buy(shares)
            print(f"Bought {shares} shares of {symbol}. Total now: {stock.shares}")
            stock_data.save_stock_data(stock_list)
        except ValueError:
            print("Invalid number of shares, shares must be a integer value")      
    input("Press Enter to continue.")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List:")
    for s in stock_list:
        print(f"- {s.symbol}: {s.name}, Shares: {s.shares}")
    symbol = input("Enter stock symbol to sell (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    exists = False
    for s in stock_list:
        if s.symbol == symbol:
            stock = s
            exists = True
            break
    # check if stock exists first then it should return back to update shares menu afterwards
    if not exists:
        print("Stock does not exists")
    # if stock exists
    if exists:
        try:
            shares = int(input("Enter number of shares to sell: "))
            if shares <= 0:
                print("Please enter a positive number.")
                return
            stock.sell(shares)
            print(f"Sold {shares} shares of {symbol}. Total now: {stock.shares}")
            stock_data.save_stock_data(stock_list)
        except ValueError:
            print("Invalid number of shares, shares must be a integer value")
    input("Press Enter to continue.")

# Remove stock and all daily data
def delete_stock(stock_list):
    # clear_screen()
    while True: # repeat so that stock entered correctly
        clear_screen()
        print("Delete Stock and Daily Data ---")
        symbol = input("Enter stock symbol to delete (or 0 to cancel): ").upper()
        if symbol == "0":
            break
        exists = False
        for s in stock_list:
            if s.symbol == symbol:
                stock = s
                exists = True
                break
        if not exists:
            print("Stock does not exists")
        else:
            for stock in stock_list:
                if stock.symbol == symbol:
                    stock_list.remove(stock)
                    print(f"{symbol} stock and daily data deleted.")
                    break
            stock_data.save_stock_data(stock_list)
        # note must save to database or else its not updatd on database but just on current run of the program
        input("Press Enter to continue.")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print(f"Loaded {len(stock_list)} stocks from the database.")
    stocks_exists = False
    for _ in stock_list:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks found.")
    elif stocks_exists:
        print("Stock Data ---")
        for s in stock_list:
            print(f"Symbol: {s.symbol} | Name: {s.name} | Shares: {s.shares}")
    input("Press Enter to continue.")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    stocks_exists = False
    for _ in stock_list:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks available.")
        input("Press Enter to return to menu.")
        return
    print("Stock List:")
    for s in stock_list:
        print(f"- {s.symbol}: {s.name}, Shares: {s.shares}")
    symbol = input("Enter stock symbol to add daily data for (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    exists = False
    for s in stock_list:
        if s.symbol == symbol:
            stock = s
            exists = True
            break
    if not exists:
        print("Stock does not exists")
        input("Press Enter to return to menu.")
        return
    # stock exists then check each input for errors
    try:
        date_input = input("Enter date (MM/DD/YYYY): ")
        date_obj = datetime.strptime(date_input, "%m/%d/%Y")
    except ValueError:
        print(f"Invalid input, please enter date in format (MM/DD/YYYY) and try again.")
        input("Press Enter to return to menu.")
        return

    try:
        price = float(input("Enter closing price: "))
    except ValueError:
        print(f"Invalid input, please enter price as float and try again.")
        input("Press Enter to return to menu.")
        return

    try:
        volume = int(input("Enter volume: "))
    except ValueError:
        print(f"Invalid input, please enter volume in integer format and try again.")
        input("Press Enter to return to menu.")
        return
        
    new_data = DailyData(date_obj, price, volume)
    stock.add_data(new_data)
    print("Daily data added successfully.")
    stock_data.save_stock_data(stock_list)
    input("Press Enter to continue.")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    # for stock in stock_data: check if stock data exists or errpr
    stocks_exists = False
    for _ in stock_data:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks to report.")
    else:
        for stock in stock_data:
            print(f"Symbol: {stock.symbol}, Name: {stock.name}, Shares: {stock.shares}")
            if stock.DataList:
                print(f"{stock.symbol} Daily Data:")
                for data in stock.DataList:
                    print(f"Date: {data.date.strftime('%m/%d/%Y')}, Close Price: ${data.close:.2f}, Volume: {data.volume}")
            else:
                print(f"No daily data available for {stock.symbol}.")
    input("Press Enter to continue.")



  


# Display Chart
def display_chart(stock_list):
    # print("Stock List: [",end="")
    # for stock in stock_list:
    clear_screen()
    print("Display Chart ---")
    stocks_exists = False
    for _ in stock_list:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks to display.")
        input("Press Enter to return to menu.")
        return
    else:
        print("Stock List:")
        for s in stock_list:
            print(f"- {s.symbol}: {s.name}, Shares: {s.shares}")
        symbol = input("Enter stock symbol to display chart (or 0 to cancel): ").upper()
        if symbol == "0":
            return
        exists = False
        for s in stock_list:
            if s.symbol == symbol:
                exists = True
                break
        if not exists:
            print("Stock not found.")
            input("Press Enter to return to menu.")
            return
        try:
            display_stock_chart(stock_list, symbol)
        except:
            print("Error displaying chart.")
        input("Press Enter to continue.")

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve from Web")
        print("4 - Import from CSV")
        print("0 - Return to Main Menu")
        option = input("Enter Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Stock data saved to database.")
            input("Press Enter to return to menu.")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Stock data loaded from database.")
            input("Press Enter to return to menu.")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        elif option == "0":
            print("Returning to Main Menu")
        else:
            print("Invalid option. Try again.")


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Stock Data from Web ---")
    stocks_exists = False
    for _ in stock_list:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks to retrieve data.")
        input("Press Enter to return to menu.")
        return
    print("Stock List:")
    for s in stock_list:
        print(f"- {s.symbol}: {s.name}")
    symbol = input("Enter the stock symbol to retrieve data for (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    exists = False
    for s in stock_list:
        if s.symbol == symbol:
            stock = s
            exists = True
            break
    if not exists:
        print("Stock not found.")
        input("Press Enter to return to menu.")
        return
    print("Enter date range to retrieve data (format: mm/dd/yy)")
    date_start = input("Start Date: ")
    date_end = input("End Date: ")
    try:
        datetime.strptime(date_start, "%m/%d/%y")
    except ValueError:
        print("Invalid date format, please enter in mm/dd/yy and try again.")
        input("Press Enter to return to the menu.")
        return
    
    try:
        datetime.strptime(date_end, "%m/%d/%y")
    except ValueError:
        print("Invalid date format, please enter in mm/dd/yy and try again.")
        input("Press Enter to return to the menu.")
        return
    
    print("Retrieving data, please wait...")

    try:
        count = stock_data.retrieve_stock_web(date_start, date_end, [stock])
        stock_data.save_stock_data(stock_list)
        print(f"{count} daily records retrieved and saved.")
    except Exception as e:
        print("Error retrieving data")
    input("Press Enter to return to the menu.")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance ---")
    stocks_exists = False
    for _ in stock_list:
        stocks_exists = True
        break
    if not stocks_exists:
        print("No stocks available.")
        input("Press Enter to return to the menu.")
        return
    print("Stock List:")
    for s in stock_list:
        print(f"- {s.symbol}: {s.name}")
    symbol = input("Enter the stock symbol to import (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    exists = False
    for s in stock_list:
        if s.symbol == symbol:
            exists = True
            break
    if not exists:
        print("Stock not found.")
        input("Press Enter to return to menu.")
        return
    filename = input("Enter filename: ")
    if not path.exists(filename):
        print("File does not exist, please check if filename is correct or is in the correct location.")
        input("Press Enter to return to the menu.")
        return
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        stock_data.save_stock_data(stock_list)
        # make sure when importing csv file, there are no commas in the volume column and date is formated as yyyy/mm/dd, in excel can change by going to format and then adjusting the date manually
        print("CSV File Imported")
    except Exception as e:
        print(f"Failed to import CSV: {e}")
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    stock_data.load_stock_data(stock_list)
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()