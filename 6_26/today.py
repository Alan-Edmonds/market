import csv
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
    trade_day = 626
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
#all_combiner(['OptionTradeScreenerResults_20200608', 'OptionTradeScreenerResults_20200609', 'OptionTradeScreenerResults_20200610', 'OptionTradeScreenerResults_20200611', 'OptionTradeScreenerResults_20200612'])
all_combiner(['OptionTradeScreenerResults_20200626'])

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
            symbol = row[1]
            days_to_exp = int(row[24])
            otm = float(row[29])
            trade_price = float(row[7])
            satisfies = False
            """
            conditions = [(days_to_exp > 79)]
            for c in conditions:
                if eval(str(c)):
                    satisfies = True
            """
            if days_to_exp == 4 or days_to_exp == 9:
                if trade_price < 0.2:
                    if symbol in ['TWTR', 'SPY', 'MGM', 'SNAP', 'TLRY', 'DAL', 'WFC', 'PCG', 'AMD', 'AAPL', 'UNG', 'CRON', 'PFE', 'TSLA', 'VZ']:
                        satisfies = True
            if satisfies:
                rows.append(row[:8] + row[9:11] + [row[12]] + row[24:27] + [row[29]])
    sorted_rows = sorted(rows, key=lambda r: r[1])
    #sorted_rows = sorted(rows, key=lambda r: float(r[10]))
    #sorted_rows = sorted(rows, key=lambda r: r[11])
    #sorted_rows = sorted(rows, key=lambda r: float(r[14]))
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'Bid', 'Ask', 'Notional',
        'Days2Exp.', 'Qty.vsOI', 'Date', '% OTM']
    print(tabulate(sorted_rows, headers))
    print("------  --------  ---------  ------  --------  -------  -----  ----------  -----  -----  ----------  -----------  ----------  ------  -------")
    print("Time    Symbol    Expiry     Type      Strike     Spot     OI    TrdPrice    Bid    Ask    Notional    Days2Exp.    Qty.vsOI  Date      % OTM")
    print("num of rows:", len(sorted_rows))

    options = {}
    for row in sorted_rows:
        hash = (row[1], row[2])
        if hash in options.keys():
            if row[3] == 'CALL':
                tuple = (options.get(hash)[0] + 1, options.get(hash)[1])
            else:
                tuple = (options.get(hash)[0], options.get(hash)[1] + 1)
            options[hash] = tuple
        else:
            options[hash] = (0, 0)

    table_rows = []
    for opt in options:
        calls = options.get(opt)[0]
        puts = options.get(opt)[1]
        if calls >= 5 or puts >= 5:
            if calls == 0:
                calls = 0.0001
            if puts == 0:
                puts = 0.0001
            ratio = max(calls/puts, puts/calls)
            table_rows.append([opt, calls, puts, ratio])
    sorted_table = sorted(table_rows, key=lambda r: r[3])
    these_headers = ['option', 'calls', 'puts', 'max ratio']
    print(tabulate(sorted_table, these_headers))
    print("num of rows:", len(sorted_table))

    #moves: agnc calls, auy calls, azn calls,
    """
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
    """
newest_scan()

#qqq:
#   <0.1, ==9
#   0.1-0.2, ==3, ==4, ==2
#wfc:
#   0.1-0.2, ==3, ==2,
#   <0.1, ==2, ==4
"""
Attributes                                                                                               #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'QQQ'                                                                            14           2.5                     93.918
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'SPY'                                                                           241           2.30137                336.153
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'VXX'                                                           7           1.33333                458.435
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'VXX'                                                                           122           1.21818                237.248
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'QQQ'                                                         100           1.08333                182.18
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'QQQ'                                                          95           1.02128                129.18
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'SPY'                                                         134           0.970588               152.199
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'WFC'                                                          74           0.85                   428.172
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'AAPL'                                                                           27           0.8                    195.299
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'WFC'                                                                           102           0.728814               237.695
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'QQQ'                                                         131           0.723684               262.06
TrdPrice< 0.1,   Days2Exp.==9,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       1305           0.701434               153.712
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'VXX'                                                          44           0.692308               323.217
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'WFC'                                                                            96           0.684211               338.605
TrdPrice< 0.1,   Days2Exp.==4,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       5207           0.594793               241.21
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'WFC'                                                          82           0.54717                196.164
TrdPrice< 0.1,   Days2Exp.==3,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       4950           0.529194               237.75
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     5891           0.493661               166.652
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     6437           0.476715               185.051
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     1939           0.461191               155.035
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     6214           0.459371               177.754
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'SPY'                                                         557           0.443005               200.26
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'SPY'                                                                          1045           0.437414               194.466
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'VXX'                                                          52           0.405405               212.241
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'AAPL'                                                         21           0.4                    160.996
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'SPY'                                                         944           0.39645                273.84
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'WFC'                                                          96           0.391304               411.118
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'WFC'                                                                            25           0.388889               246.308
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'AAPL'                                                         91           0.378788               287.831
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'WFC'                                                                            74           0.37037                486.059
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'QQQ'                                                                            90           0.363636               139.119
TrdPrice< 0.1,   Days2Exp.==2,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       5981           0.356543               213.675
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'VXX'                                                                            12           0.333333                30.897
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'SPY'                                                                           699           0.311445                96.27
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'AAPL'                                                                          114           0.310345               266.47
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'QQQ'                                                                            74           0.298246                84.395
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'SPY'                                                        1611           0.273518               156.66
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'WFC'                                                          24           0.263158               166.22
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'AAPL'                                                        163           0.253846               163.508
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'AAPL'                                                                          168           0.253731               145.163
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'QQQ'                                                                           106           0.247059                98.262
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'VXX'                                                                            73           0.216667                85.125
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'VXX'                                                          68           0.214286                99.302
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'SPY'                                                                          1836           0.210283               258.723
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'QQQ'                                                           9           0.125                   61.847
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'AAPL'                                                        200           0.123596                70.554
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'AAPL'                                                                          198           0.0879121               59.396
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'VXX'                                                                            39           0.0833333              153.676
above table for: good_with_symbol.csv
"""


