import csv
import time
from tqdm import tqdm
from tabulate import tabulate
from combiner import grouped_attributes
start = time.time()
filenames = ['OptionTradeScreenerResults_20200505', 'OptionTradeScreenerResults_20200507',
    'OptionTradeScreenerResults_20200508', 'OptionTradeScreenerResults_20200511', 'OptionTradeScreenerResults_20200512',
    'OptionTradeScreenerResults_20200513', 'OptionTradeScreenerResults_20200514', 'OptionTradeScreenerResults_20200515',
    'OptionTradeScreenerResults_20200518', 'OptionTradeScreenerResults_20200519', 'OptionTradeScreenerResults_20200520',
    'OptionTradeScreenerResults_20200521', 'OptionTradeScreenerResults_20200522', 'OptionTradeScreenerResults_20200526',
    'OptionTradeScreenerResults_20200527', 'OptionTradeScreenerResults_20200528', 'OptionTradeScreenerResults_20200529',
    'OptionTradeScreenerResults_20200601', 'OptionTradeScreenerResults_20200602', 'OptionTradeScreenerResults_20200603',
    'OptionTradeScreenerResults_20200604', 'OptionTradeScreenerResults_20200605', 'OptionTradeScreenerResults_20200608',
    'OptionTradeScreenerResults_20200609', 'OptionTradeScreenerResults_20200610', 'OptionTradeScreenerResults_20200611',
    'OptionTradeScreenerResults_20200612', 'OptionTradeScreenerResults_20200615', 'OptionTradeScreenerResults_20200616',
    'OptionTradeScreenerResults_20200617', 'OptionTradeScreenerResults_20200618', 'OptionTradeScreenerResults_20200619']
