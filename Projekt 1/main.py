from math import floor
from matplotlib import pyplot
from dateutil import parser
import csv
import os

STARTING_MONEY = 1000
CURRENCIES = os.listdir('./data')

class Simulator:
    def simulation(self, exchange_rate, signals, money):
        currency = 0
        for it in range(len(exchange_rate)):
            if signals[it] == "buy":
                if money != 0:
                    currency = money * exchange_rate[it]
            elif signals[it] == "sell":
                if currency != 0:
                    money = currency * (1 / exchange_rate[it])
        if money == 0:
            return currency * (1 / exchange_rate[-1])
        else:
            return money

    def multi_currency_simulator(self, enchanted = False):
        overall = float(0.0)
        for currency in CURRENCIES:
            currency = Currency(currency)
            time, exchange_rate = currency.create_data()
            macd = Macd(exchange_rate, enchanted)
            money_after_simulation = self.simulation(exchange_rate[26::], macd.getBuySellSignals(), STARTING_MONEY)

            profit = floor(money_after_simulation / STARTING_MONEY * 100) - 100
            overall += profit
            print(currency.getName() + ": " + str(profit) + "%")

            Diagrams.show_macd_signal_diagram(Diagrams(), time[26::], macd.getMacd(26), macd.getSignal(17))
            Diagrams.show_exchange_rate_diagram(Diagrams(), time[26::], exchange_rate[26::])

            Diagrams.show_parallel_diagrams(Diagrams(), time[26::], macd, exchange_rate[26::], 0, 100)
        print("OVERALL: " + str(overall) + '%')
        print('AVARAGE: ' + str(overall / len(CURRENCIES)) + "%")

    def single_currency_simulator(self, name,  enchanted = False):
        currency = Currency(name)
        time, exchange_rate = currency.create_data()
        macd = Macd(exchange_rate, enchanted)
        money_after_simulation = self.simulation(exchange_rate[26::], macd.getBuySellSignals(), STARTING_MONEY)

        profit = floor(money_after_simulation / STARTING_MONEY * 100) - 100

        print(currency.getName() + ": " + str(profit) + "%")

        Diagrams.show_macd_signal_diagram(Diagrams(), time[26::], macd.getMacd(26), macd.getSignal(17))
        Diagrams.show_exchange_rate_diagram(Diagrams(), time[26::], exchange_rate[26::])

        Diagrams.show_parallel_diagrams(Diagrams(), time[26::], macd, exchange_rate[26::], 270, 370)

class Diagrams:
    def show_macd_signal_diagram(self, time, macd, signal):
        pyplot.plot(time, macd, label="macd", color='red')
        pyplot.plot(time, signal, label="signal", color='blue')
        pyplot.legend()
        pyplot.grid(True)
        pyplot.ylabel('Wartość składowych')
        pyplot.xlabel('Data')
        pyplot.title('Wskaźnik MACD')
        pyplot.show()

    def show_exchange_rate_diagram(self, time, data):
        pyplot.plot(time, data, label="macd", color='red')
        pyplot.ylabel('Kurs [ 1 CHF = ? zł]')
        pyplot.xlabel('Data')
        pyplot.title('Kurs franka szwajcarskiego')
        pyplot.grid(True)
        pyplot.show()

    def show_parallel_diagrams(self, time, macd, exchange_rate, start_date, end_date):
        print(str(time[start_date]) + " " + str(time[end_date-1]))
        pyplot.figure(1)
        pyplot.subplot(211)
        pyplot.plot(time[start_date:end_date], exchange_rate[start_date:end_date])
        pyplot.grid(True)
        pyplot.ylabel("Kurs")

        pyplot.title("Kurs waluty")
        pyplot.subplot(212)
        pyplot.plot(time[start_date:end_date], macd.getMacd(26)[start_date:end_date], color="red", label="macd")
        pyplot.plot(time[start_date:end_date], macd.getSignal(17)[start_date:end_date], color="blue", label="signal")
        pyplot.legend()
        pyplot.grid(True)
        pyplot.title("Składowe wskaźnika MACD")
        pyplot.ylabel("Wartość składowej")
        pyplot.xlabel("Data")
        pyplot.show()

