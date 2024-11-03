from kite_trade import *
import time
import pandas as pd

#enctoken = input("Enter enc token \n\n")
#kite = KiteApp(enctoken=enctoken)

def case1():
    print(kite.margins())
    print(kite.orders())
    print(kite.positions())

def case2():

    # Initial parameters
    entry_price = 100.0  # The price at which you entered the position
    trailing_percent = 0.05  # 5% trailing stop
    current_price = 110.0  # The current price (you would get this from your data source)

    pivot_stop_price = entry_price * (1 - trailing_percent)  # Initial trailing stop price
    new_pivot = 0.0
    while current_price > pivot_stop_price :
        # Check if the current price is higher than the trailing stop price
        if current_price > pivot_stop_price :
           new_pivot = current_price * (1-trailing_percent)
           if new_pivot > pivot_stop_price :
              pivot_stop_price = new_pivot
        # Simulate price changes (you would get this from your data source)
        # Open the file in read mode ('r')
        file_path = 'your_file.txt'  # Replace with the path to your file
        try:
            with open(file_path, 'r') as file:
                # Read a single line from the file
                line = file.readline()
        
                # You can convert the line to the appropriate data type (e.g., int, float, etc.)
                value = float(line)  # Assuming the file contains an integer value
        
                # Print the read value
                #print("Value from the file:", value)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except ValueError:
            print("Invalid value in the file. Expected an integer.")
        except Exception as e:
            print(f"An error occurred: {e}")
        current_price = value
        print(f"Current Price: {current_price:.2f}, Trailing Stop Price: {pivot_stop_price:.2f}")
        time.sleep(1)
        #kite.modify_orderi(variety=kite.VARIETY_REGULAR,
        #          order_id="order_id",
        #          parent_order_id=None,
        #          quantity=5,
        #          price=trailing_stop_price,
        #          order_type=kite.ORDER_TYPE_SL,
        #          trigger_price=None,
        #          validity=kite.VALIDITY_DAY,
        #          disclosed_quantity=None)

    print("Stop Loss Executed!!")
def case3():
    while True:
        print(pd.DataFrame(kite.ltp(["NSE:NIFTY 50"])))
        df = kite.ltp(["NSE:NIFTY 50"])
        value = df['NSE:NIFTY 50']['last_price']
        print("Last price again ==", value)

        time.sleep(2)

def exit_program():
    print("Exiting the program")
    exit()

# Create a dictionary to map cases to functions
switch = {
    1: case1,
    2: case2,
    3: case3,
    0: exit_program
}

while True:
    # Get the user's choice
    choice = int(input("Enter a case (1-3) or 0 to exit: "))

    # Use the dictionary to execute the chosen case or exit
    case_function = switch.get(choice, lambda: print("Invalid choice"))
    case_function()

