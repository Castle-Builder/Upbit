import pyupbit
import datetime
import time

access_key = ''
secret_key = ''
upbit = pyupbit.Upbit(access_key, secret_key)

print("Thank you Larry")

# 3일 이평선 계산
def get_yesterday_ma3(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=3).mean()
    return ma[-2]
# 목표가 계산
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)

    noise_list = []
    for i in range(-21,-2):
        noise = 1- abs(df.iloc[i]['open']-df.iloc[i]['close'])/abs(df.iloc[i]['high']-df.iloc[i]['low'])
        noise_list.append(noise)

    noise_average = sum(noise_list)/20

    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low)*noise_average
    return target


# 현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


#매수함수
def buy_crypto_currency(ticker):
    balance = upbit.get_balance("KRW")
    upbit.buy_market_order(ticker, balance)


#매도함수
def sell_crypto_currency(ticker):
    unit = upbit.get_balance("KRW-ETH")
    upbit.sell_market_order(ticker, unit)



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma3 = get_yesterday_ma3("KRW-ETH")
target_price = get_target_price("KRW-ETH")

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma3 = get_yesterday_ma3("KRW-ETH")
            sell_crypto_currency("KRW-ETH")

        current_price = pyupbit.get_current_price("KRW-ETH")
        if (current_price > target_price) and (current_price > get_yesterday_ma3("KRW-ETH")):
            buy_crypto_currency("KRW-ETH")
        if current_price < target_price*0.98:
            sell_crypto_currency("KRW-ETH")
    except:
        print("")
    time.sleep(1)
