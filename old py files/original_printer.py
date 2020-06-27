import csv
import math
import matplotlib.pyplot as plt
from tabulate import tabulate
from tqdm import tqdm
filenames = ['OptionTradeScreenerResults_20200505', 'OptionTradeScreenerResults_20200507', 'OptionTradeScreenerResults_20200508',
    'OptionTradeScreenerResults_20200511', 'OptionTradeScreenerResults_20200511', 'OptionTradeScreenerResults_20200512',
    'OptionTradeScreenerResults_20200513', 'OptionTradeScreenerResults_20200515','OptionTradeScreenerResults_20200518',
    'OptionTradeScreenerResults_20200519']

def symbols():
    symbol_counts = {}
    def read_data(filename):
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] in symbol_counts:
                    symbol_counts[row[1]] += 1
                else:
                    symbol_counts[row[1]] = 1
    for f in tqdm(filenames):
        read_data(f + '.csv')
    sorted = {k: v for k, v in sorted(symbol_counts.items(), key=lambda item: item[1])}
    for k in sorted:
        print(k, sorted[k])
    print(len(sorted))
#symbols()

def printer():
    data = []
    with open('OptionTradeScreenerResults_20200519.csv') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count == 0:
                count += 1
                data.append(row)
                continue
            if count < 5: #change this num to look at different block trades
                count += 1
                continue
            data.append(row)
            break
    rows = []
    for trade in data:
        for i in range(len(trade)):
            rows.append((i, data[0][i], data[1][i]))
    headers = ['index', 'param', 'val']
    print(tabulate(rows, headers))
printer()

def earnings7days():
    symbol_counts = {}
    def read_data(filename):
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader: ###first condition sets criteria for what we want to look at
                if row[45][:6] != 'Next_7':
                    continue
                if row[1] in symbol_counts:
                    symbol_counts[row[1]] += 1
                else:
                    symbol_counts[row[1]] = 1
    for f in filenames:
        read_data(f + '.csv')
    sortedd = {k: v for k, v in sorted(symbol_counts.items(), key=lambda item: -1*item[1])}
    #for k in sortedd:
    #    print(k, sortedd[k])
    #print(len(sortedd), "different stocks with earnings in the next 7 days")
    return list(sortedd.keys()) ### four stocks with the most block trades
#earnings7days()

def specific_stock1(stock):
    def below_or_above(filename):
        below_mid = 0
        above_mid = 0
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                symbol = row[1]
                type = row[6]
                if symbol == stock and type == 'CALL': ### looking at calls
                    trade_price = float(row[14])
                    bid = float(row[16])
                    ask = float(row[17])
                    if bid == ask:
                        continue
                    mid = (bid + ask)/2
                    notional = float(row[19])
                    if trade_price < mid:
                        below_mid += (mid - trade_price)/(mid - bid) * math.sqrt(notional) ### the trade price's (relative) distance from the mid, weighted by sqrt of notional
                    elif trade_price > mid:
                        above_mid += (trade_price - mid)/(ask - mid) * math.sqrt(notional)
        return below_mid, above_mid
    ratios = []
    rows = []
    for f in tqdm(filenames):
        b, a = below_or_above(f + '.csv')
        if a == 0:
            a += 1
        ratios.append(b/a)
        rows.append((f[-4:], b/a))
    headers = ['data', 'below/above ratio']
    #print('(higher ratio = more sellers and vice versa)')
    #print()
    #print(tabulate(rows, headers))
    return ratios

def plotter1(stock_list):
    for s in tqdm(stock_list):
        ratios = specific_stock1(s)
        x = list(range(len(ratios)))
        y = ratios
        plt.plot(x, y, label = s)
    plt.xlabel('day (starting from 5/05 ending at 5/19)')
    plt.ylabel('ratio ()')
    plt.title('ratio for selling vs buying calls')
    plt.legend()
    plt.show()
#plotter1(earnings7days()[:3])

def specific_stock2(stock):
    def sell_or_buy(filename):
        sells = 0
        buys = 0
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                symbol = row[1]
                type = row[6]
                if symbol == stock and type == 'CALL': ### conditions
                    trade_price = float(row[14])
                    bid = float(row[16])
                    ask = float(row[17])
                    if bid == ask:
                        continue
                    notional = float(row[19])
                    if notional < 50000:
                        continue
                    if trade_price < bid + (ask - bid)/5:
                        sells += 1
                    elif trade_price > ask - (ask - bid)/5:
                        buys += 1
        return sells, buys
    results = [[],[]] ### list of sells and buys (for all the dates)
    for f in tqdm(filenames):
        s, b = sell_or_buy(f + '.csv')
        results[0].append(s)
        results[1].append(b)
    return results

def plotter2(stock):
    sells, buys = specific_stock2(stock)
    scoring = []
    for i in range(len(sells)):
        scoring.append((buys[i]/(sells[i] + 1) - 1) * 10)
    x = list(range(len(sells)))
    plt.plot(x, sells, label = "selling trades")
    plt.plot(x, buys, label = "buying trades")
    plt.plot(x, scoring, label = "(buy/sell ratio - 1) x 10")
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.xlabel('day (starting from 5/05 ending at 5/19)')
    plt.ylabel('y')
    plt.title(stock + ' call block trades: sells vs buys')
    plt.legend()
    plt.show()
#plotter2("NVDA")

"""
with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    for tick in tickers[1:]:
        writer.writerow([tick])
"""