#fridays: qqq:
"""
Attributes                                                                                               #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'QQQ'                                                                             3            1e+10                 127.182
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'AAPL'                                                                           19            8.5                   149.556
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'QQQ'                                                          49            4.44444               163.317
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'SPY'                                                                            91            1.93548               160.813
TrdPrice< 0.1,   Days2Exp.==5,   Symbol == 'QQQ'                                                                             5            1.5                    32.934
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'SPY'                                                          97            1.48718                87.366
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'VXX'                                                           7            1.33333               248.499
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'WFC'                                                                            52            1.16667               266.356
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'QQQ'                                                                            36            1.11765                76.007
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'QQQ'                                                          64            1.06452               398.882
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'VXX'                                                          26            1                     296.175
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'AAPL'                                                         56            1                     343.826
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol == 'SPY'                                                         464            1                     136.673
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'AAPL'                                                         12            1                     127.153
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'QQQ'                                                          39            0.857143              -35.379
TrdPrice< 0.1,   Days2Exp.==9,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                        922            0.769674               59.793
TrdPrice< 0.1,   Days2Exp.==5,   Symbol == 'WFC'                                                                            28            0.75                  116.301
TrdPrice< 0.1,   Days2Exp.==5,   Symbol == 'SPY'                                                                           362            0.72381                66.871
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'WFC'                                                          53            0.709677              291.542
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol == 'AAPL'                                                         38            0.652174              185.866
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'QQQ'                                                                            31            0.631579              141.779
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'SPY'                                                                           308            0.62963                31.156
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'VXX'                                                                             8            0.6                   -42.72
TrdPrice< 0.1,   Days2Exp.==4,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       2792            0.598168              124.986
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol == 'VXX'                                                          19            0.583333               92.444
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol == 'QQQ'                                                          19            0.583333              -57.909
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     3521            0.568374               78.272
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'SPY'                                                                           505            0.568323              114.744
TrdPrice< 0.1,   Days2Exp.==5,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       2174            0.565155               60.846
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'QQQ'                                                                            25            0.5625                 10.195
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'VXX'                                                                            45            0.551724              244.306
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'SPY'                                                         515            0.537313              271.852
TrdPrice< 0.1,   Days2Exp.==4,   Symbol == 'AAPL'                                                                           81            0.528302              222.813
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     1565            0.525341               39.245
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol == 'WFC'                                                          32            0.52381               155.948
TrdPrice< 0.1,   Days2Exp.==5,   Symbol == 'AAPL'                                                                           32            0.52381                 6.793
TrdPrice< 0.1,   Days2Exp.==3,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       2547            0.523325              139.999
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     2671            0.508187               47.29
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'VXX'                                                          37            0.48                  141.444
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4,   Symbol == 'SPY'                                                         279            0.47619               114.411
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     3612            0.457039               92.963
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'VXX'                                                                            40            0.428571              -30.267
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'WFC'                                                          34            0.416667              236.516
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                     3590            0.408395               73.61
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'WFC'                                                                            65            0.382979               46.852
TrdPrice< 0.1,   Days2Exp.==2,   Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']                                       3315            0.369269              110.976
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'WFC'                                                          18            0.285714               10.068
TrdPrice< 0.1,   Days2Exp.==9,   Symbol == 'WFC'                                                                            18            0.285714               69.549
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'SPY'                                                                           960            0.283422              218.862
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'WFC'                                                          56            0.244444               37.46
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'SPY'                                                         959            0.227913               25.457
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3,   Symbol == 'AAPL'                                                        120            0.22449                13.186
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'VXX'                                                          34            0.214286              -43.542
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'WFC'                                                                            42            0.2                   276.348
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'AAPL'                                                                          117            0.193878               18.024
TrdPrice< 0.1,   Days2Exp.==5,   Symbol == 'VXX'                                                                            44            0.157895               60.196
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2,   Symbol == 'AAPL'                                                        113            0.153061              -42.762
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9,   Symbol == 'QQQ'                                                           9            0.125                 -27.93
TrdPrice< 0.1,   Days2Exp.==2,   Symbol == 'AAPL'                                                                          133            0.108333              -55.569
TrdPrice< 0.1,   Days2Exp.==3,   Symbol == 'VXX'                                                                            35            0.09375                30.111
above table for: good_with_symbol.csv
"""
