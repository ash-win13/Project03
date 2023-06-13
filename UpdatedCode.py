import ccxt
import time

trendline_period = 20
trama_period = 10

trendline_break = False
trama = []
in_position = False
is_enabled = True

api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret
})

def calculate_trendline_with_breaks(data):
    trendline = sum(data[-trendline_period:]) / trendline_period

    '''if data[-1] > trendline and data[-2] <= trendline:
        return True
    elif data[-1] < trendline and data[-2] >= trendline:
        return True
    else:
        return False'''
    if data[-1] == trendline:
        return False
    else:
        return True

def calculate_trama(data):
    if len(data) >= trama_period:
        trama_sum = sum(data[-trama_period:])
        trama_average = trama_sum / trama_period
        return trama_average
    else:
        return None

def place_buy_order(symbol, quantity):
    print(f"Placing buy order for {quantity} {symbol}")

def place_sell_order(symbol, quantity):
    print(f"Placing sell order for {quantity} {symbol}")

def toggle_bot():
    global is_enabled
    is_enabled = not is_enabled
    print("Bot is", "enabled" if is_enabled else "disabled")

def main_loop():
    while True:
        try:
            if is_enabled:
                symbol = input("Enter the symbol of the cryptocurrency (e.g., BTC/USDT): ")
                buy_quantity = float(input("Enter the quantity to buy: "))
                sell_quantity = buy_quantity
                
                candlesticks = exchange.fetch_ohlcv(symbol, '1m')
                close_prices = [candlestick[4] for candlestick in candlesticks]

                trendline_break = calculate_trendline_with_breaks(close_prices)

                trama_value = calculate_trama(close_prices)
                if trama_value is not None:
                    trama.append(trama_value)

                if trendline_break and not in_position:
                    place_buy_order(symbol, buy_quantity)
                    in_position = True
                elif not trendline_break and in_position:
                    place_sell_order(symbol, sell_quantity)
                    in_position = False

                print("Trendline Break:", trendline_break)
                print("TRAMA:", trama)

        except Exception as e:
            print("An error occurred:", str(e))

        time.sleep(60)

toggle_bot()

main_loop()
