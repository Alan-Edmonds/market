import csv
from tabulate import tabulate
from operator import itemgetter
upcoming = ['upcoming522.csv']
previous = ['OptionTradeScreenerResults_20200518.csv', 'OptionTradeScreenerResults_20200519.csv',
    'OptionTradeScreenerResults_20200520.csv', 'OptionTradeScreenerResults_20200521.csv', 'OptionTradeScreenerResults_20200522.csv']

def relevant_expiry(filename): #change 'key lines' to change the relevant expirations
    relevant = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            if row[1] == 'CGC':
                relevant.append(row)
    return relevant

def buys_sells(rows):
    buys = []
    sells = []
    buys_ticker_counts = {}
    sells_ticker_counts = {}
    for row in rows:
        trade_price = float(row[14])
        bid = float(row[16])
        ask = float(row[17])
        if bid == ask:
            continue
        if trade_price > ask - (ask - bid)/4:
            buys.append(row)
            if row[1] in buys_ticker_counts:
                buys_ticker_counts[row[1]] += 1
            else:
                buys_ticker_counts[row[1]] = 1
        if trade_price < bid + (ask - bid)/4:
            sells.append(row)
            if row[1] in sells_ticker_counts:
                sells_ticker_counts[row[1]] += 1
            else:
                sells_ticker_counts[row[1]] = 1
    return buys, sells, buys_ticker_counts, sells_ticker_counts

def otm(rows):
    otm = []
    ticker_counts = {}
    for row in rows:
        strike = float(row[7])
        spot = float(row[8])
        if row[6] == 'CALL':
            if strike - spot > max(0.05*spot, 2): #if difference between strike and spot is >5% otm and >2
                otm.append(row)
                if row[1] in ticker_counts:
                    ticker_counts[row[1]] += 1
                else:
                    ticker_counts[row[1]] = 1
        if row[6] == 'PUT':
            if spot - strike > max(0.05*spot, 2):
                otm.append(row)
                if row[1] in ticker_counts:
                    ticker_counts[row[1]] += 1
                else:
                    ticker_counts[row[1]] = 1
    return otm, ticker_counts

def table(filename, otm_bool, buy_bool):
    print()
    print("otm? ", otm_bool, "   buys? ", buy_bool)
    buys, sells, buys_ticker_counts, sells_ticker_counts = buys_sells(relevant_expiry(filename))
    if otm_bool:
        buys, buys_ticker_counts = otm(buys)
        sells, sells_ticker_counts = otm(sells)
    cherry_picked = []
    if buy_bool:
        print({k: v for k, v in sorted(buys_ticker_counts.items(), key=lambda item: -1*item[1])})
        print()
        for row in buys:
            cherry_picked.append(row[:2] + row[5:10] + row[13:15] + row[16:18] + row[19:21] + row[23:24] + row[31:34] + [row[len(row) - 1]])
    elif not buy_bool:
        print({k: v for k, v in sorted(sells_ticker_counts.items(), key=lambda item: -1*item[1])})
        print()
        for row in sells:
            cherry_picked.append(row[:2] + row[5:10] + row[13:15] + row[16:18] + row[19:21] + row[23:24] + row[31:34] + [row[len(row) - 1]])
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot Price', 'Open Int.', 'Trade Qty', 'Trade Price', 'Bid', 'Ask',
        'Notional', 'Side', 'Option Return %', 'Exch.', 'Condition', 'Execution', 'Date of Trade']
    print(tabulate(cherry_picked, headers))

def days_separately():
    for f in upcoming:
    #for f in previous:
        print(str(f))
        table(f, True, True)
        print()
        print()
        print()
#days_separately()

def combined():
    data = []
    trade_day = 18 ### change this with different data
    for filename in upcoming:
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                row.append('5/' + str(trade_day))
                data.append(row)
        trade_day += 1
    sorted_data = sorted(data, key=itemgetter(1))
    with open('combined.csv', 'w') as f:
        writer = csv.writer(f)
        for row in sorted_data:
            writer.writerow(row)
    print('combined.csv')
    table('combined.csv', True, True) #otm buys
    table('combined.csv', False, False) #sells (itm, otm, atm)
combined()
