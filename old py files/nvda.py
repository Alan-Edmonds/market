import csv
import math
import matplotlib.pyplot as plt
from tabulate import tabulate
from tqdm import tqdm

def printer():
    data = []
    with open('OptionTradeScreenerResults_20200518.csv') as f:
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
#printer()

def specific_dates():
    nvda = []
    def read_file(filename):
        nvda = []
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                symbol = row[1]
                if symbol == 'NVDA':
                    notional = float(row[19])
                    if notional > 75000:
                        nvda.append(row)
    for filename in ['OptionTradeScreenerResults_20200518.csv', 'OptionTradeScreenerResults_20200519.csv', 'OptionTradeScreenerResults_20200520.csv']:
        read_file(filename)
    return nvda

def expiry_filter(trades):
    exp522 = ([], [])
    exp529 = ([], [])
    expJune = ([], [])
    for row in trades:
        i = 0
        if row[6] == 'PUT':
            i = 1
        if row[5][:4] == '5/22':
            exp522[i].append(row)
        elif row[5][:4] == '5/29':
            exp529[i].append(row)
        elif row[5][:1] == '6':
            expJune[i].append(row)
    return exp522, exp529, expJune

def buysell_filter(one_expiry_calls_or_puts):
    buys = []
    sells = []
    for row in one_expiry_calls_or_puts:
        trade_price = float(row[14])
        bid = float(row[16])
        ask = float(row[17])
        if bid == ask:
            continue
        if trade_price > ask - (ask - bid)/4:
            buys.append(row)
        elif trade_price < bid + (ask - bid)/4:
            sells.append(row)
    return buys, sells

def strike_filter(trades):
    strike_counts = {}
    for row in trades:
        if row[7] in strike_counts:
            strike_counts[row[7]] += 1
        else:
            strike_counts[row[7]] = 1
    sorted_dict = {k: v for k, v in sorted(strike_counts.items(), key=lambda item: item[0])}
    list_form = []
    for k in sorted_dict:
        list_form.append((k, sorted_dict[k]))
    headers = ['strike', '# of trades']
    print(tabulate(list_form, headers))
    print()

def run():
    nvda = specific_dates()
    exp522, exp529, expJune = expiry_filter(nvda)
    lets_look_at = [exp522, exp529, expJune]
    exps = ['5/22', '5/29', 'june']
    index = 0
    for expiry in lets_look_at:
        call_buys, call_sells = buysell_filter(expiry[0])
        print(exps[index], 'call buys')
        strike_filter(call_buys)
        print(exps[index], 'call sells')
        strike_filter(call_sells)
        print()

        put_buys, put_sells = buysell_filter(expiry[1])
        print(exps[index], 'put buys')
        strike_filter(put_buys)
        print(exps[index], 'put sells')
        strike_filter(put_sells)
        print()
run()
