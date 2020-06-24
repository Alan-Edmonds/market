cd import csv
import math
import statistics as stats
import numpy
import time
from tabulate import tabulate
from tqdm import tqdm
from operator import itemgetter

def all_combiner(input): #this writes the combined.csv, which is all of the block trades near ask from all the input files
    data = []
    #trade_day = 505
    trade_day = 623
    #relative_trade_day = 0  #don't really need this, because of the Days To Exp param
    print("Reading today's csv...")
    for filename in tqdm(input):
        with open(filename + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == [] or row[14] == 'Trade Price':
                    continue
                important = [0, 1, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 28, 29, 30, 32, 33, 34, 35, 37, 38, 39, 40, 43, 47]
                trimmed_row = []
                for i in important:
                    if i in [0, 32, 33]:
                        trimmed_row.append(row[i][:5]) #trimming certain excessively long strings
                        continue
                    if i in [38, 40]:
                        if row[i] == '':
                            trimmed_row.append('')
                        else:
                            trimmed_row.append(100*float(row[i])) #converted to percent value
                        continue
                    trimmed_row.append(row[i])
                trimmed_row.append(str(trade_day)[0] + '/' + str(trade_day)[1:]) #appending Day of Trade
                """
                trimmed_row.append(relative_trade_day)
                relative_time = flt(row[0][:2])*10000 + flt(row[0][3:5])*100 + flt(row[0][6:8]) + relative_trade_day*67000
                trimmed_row.append(relative_time)
                """
                data.append(trimmed_row)
                #data.append(row)
        #day of trade conditional bullshit:
        if trade_day == 505:
            trade_day += 2
        elif trade_day in [508, 515, 605, 612, 619]: #continually updatee with new fridays. The other conditionals for edge cases
            trade_day += 3
        elif trade_day == 522:
            trade_day += 4
        elif trade_day == 529:
            trade_day = 601
        else:
            trade_day += 1
        #relative_trade_day += 1
    with open('today1.csv', 'w') as f:
        writer = csv.writer(f)
        print("writing data into today1.csv...")
        for row in tqdm(data):
            writer.writerow(row)
all_combiner(['OptionTradeScreenerResults_20200608',
'OptionTradeScreenerResults_20200609', 'OptionTradeScreenerResults_20200610', 'OptionTradeScreenerResults_20200611',
'OptionTradeScreenerResults_20200612'])
#all_combiner(['OptionTradeScreenerResults_20200623'])

def filter_buys():
    rows = []
    print("Reading today1.csv...")
    with open('today1.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            # bid/ask stuff
            trade_price = float(row[7])
            bid = float(row[9])
            ask = float(row[10])
            spread = float(row[19])
            strike = float(row[4])
            spot = float(row[5])
            type = row[3]
            if bid == ask or trade_price < ask - spread*0.41 or spot == 0: #filtering out non-buys. Right now 'buys' are upper 41% of bid/ask spread
                continue
            row.append(round(spread/(bid/2 + ask/2), 4)) #bid-ask spread divided by mid
            row.append(round(100*(trade_price - bid)/spread, 2)) #bid/ask percentile of the buy
            # %OTM stuff
            if type == 'CALL':
                row.append(round(100*(strike - spot)/spot, 2))
            elif type == 'PUT':
                row.append(round(100*(spot - strike)/spot, 2))
            if row[20] != '' and row[22] != '':
                IV20day = float(row[20])
                IV1year = float(row[22])
                row.append(round(IV20day/IV1year, 2))
            else:
                row.append('')
            rows.append(row)
    with open('today2.csv', 'w') as f:
        writer = csv.writer(f)
        print("writing data into today2.csv...")
        for row in tqdm(rows):
            writer.writerow(row)
filter_buys()

def scan1():
    rows = []
    print("Making today's table...")
    with open('today2.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            otm = float(row[29])
            days_to_exp = int(row[24])
            if row[1] not in ['SPY', 'QQQ', 'IWM'] and otm > 230 and otm < 300 and days_to_exp > 5:
                rows.append(row[:13] + row[16:18] + row[24:27] + [row[29]])
    sorted_rows = sorted(rows, key=lambda r: r[1])
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'B.Size', 'Bid', 'Ask', 'A.Size', 'Notional',
        'Cond.', 'Exec.', 'Days2Exp.', 'Qty.vsOI', 'Date', '% OTM']
    print(tabulate(sorted_rows, headers))
#scan1()

def new_scan():
    rows = []
    print("Making today's table...")
    with open('today2.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            days_to_exp = int(row[24])
            satisfies = False
            conditions = [(days_to_exp > 29 and days_to_exp <= 34), (days_to_exp > 54 and days_to_exp <= 59), (days_to_exp > 74 and days_to_exp <= 79),
                (days_to_exp > 79 and days_to_exp <= 84), (days_to_exp > 109 and days_to_exp <= 114), (days_to_exp > 114 and days_to_exp <= 124),
                (days_to_exp > 154 and days_to_exp <= 159), (days_to_exp > 159 and days_to_exp <= 164), (days_to_exp > 174 and days_to_exp <= 179),
                (days_to_exp > 414 and days_to_exp <= 419), (days_to_exp > 419 and days_to_exp <= 424), (days_to_exp > 424 and days_to_exp <= 429),
                (days_to_exp > 429)]
            for c in conditions:
                if eval(str(c)) and float(row[12]) < 2500 and float(row[29]) > 66:
                    satisfies = True
            if satisfies:
                rows.append(row[:8] + row[9:11] + [row[12]] + row[24:27] + [row[29]])
    sorted_rows = sorted(rows, key=lambda r: r[0])
    #sorted_rows = sorted(rows, key=lambda r: float(r[10]))
    #sorted_rows = sorted(rows, key=lambda r: r[11])
    #sorted_rows = sorted(rows, key=lambda r: float(r[14]))
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'Bid', 'Ask', 'Notional',
        'Days2Exp.', 'Qty.vsOI', 'Date', '% OTM']
    print(tabulate(sorted_rows, headers))
#new_scan()

def newest_scan():
    rows = []
    print("Making today's table...")
    with open('today2.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            days_to_exp = int(row[24])
            satisfies = False
            conditions = [(days_to_exp > 79)]
            for c in conditions:
                if eval(str(c)):
                    satisfies = True
            if satisfies:
                rows.append(row[:8] + row[9:11] + [row[12]] + row[24:27] + [row[29]])
    sorted_rows = sorted(rows, key=lambda r: r[1])
    #sorted_rows = sorted(rows, key=lambda r: float(r[10]))
    #sorted_rows = sorted(rows, key=lambda r: r[11])
    #sorted_rows = sorted(rows, key=lambda r: float(r[14]))
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'Bid', 'Ask', 'Notional',
        'Days2Exp.', 'Qty.vsOI', 'Date', '% OTM']
    #print(tabulate(sorted_rows, headers))
    print()
    calls_and_puts = {}
    for r in sorted_rows:
        if r[1] in calls_and_puts:
            if r[3] == 'CALL':
                calls_and_puts[r[1]][0] += 1
            elif r[3] == 'PUT':
                calls_and_puts[r[1]][1] += 1
        else:
            if r[3] == 'CALL':
                calls_and_puts[r[1]] = [1, 0]
            elif r[3] == 'PUT':
                calls_and_puts[r[1]] = [0, 1]
    ticker_counts = []
    for ticker in calls_and_puts:
        c_p = calls_and_puts.get(ticker)
        if c_p[1] == 0:
            c_p[1] = 0.00001
        ticker_counts.append((ticker, c_p[0], c_p[1], c_p[0] + c_p[1], c_p[0]/c_p[1]))
    sorted_by_total = sorted(ticker_counts, key=lambda r: r[3])
    headers2 = ['Ticker', 'Calls', 'Puts', 'total calls/puts', 'call/put ratio']
    print(tabulate(sorted_by_total, headers2))
newest_scan()
