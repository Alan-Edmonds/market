import csv
from tabulate import tabulate
from operator import itemgetter
filenames = ['OptionTradeScreenerResults_20200511','OptionTradeScreenerResults_20200512', 'OptionTradeScreenerResults_20200513',
    'OptionTradeScreenerResults_20200514', 'OptionTradeScreenerResults_20200515', 'OptionTradeScreenerResults_20200518',
    'OptionTradeScreenerResults_20200519', 'OptionTradeScreenerResults_20200520', 'OptionTradeScreenerResults_20200521',
    'OptionTradeScreenerResults_20200522']

def find_ticker(ticker, expiry, type):
    trade_day = 11 #not absolutely necessary
    relative_trade_day = 0
    relevant = []
    for filename in filenames:
        this_file = []
        with open(filename + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == ticker and row[5][:5] == expiry and row[6] == type:
                    this_file.append(row[0:2] + row[5:8] + [(row[16] + row[17])/2] + ['5/' + str(trade_day)] +
                        [float(row[0][:2])*10000 + float(row[0][3:5])*100 + float(row[0][6:8]) + relative_trade_day*67000])
            this_file = sorted(this_file, key=itemgetter(0))    #sort trades within each file by the trade timestamp
            for row in this_file:                               #then adds the sorted list to all_trades, row by row
                relevant.append(row)
        relative_trade_day += 1
        if trade_day == 15:
            trade_day += 3
        else:
            trade_day += 1
    headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Mid', 'Date of Trade', 'Time Score']
    print(tabulate(all_trades, headers))
    return relevant
find_ticker('ZM', '6/5/', 'CALL')

"""
def separate_strikes(rows):
    strike_dict = {} #dictionary where each strike price is mapped to a list of trades at that strike
    for row in rows:
        if row[7] in strikes:
            strike_dict[row[7]].append(row)
        else:
            strike_dict[row[7]] = [(row[0], row[5]]
    for strike in strike_dict:
        if len(strike_dict.get(strike)) < 5:
            strike_dict.pop(strike)



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
"""