#this function prints the symbols with most trades (any trade. ask, bid, notional don't matter) across all filenames
def symbol_counts(input): #returs dictionary mapping each symbol to counter for total number of buy trades
    output = {}
    table_format = []
    print("counting symbols...")
    for filename in tqdm(input):
        with open(filename + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                #conditional stuff for filtering out non-buys
                if row == [] or row[14] == 'Trade Price':
                    continue
                spot = float(row[8])
                trade_price = float(row[14])
                bid = float(row[16])
                ask = float(row[17])
                if bid == ask or trade_price < ask - (ask - bid)*0.41 or spot == 0:
                    continue
                if row[1] in output:
                    output[row[1]] += 1
                else:
                    output[row[1]] = 1
    output = sorted(output.items(), key=lambda x: x[1], reverse = True)
    with open('symbol_counts.csv', 'w') as f:
        writer = csv.writer(f)
        i = 0
        for symbol, count in output:
            writer.writerow([symbol, count])
            if i < 50:
                table_format.append([symbol, count])
            i += 1
    headers = ['symbol', 'count']
    print(tabulate(table_format, headers))
    print("number of distinct symbols: ", i)
#symbol_counts(filenames)

def read_symbols():
    rows = []
    with open('symbol_counts.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            rows.append(row)
            if row[0] == 'VXX':
                break
    headers = ['symbols', 'Counts']
    symbols_shit = [
        [(1, " != '@@@@'"), (1, " != '@@@@'")] #this is base case that excludes no symbols
    ]
    big_string = ""
    for r in rows:
        symbols_shit.append([(1, " == '" + r[0] + "'"), (1, " != '@@@@'")])
        big_string += "'" + str(r[0]) + "', "
    symbols_shit.append([(1, " not in [" + big_string[:-2] + "]"), (1, " != '@@@@'")])
    #print("the 'not in key symbols' conditional:", symbols_shit[-1])
    #print('number of key symbols: ', len(rows))
    #print()
    return symbols_shit

symbol_conditionals_list = read_symbols()
days_to_exp_list = [
    [(24, '<=4'), (24, '<=4')],
    [(24, '>4'), (24, '<=9')],
    [(24, '>9'), (24, '<=14')],
    [(24, '>14'), (24, '<=19')],
    [(24, '>19'), (24, '<=24')],
    [(24, '>24'), (24, '<=29')],
    [(24, '>29'), (24, '<=34')],
    [(24, '>34'), (24, '<=39')],
    [(24, '>39'), (24, '<=44')],
    [(24, '>44'), (24, '<=49')],
    [(24, '>49'), (24, '<=54')],
    [(24, '>54'), (24, '<=59')],
    [(24, '>59'), (24, '<=64')],
    [(24, '>64'), (24, '<=69')],
    [(24, '>69'), (24, '<=74')],
    [(24, '>74'), (24, '<=79')],
    [(24, '>79'), (24, '<=84')],
    [(24, '>84'), (24, '<=89')],
    [(24, '>89'), (24, '<=94')],
    [(24, '>94'), (24, '<=99')],
    [(24, '>99'), (24, '<=104')],
    [(24, '>104'), (24, '<=109')],
    [(24, '>109'), (24, '<=114')],
    [(24, '>114'), (24, '<=124')],
    [(24, '>124'), (24, '<=134')],
    [(24, '>134'), (24, '<=139')],
    [(24, '>139'), (24, '<=144')],
    [(24, '>144'), (24, '<=149')],
    [(24, '>149'), (24, '<=154')],
    [(24, '>154'), (24, '<=159')],
    [(24, '>159'), (24, '<=164')],
    [(24, '>164'), (24, '<=169')],
    [(24, '>169'), (24, '<=174')],
    [(24, '>174'), (24, '<=179')],
    [(24, '>179'), (24, '<=274')],
    [(24, '>274'),(24, '<=409')],
    [(24, '>409'),(24, '<=414')],
    [(24, '>414'),(24, '<=419')],
    [(24, '>419'),(24, '<=424')],
    [(24, '>424'),(24, '<=429')],
    [(24, '>429'),(24, '>429')]
]
notionals_list = [
    [(12, '<=1000'), (12, '<=1000')],
    [(12, '>1000'), (12, '<=2500')],
    [(12, '>2500'), (12, '<=5000')],
    [(12, '>5000'), (12, '<=10000')],
    [(12, '>10000'), (12, '<=25000')],
    [(12, '>25000'), (12, '<=70000')],
    [(12, '>70000'), (12, '<=200000')],
    [(12, '>200000'), (12, '<=400000')],
    [(12, '>400000'), (12, '<=800000')],
    [(12, '>800000'), (12, '>800000')],
]
otm_list = [
    [(29, '<=-33'), (29, '<=-33')],
    [(29, '>-33'), (29, '<=-10')],
    [(29, '>-10'), (29, '<=-2')],
    [(29, '>-2'), (29, '<2')],
    [(29, '>=2'), (29, '<=10')],
    [(29, '>10'), (29, '<=20')],
    [(29, '>20'), (29, '<=33')],
    [(29, '>33'), (29, '<=50')],
    [(29, '>50'), (29, '<=66')],
    [(29, '>66'), (29, '<=100')],
    [(29, '>100'), (29, '<=150')],
    [(29, '>150'), (29, '>150')]
]
types = [
    [(3, " == 'CALL'"), (3, " == 'CALL'")],
    [(3, " == 'PUT'"), (3, " == 'PUT'")]
]
"""
list_of_lists = [symbol_conditionals_list, days_to_exp_list, notionals_list, otm_list, types]
count = 1
for i in range(len(list_of_lists)):
    count *= len(list_of_lists[i])
print("total number of combinations: ", count)
"""

def write():
    with open('attributes_newest.csv', 'w') as f:
        writer = csv.writer(f)
        for x in tqdm(symbol_conditionals_list):
            writer.writerow(grouped_attributes(x))
#write()

def read():
    rows = []
    with open('attributes_newest.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == [] or float(row[1]) == 0:
                continue
            rows.append(row)
    #sorted_rows = sorted(rows, key=lambda r: float(r[3]))
    sorted_rows = sorted(rows, key=lambda r: float(r[2]))
    headers = ['Attributes', '#of satisfying trades', 'top2/3 G/L ratio', 'notional return %']
    print(tabulate(sorted_rows, headers))
read()

print("time elapsed:", time.time() - start)
