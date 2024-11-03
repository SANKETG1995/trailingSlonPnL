from kite_trade import *
import time
import pandas as pd

enctoken = '5N4NN5+zFuly/ZlVM/0ekYHtbxbFUbzx/cUS5nOQeJeqUccM7RYw3s4tnTKgpsQfFf7CawG8i6S/viOXNAYRwUNY8ybNjqgLWc94sHiFqLEdp0+1rYHBdA==' # input("Enter enc token \n\n")
kite = KiteApp(enctoken=enctoken)
stock = input("Enter trading Symbol:\n (IN ->NSE:<- ONLY)\n")
qty = input("Enter quantity:  \n")
symbol = stock.replace('NSE:','')
#def case1():
#    print(kite.margins(), '\n')
#    #print(kite.orders(), '\n')
#    order = pd.DataFrame(kite.margins())
#    q=kite.margins()
#    #order = order1['utilised']
#    print("Profit is --->", q['equity']['utilised']['m2m_realised']) #['utilised'])  #['m2m_realised'])
#    #print(kite.positions(), '\n')

def case1():
    # Retrieve margin information
    margins = kite.margins()
    
    # Print the entire margins information (commented out in your example)
    print(margins, '\n')

    # Extracting and printing equity and commodity balances separately
    equity = margins['equity']
    commodity = margins['commodity']

    print("Equity Balances:")
    print("Net:", equity['net'])
    print("Available Cash:", equity['available']['cash'])
    print("Utilised Margins:")
    for key, value in equity['utilised'].items():
        print(f"  {key}: {value}")

    print("\nCommodity Balances:")
    print("Net:", commodity['net'])
    print("Available Cash:", commodity['available']['cash'])
    print("Utilised Margins:")
    for key, value in commodity['utilised'].items():
        print(f"  {key}: {value}")

    # Print realized profit from equity
    print("Profit is --->", equity['utilised']['m2m_realised'])


def case2():
    # Initial parameters
    #    entry_price = 0.00  # The price at which you entered the position
    trailing_percent = 0.002  # 1% trailing stop

    q=kite.margins()
    df=kite.ltp(stock)
    current_price = df[stock]['last_price']  # The current price (you would get this from your data source)

    pivot_stop_price = current_price * (1 - trailing_percent)  # Initial trailing stop price
    new_pivot = pivot_stop_price
    while current_price > pivot_stop_price :
        # Check if the current price is higher than the trailing stop price
        if current_price > pivot_stop_price :
           new_pivot = current_price * (1-trailing_percent)
           if new_pivot > pivot_stop_price :
              pivot_stop_price = new_pivot
        df = kite.ltp(stock)
        current_price = df[stock]['last_price']
        print(f"Current Price: {current_price:.2f}, Trailing Stop Price: {pivot_stop_price:.2f}")
        print("Profit is --->", q['equity']['utilised']['m2m_realised']) #['utilised'])  #['m2m_realised'])
        time.sleep(1)
    print("Stop Loss Executed!!")
    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NSE,
                         tradingsymbol=symbol,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=qty,
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=None,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")

    print(order)