class Currency:
    __name = ""

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name.split('.')[0].replace('_', ' ')

    def create_data(self):
        file = "./data/" + str(self.__name)
        f = open(file, 'r')
        tmp = list(csv.reader(f))
        data = []
        for it in reversed(tmp[1::]):
            data.append(it)

        parser.parser('2018-03-28')
        time = [parser.parse(i[1]) for i in data]
        exchange_rate = [float(it[2]) for it in data]

        return time, exchange_rate

class Macd:
    __macd = []
    __signal = []
    __buy_sell_signals = []

    def __init__(self, exchange_rate, enchanted = False):
        self.calculate_macd(exchange_rate)
        self.calculate_signal()
        if enchanted:
            self.enchanted_calculate_buy_sell_signals()
        else:
            self.calculate_buy_sell_signals()

    def printer(self):
        print(len(self.__macd))
        print(len(self.__signal))
        print(len(self.__buy_sell_signals))

    def calculate_ema(self, n, data, day):
        one_minus_alpha = 1 - (2 / (n - 1))
        p1 = data[day - n: day:]
        p = []
        for i in reversed(p1):
            p.append(i)
        counter = float(0.0)
        denominator = float(0.0)
        for i in range(n):
            power = pow(one_minus_alpha, i)
            counter += power * p[i]
            denominator += power

        return counter / denominator

    def calculate_macd(self, exchange_rate):
        self.__macd = []
        for i in range(0, len(exchange_rate)):
            if i >= 26:
                temp_ema12 = self.calculate_ema(12, exchange_rate, i)
                temp_ema26 = self.calculate_ema(26, exchange_rate, i)
                self.__macd.append(temp_ema12 - temp_ema26)
            else:
                self.__macd.append(float(0))

    def calculate_signal(self):
        self.__signal = []
        for i in range(9, len(self.__macd)):
            self.__signal.append(self.calculate_ema(9, self.__macd, i))

    def calculate_buy_sell_signals(self):
        self.__buy_sell_signals = ["none"]
        tmp_macd = self.getMacd(26)
        tmp_signal = self.getSignal(17)

        for it in range(1, len(tmp_macd)):
            if tmp_macd[it - 1] > tmp_signal[it - 1] and tmp_macd[it] < tmp_signal[it]:
                self.__buy_sell_signals.append("sell")
            elif tmp_macd[it - 1] < tmp_signal[it - 1] and tmp_macd[it] > tmp_signal[it]:
                self.__buy_sell_signals.append("buy")
            else:
                self.__buy_sell_signals.append("none")

    def enchanted_calculate_buy_sell_signals(self):
        self.__buy_sell_signals = ["none"]
        tmp_macd = self.getMacd(26)
        tmp_signal = self.getSignal(17)

        for it in range(1, len(tmp_macd)):
            if tmp_macd[it - 1] > tmp_signal[it - 1] and tmp_macd[it] < tmp_signal[it] and tmp_signal[it] < 0:
                self.__buy_sell_signals.append("sell")
            elif tmp_macd[it - 1] < tmp_signal[it - 1] and tmp_macd[it] > tmp_signal[it] and tmp_signal[it] > 0:
                self.__buy_sell_signals.append("buy")
            else:
                self.__buy_sell_signals.append("none")

    def getMacd(self, n=0):
        return self.__macd[n::]

    def getSignal(self, n=0):
        return self.__signal[n::]

    def getBuySellSignals(self, n=0):
        return self.__buy_sell_signals[n::]

if __name__ == '__main__':
    # print("CLEAR")
    # Simulator.multi_currency_simulator(Simulator(), False)
    # print("ENCHANTED")
    # Simulator.multi_currency_simulator(Simulator(), True)
    Simulator.single_currency_simulator(Simulator(), 'frank_szwajcarski.csv', True)