import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
from operator import itemgetter
from tqdm import tqdm
filenames = ['OptionTradeScreenerResults_20200511','OptionTradeScreenerResults_20200512', 'OptionTradeScreenerResults_20200513',
    'OptionTradeScreenerResults_20200514', 'OptionTradeScreenerResults_20200515', 'OptionTradeScreenerResults_20200518',
    'OptionTradeScreenerResults_20200519', 'OptionTradeScreenerResults_20200520', 'OptionTradeScreenerResults_20200521',
    'OptionTradeScreenerResults_20200522']

def find_ticker(ticker, type):
    trade_day = 11 #not absolutely necessary
    relative_trade_day = 0
    relevant = []
    for filename in tqdm(filenames):
        this_file = []
        with open(filename + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == ticker and row[6] == type and row[5][0] == '6': #only look at june expiries
                    this_file.append(row[0:2] + row[5:8] + [(float(row[16]) + float(row[17]))/2] + [row[19]] + ['5/' + str(trade_day)] +
                        [float(row[0][:2])*10000 + float(row[0][3:5])*100 + float(row[0][6:8]) + relative_trade_day*67000])
            this_file = sorted(this_file, key=itemgetter(0))    #sort trades within each file by the trade timestamp
            for row in this_file:                               #then adds the sorted list to all_trades, row by row
                relevant.append(row)
        relative_trade_day += 1
        if trade_day == 15:
            trade_day += 3
        else:
            trade_day += 1
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Mid', 'Notional', 'Date of Trade', "Time 'Score'"]
    print(tabulate(relevant, headers))
    return relevant
#find_ticker('ZM', 'CALL')

def graphable_data(rows):
    dict = {} #dictionary where each (expiry, strike price) tuple is mapped to a list of trade params (listed in 'headers' from above) at that strike
    for row in rows:
        specific_option = (row[2], row[4])
        if specific_option in dict:
            dict[(row[2], row[4])].append(row)
        else:
            dict[specific_option] = [row]
    non_trivial = {}
    for specific_option in dict: #only look at (expiry date, strike price) combinations that had more than 5 trades
        if len(dict.get(specific_option)) > 3:
            non_trivial[specific_option] = dict.get(specific_option)
    return non_trivial

def plotter(stock, type):
    dict = graphable_data(find_ticker(stock, type))
    for expiry, strike in dict:
        data_list = dict.get((expiry, strike))
        x = []
        y = []
        for row in data_list:
            x.append(row[8])
            y.append(row[5])
        plt.plot(x, y, label = str(expiry) + " $" + str(strike))
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.xlabel('relative time')
    plt.ylabel('mid')
    plt.title(stock + ' ' + type + ' options pricing')
    plt.legend()
    plt.show()
plotter('MDB', 'CALL')
plotter('MDB', 'PUT')
