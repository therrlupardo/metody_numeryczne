from math import floor
from matplotlib import pyplot
import csv
from dateutil import parser

STARTING_MONEY = 1000
CURRENCIES = ['./data/hongkong_dolar.csv', './data/usa_dolar.csv', './data/frank_szw.csv','./data/euro.csv' ]

def ema(n, data, day):
    one_minus_alpha = 1 - (2 / (n - 1))
    p1 = data[day-n: day:]
    p = []
    for i in reversed(p1):
        p.append(i)
    counter = float(0.0)
    denominator = float(0.0)
    for i in range(n):
        power = pow(one_minus_alpha, i)
        counter += power * p[i]
        denominator += power

    return counter/denominator

def create_data(file):
    f = open(file, 'r')
    tmp = list(csv.reader(f))
    data = []
    for it in reversed(tmp[1::]):
        data.append(it)

    parser.parser('2018-03-28')
    time = [parser.parse(i[1]) for i in data]
    exchange_rate = [float(it[2]) for it in data]

    return time, exchange_rate

def calculate_macd(exchange_rate):
    macd = []
    for i in range(0, 1000):
        if i >= 26:
            temp_ema12 = ema(12, exchange_rate, i)
            temp_ema26 = ema(26, exchange_rate, i)
            macd.append(temp_ema12 - temp_ema26)
        else:
            macd.append(float(0))
    return macd

def calculate_signal(macd):
    signal = []
    for i in range(9, len(macd)):
        signal.append(ema(9, macd, i))
    return signal

def show_diagrams(time, macd, signal):
    pyplot.plot(time, macd, label="macd", color='red')
    pyplot.plot(time, signal, label="signal", color='blue')
    pyplot.legend()
    pyplot.ylabel('Kurs średni')
    pyplot.xlabel('Data')
    pyplot.title('Kurs dolar hongkongski')
    pyplot.show()

def calculate_buying_signals(macd, signal):
    out = [0]
    for it in range(1, len(macd)):
        if macd[it-1] > signal[it-1] and macd[it] < signal[it]:
            out.append("sell")
        elif macd[it-1] < signal[it-1] and macd[it] > signal[it]:
            out.append("buy")
        else:
            out.append("none")
    return out

def simulation(exchange_rate, signals, money):
    currency = 0
    for it in range(len(signals)):
        if signals[it] == "buy":
            if money != 0:
                currency = money * exchange_rate[it]
        elif signals[it] == "sell":
            if currency != 0:
                money = currency * (1/exchange_rate[it])
    if money == 0:
        return currency * (1/exchange_rate[-1])
    else:
        return money

if __name__ == '__main__':
    for currency in CURRENCIES:
        time, exchange_rate = create_data(currency)
        macd = calculate_macd(exchange_rate)
        signal = calculate_signal(macd)
        buying_signals = calculate_buying_signals(macd[26::], signal[17::])
        money_after_simulation = simulation(exchange_rate[26::], buying_signals, STARTING_MONEY)
        name = currency.split('/')[2].split('.')[0]
        profit = floor(money_after_simulation/STARTING_MONEY * 100 - 100)
        print(name + ": " + str(profit) + "%")
        show_diagrams(time[26::], macd[26::], signal[17::])