def case3():
    exit_threshold = -500  # Loss threshold for immediate exit
    positive_exit_threshold = 100  # Example positive threshold to start trailing
    trailing_percent = 0.20  # 20% trailing stop
    monitoring = True
    highest_pnl = None  # Track the highest P&L seen

    while monitoring:
        try:
            # Retrieve positions to get MIS position details
            positions = kite.positions()
            equity_positions = positions.get('day', [])

            if not equity_positions:
                print("No positions found in 'day'. Retrying...")
                time.sleep(2)
                continue

            for position in equity_positions:
                # Only check for MIS positions of the specified stock
                if position['product'] == 'MIS' and position['tradingsymbol'] == stock:
                    pnl = position.get('pnl', None)
                    if pnl is None:
                        print(f"Unable to retrieve P&L for {position['tradingsymbol']}.")
                        continue

                    print(f"Current P&L for {position['tradingsymbol']}: {pnl}")

                    # Exit immediately if P&L drops below exit_threshold
                    if pnl < exit_threshold:
                        print(f"Loss of {pnl} exceeds threshold. Exiting position for {position['tradingsymbol']} at market price...")
                        kite.place_order(
                            variety=kite.VARIETY_REGULAR,
                            exchange=position['exchange'],
                            tradingsymbol=position['tradingsymbol'],
                            transaction_type=kite.TRANSACTION_TYPE_SELL if position['quantity'] > 0 else kite.TRANSACTION_TYPE_BUY,
                            quantity=abs(position['quantity']),
                            product=kite.PRODUCT_MIS,
                            order_type=kite.ORDER_TYPE_MARKET
                        )
                        monitoring = False
                        break

                    # Start trailing once the P&L reaches the positive threshold
                    if pnl > positive_exit_threshold:
                        if highest_pnl is None or pnl > highest_pnl:
                            highest_pnl = pnl  # Update highest P&L if the current P&L is the new max
                            trailing_stop = highest_pnl * (1 - trailing_percent)
                            print(f"New highest P&L: {highest_pnl}, setting trailing stop at {trailing_stop}")

                        # Exit if P&L drops below the trailing stop
                        if pnl < trailing_stop:
                            print(f"P&L dropped to {pnl}, below trailing stop {trailing_stop}. Exiting position at market price...")
                            kite.place_order(
                                variety=kite.VARIETY_REGULAR,
                                exchange=position['exchange'],
                                tradingsymbol=position['tradingsymbol'],
                                transaction_type=kite.TRANSACTION_TYPE_SELL if position['quantity'] > 0 else kite.TRANSACTION_TYPE_BUY,
                                quantity=abs(position['quantity']),
                                product=kite.PRODUCT_MIS,
                                order_type=kite.ORDER_TYPE_MARKET
                            )
                            monitoring = False
                            break
                    else:
                        print(f"Position for {position['tradingsymbol']} is within thresholds, monitoring continues...")

            # Display the P&L and check conditions every 2 seconds
            time.sleep(2)

        except Exception as e:
            print(f"Error fetching positions or processing: {str(e)}")
            break

def case4():
    kite.modify_order(variety=kite.VARIETY_REGULAR,
                      order_id="order_id",
                      parent_order_id=None,
                      quantity=5,
                      price=200,
                      order_type=kite.ORDER_TYPE_LIMIT,
                      trigger_price=None,
                      validity=kite.VALIDITY_DAY,
                      disclosed_quantity=None)

def case5():
    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                             exchange=kite.EXCHANGE_NSE,
                             tradingsymbol="estACC",
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=1,
                             product=kite.PRODUCT_MIS,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=3000,
                             validity=None,
                             disclosed_quantity=None,
                             trigger_price=None,
                             squareoff=None,
                             stoploss=None,
                             trailing_stoploss=None,
                             tag="TradeViaPython")

    print(order)
def case6():
    # Initial parameters
    trailing_percent = 0.002  # 1% trailing stop
    q=kite.margins()
    df=kite.ltp(stock)
    current_price = df[stock]['last_price']  # The current price (you would get this from your data source)
    entry_price = current_price

    pivot_stop_price = entry_price * (1 + trailing_percent)  # Initial trailing stop price
    new_pivot = pivot_stop_price
    while current_price < pivot_stop_price :
        # Check if the current price is higher than the trailing stop price
        if current_price < pivot_stop_price :
           new_pivot = current_price * (1 + trailing_percent)
           if new_pivot < pivot_stop_price :
              pivot_stop_price = new_pivot
        df = kite.ltp(stock)
        current_price = df[stock]['last_price']
        print(f"Current Price: {current_price:.2f}, Trailing Stop Price: {pivot_stop_price:.2f}")
        print("Profit is --->", q['equity']['utilised']['m2m_realised']) #['utilised'])  #['m2m_realised'])
        time.sleep(1)
    print("Stop Loss Executed!!")
    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NSE,
                         tradingsymbol=symbol,
                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                         quantity=qty,
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=None,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")

    print(order)
def exit_program():
    print("Exiting the program")
    exit()

# Create a dictionary to map cases to functions
switch = {
    1: case1,
    2: case2,
    3: case3,
    4: case4,
    5: case5,
    6: case6,
    0: exit_program
}

while True:
    # Get the user's choice
    choice = int(input("Enter a case (1-6) \n2. NSE going up \n6. NSE going down  OR \n0 to exit: \n"))

    # Use the dictionary to execute the chosen case or exit
    case_function = switch.get(choice, lambda: print("Invalid choice"))
    case_function()
