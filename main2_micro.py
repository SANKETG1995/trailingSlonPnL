from kite_trade import *
import time
import pandas as pd

enctoken = 'MAaviZ30P4IPuQ4bwgmLS5rATUOV3jjxXKT5RgER+dpawiGOoMecioXQQL4D0Xjfwm/PZesVmSNdT0WtM3w5ihEBzvbtPTAtvCFDDISQrZ3SQfXWbS+l9g==' # input("Enter enc token \n\n")
kite = KiteApp(enctoken=enctoken)
stock = input("Enter trading Symbol:\n (IN ->NSE:<- ONLY)\n")
qty = input("Enter quantity:  \n")
symbol = stock.replace('NSE:','')
def case1():
    print(kite.margins(), '\n')
    #print(kite.orders(), '\n')
    order = pd.DataFrame(kite.margins())
    q=kite.margins()
    #order = order1['utilised']
    print("Profit is --->", q['equity']['utilised']['m2m_realised']) #['utilised'])  #['m2m_realised'])
    #print(kite.positions(), '\n')

def case2():
    # Initial parameters
    #    entry_price = 0.00  # The price at which you entered the position
    trailing_percent = 0.0005  # 1% trailing stop

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
    while True:
        print(stock)
        df = kite.ltp(stock)
        value = df[stock]['last_price']
        print("Last price again --> ", value)
        time.sleep(1)

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
    trailing_percent = 0.0005  # 1% trailing stop
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
