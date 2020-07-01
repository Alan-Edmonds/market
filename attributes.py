import csv
import time
from tqdm import tqdm
from tabulate import tabulate
#from original_combiner import grouped_attributes as ga1
#from recent_combiner import grouped_attributes as ga2
start = time.time()
filenames = ['505', '507', '508', '511', '512', '513', '514', '515', '518', '519', '520', '521', '522',
    '526', '527', '528', '529', '601', '602', '603', '604', '605', '608', '609', '610', '611',
    '612', '615', '616', '617', '618', '619', '622', '623', '624', '625', '626', '629', '630']
#this function prints the symbols with most trades (any trade. ask, bid, notional don't matter) across all filenames
def symbol_counts(input): #returs dictionary mapping each symbol to counter for total number of buy trades
    output = {}
    table_format = []
    print("counting symbols...")
    for d in tqdm(input):
        with open('OptionTradeScreenerResults_2020' + '0' + d + '.csv') as f:
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
            table_format.append([symbol, count])
            i += 1
            if symbol == 'VXX':
                break
    headers = ['symbol', 'count']
    print(tabulate(table_format, headers))
    print("number of distinct symbols: ", i)
symbol_counts(filenames)

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

"""
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
symbols_shit = read_symbols()
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
    [(24, '>54'), (24, '<=69')],
    [(24, '>69'), (24, '<=74')],
    [(24, '>74'), (24, '<=84')],
    [(24, '>84'), (24, '<=94')],
    [(24, '>94'), (24, '<=134')],
    [(24, '>134'), (24, '<=154')],
    [(24, '>154'), (24, '<=159')],
    [(24, '>159'), (24, '<=169')],
    [(24, '>169'), (24, '<=274')],
    [(24, '>274'), (24, '>274')]
]
notionals_list = [
    [(12, '<=1000'), (12, '<=1000')],
    [(12, '>1000'), (12, '<=5000')],
    [(12, '>5000'), (12, '<=10000')],
    [(12, '>10000'), (12, '<=50000')],
    [(12, '>50000'), (12, '<=200000')],
    [(12, '>200000'), (12, '<=600000')],
    [(12, '>600000'), (12, '>600000')]
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
list_of_lists = [symbols_shit, days_to_exp_list, notionals_list, otm_list, types]
length_multiplicative = 1
length_sum = 0
for i in range(len(list_of_lists)):
    length_multiplicative *= len(list_of_lists[i])
    length_sum += len(list_of_lists[i])
#print("total number of combinations: ", length_multiplicative, "    total number of grouped_attributes() calls: ", length_sum)
everything_list = []
for L in list_of_lists:
    for x in L:
        everything_list.append(x)

combinations = []
for i in symbols_shit:
    for j in days_to_exp_list:
        for k in notionals_list:
            combinations.append([(3, " == 'PUT'"), i[0], i[1], j[0], j[1], k[0], k[1]]) #adjustable: right now looking at what seems to work in terms of puts

def write(conditionals, filename1, filename2):
    """
    with open(filename1, 'w') as f:
        writer = csv.writer(f)
        for x in tqdm(conditionals):
            writer.writerow(ga1(x))
    """
    with open(filename2, 'w') as f:
        writer = csv.writer(f)
        for x in tqdm(conditionals):
            writer.writerow(ga2(x))
#write(combinations, 'attribute_combos.csv')
#write(everything_list, 'attribute_basics.csv')
"""
write([
    [(24, " <= 9"), (29, '> 24'), (7, '> 0.10')],
    [(1, " == 'VXX'"), (24, " <= 9"), (29, '> 24'), (7, '> 0.10')],
    [(1, " == 'UVXY'"), (24, " <= 9"), (29, '> 24'), (7, '> 0.10')],
    [(1, " == 'VXX'"), (3, " == 'CALL'"), (24, " <= 9"), (29, '> 24'), (7, '> 0.10')],
    [(1, " == 'UVXY'"), (3, " == 'CALL'"), (24, " <= 9"), (29, '> 24'), (7, '> 0.10')]
], "risky.csv")

write([
    [(24, " <= 9"), (29, '> 24')],
    [(1, " == 'VXX'"), (24, " <= 9"), (29, '> 24')],
    [(1, " == 'UVXY'"), (24, " <= 9"), (29, '> 24')],
    [(1, " == 'VXX'"), (3, " == 'CALL'"), (24, " <= 9"), (29, '> 24')],
    [(1, " == 'UVXY'"), (3, " == 'CALL'"), (24, " <= 9"), (29, '> 24')]
], "risky_with_low_price.csv")

write([
    [(24, " <= 9"), (29, '> 24'), (7, '< 0.1')],
    [(24, " <= 9"), (29, '> 24'), (7, '>= 0.1'), (7, '<= 0.2')],
    [(24, " <= 9"), (29, '> 24'), (7, '> 0.2'), (7, '<= 0.5')],
    [(24, " <= 9"), (29, '> 24'), (7, '> 0.5'), (7, '<= 1')],
    [(24, " <= 9"), (29, '> 24'), (7, '> 1'), (7, '<= 2')],
    [(24, " <= 9"), (29, '> 24'), (7, '> 2')],

    [(7, '< 0.1')],
    [(7, '>= 0.1'), (7, '<= 0.2')],
    [(7, '> 0.2'), (7, '<= 0.5')],
    [(7, '> 0.5'), (7, '<= 1')],
    [(7, '> 1'), (7, '<= 2')],
    [(7, '> 2')]
], 'trade_prices1.csv', 'trade_prices2.csv')

write([
    [(7, '< 0.1')],
    [(7, '< 0.1'), (24, '<=4')],
    [(7, '< 0.1'), (24, '>4'), (24, '<=9')],
    [(7, '< 0.1'), (29, '>24'), (29, '<=45')],
    [(7, '< 0.1'), (29, '>45'), (29, '<90')],
    [(7, '< 0.1'), (29, '>=90')],
    [(7, '< 0.1'), (12, '<1100')],
    [(7, '< 0.1'), (12, '>=1100'), (12, '<5500')],
    [(7, '< 0.1'), (12, '>=5500'), (12, '<12000')],
    [(7, '< 0.1'), (12, '>=12000'), (12, '<75000')],
    [(7, '< 0.1'), (12, '>=75000')],
], 'cheap_all.csv', 'cheap_recent.csv')

write([
    [(1, " == 'VXX'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
    [(1, " == 'QQQ'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
    [(1, " == 'WFC'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
    [(1, " == 'SPY'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
    [(1, " == 'AAPL'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
    [(1, " not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) == 12")), (7, '< 0.2'), (24, '==5')],
], 'prettycheap_all.csv', 'prettycheap_recent.csv')
"""


"""
aa = [
    [(7, '< 0.2'), (24, '==2')],
    [(7, '< 0.2'), (24, '==3')],
    [(7, '< 0.2'), (24, '==4')],
    [(7, '< 0.2'), (24, '==5')],
    [(7, '< 0.2'), (24, '==9')],
    [(0, '>= 14'), (7, '< 0.2'), (24, '==2')],
    [(0, '>= 14'), (7, '< 0.2'), (24, '==3')],
    [(0, '>= 14'), (7, '< 0.2'), (24, '==4')],
    [(0, '>= 14'), (7, '< 0.2'), (24, '==5')],
    [(0, '>= 14'), (7, '< 0.2'), (24, '==9')]
]
bb = [(1, " == 'VXX'"), (1, " == 'QQQ'"), (1, " == 'WFC'"), (1, " == 'SPY'"), (1, " == 'AAPL'"), (1, " not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL']")]
products = []
for a_list in aa:
    for b_condition in bb:
        c = list.copy()
        c.append(b_condition)
        products.append(c)
"""
aa = [
    [(7, '< 0.2'), (24, '==2')],
    [(7, '< 0.2'), (24, '==3')],
    [(7, '< 0.2'), (24, '==4')],
    [(7, '< 0.2'), (24, '==9')]
]
bb = [(0, ('>0')), (0, ('==9')), (0, ('==10')), (0, ('==11')), (0, ('==12')), (0, ('==13')), (0, ('==14')), (0, ('==15')), (0, ('==16'))]
products = []
for a_list in aa:
    for b_condition in bb:
        c = a_list.copy()
        c.append(b_condition)
        products.append(c)

print(len(products))
#write(products, '___.csv', 'conditionals_products.csv')
"""
Attributes                                         #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------  -----------------------  ------------------  -------------------
TrdPrice< 0.1,   Days2Exp.==9                                        774            0.954545              111.545
TrdPrice< 0.1,   Days2Exp.==2                                       3173            0.267173               58.673
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3                     3235            0.312373               55.149
TrdPrice< 0.1,   Days2Exp.==3                                       2370            0.377907               53.762
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9                     1364            0.542986               40.545
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4                     3003            0.494774               39.167
TrdPrice< 0.1,   Days2Exp.==4                                       2423            0.495679               29.85
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==8                     1132            0.432911               29.296
TrdPrice< 0.1,   Days2Exp.==7                                       1007            0.580848               22.059
TrdPrice< 0.1,   Days2Exp.==8                                        622            0.67655                13.921
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2                     3428            0.34326                11.013
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==7                     1255            0.392897                4.417
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5                     1633            0.204277              -14.275
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==6                     1762            0.362722              -14.483
TrdPrice< 0.1,   Days2Exp.==6                                       1569            0.388496              -18.306
TrdPrice< 0.1,   Days2Exp.==5                                       1447            0.276014              -19.73
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==1                     2552            0.188082              -37.736
TrdPrice< 0.1,   Days2Exp.==1                                       2530            0.144279              -38.653
above table for: basic_groupings.csv


TrdPrice< 0.1,   Days2Exp.==3                                       6350            0.495878              224.78
TrdPrice< 0.1,   Days2Exp.==2                                       8280            0.315748              220.976
TrdPrice< 0.1,   Days2Exp.==4                                       6344            0.55414               218.323
TrdPrice< 0.1,   Days2Exp.==9                                       1624            0.832957              204.913
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==3                     7770            0.468809              201.09
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==8                     2731            0.613113              191.738
TrdPrice< 0.1,   Days2Exp.==1                                       8788            0.240192              179.979
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==7                     2597            0.469723              175.321
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==4                     6774            0.492728              174.612
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==2                     8306            0.411145              171.382
TrdPrice< 0.1,   Days2Exp.==5                                       4282            0.453496              159.36
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==1                     8724            0.297828              159.302
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==9                     2134            0.481944              154.958
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==5                     5058            0.485463              152.068
TrdPrice< 0.1,   Days2Exp.==8                                       1923            0.565961              149.232
TrdPrice< 0.1,   Days2Exp.==7                                       2065            0.629834              148.618
TrdPrice>= 0.1,   TrdPrice< 0.2,   Days2Exp.==6                     3862            0.462879              142.221
TrdPrice< 0.1,   Days2Exp.==6                                       3272            0.467265              125.909
above table for: basic_groupings.csv
"""

def read(filename):
    rows = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == [] or float(row[1]) == 0:
                continue
            if filename == 'attribute_combos.csv' and (float(row[1]) < 20 or float(row[2]) < 1.5):
                continue
            rows.append(row)
    sorted_rows = sorted(rows, key=lambda r: float(r[2]), reverse = True)
    #sorted_rows = sorted(rows, key=lambda r: r[0])
    headers = ['Attributes', '#of satisfying trades', 'top1/3 G/L ratio', 'notional return %']
    print(tabulate(sorted_rows, headers))
    print("above table for:", filename)
    print()
#read('attribute_combos.csv')
#read('attribute_basics.csv')
#read('risky.csv')
#read('risky_with_low_price.csv')
#read('trade_prices1.csv')
#read('trade_prices2.csv')
#read('short_term1.csv')
#read('short_term2.csv')
#read('cheap_all.csv')
#read('cheap_recent.csv')
#read('prettycheap_recent.csv')
#read('tradeprices_recent.csv')
#read('prettycheap_recent.csv')
read('conditionals_products.csv')

print("time elapsed:", time.time() - start)


#good performers: QQQ, WFC, VXX, SPY, AAPL
"""
Attributes                                                                                                                                                                                               #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
Symbol == 'BA',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                         10           1.5                    994.24
Symbol == 'WFC',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        50           1                      429.673
Symbol == 'VXX',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        47           0.958333               426.562
Symbol == 'SPY',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       560           1.20472                398.663
Symbol == 'AAPL',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                      162           0.951807               248.359
Symbol == 'QQQ',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        62          14.5                    180.655
Symbol == 'BAC',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       346           0.73                   175.6
Symbol == 'MSFT',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       73           0.780488               118.211
Symbol != '@@@@',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                     5399           0.687187               110.592
Symbol == 'GE',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        559           0.579096                56.095
Symbol not in ['SPY', 'QQQ', 'AAPL', 'IWM', 'BAC', 'AAL', 'AMD', 'GE', 'MSFT', 'HTZ', 'SLV', 'XLF', 'F', 'NIO', 'WFC', 'FB', 'BA', 'GLD', 'VXX'],   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                     2092           0.681672                48.047
Symbol == 'F',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                         341           0.515556                45.687
Symbol == 'FB',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                          9           0.285714                39.249
Symbol == 'IWM',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        19           0.357143                36.773
Symbol == 'AAL',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       205           0.614173                19.15
Symbol == 'HTZ',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       161           0.61                    15.529
Symbol == 'NIO',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       283           0.654971                -1.376
Symbol == 'GLD',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        10           0.428571                -9.142
Symbol == 'AMD',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       144           0.333333               -18.404
Symbol == 'SLV',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                       193           0.0903955              -39.101
Symbol == 'XLF',   Symbol != '@@@@',   TrdPrice< 0.2,   Days2Exp.<=4                                                                                                                                                        73           1.35484                -42.52
above table for: with_symbols_shit.csv


Attributes                                            #of satisfying trades    top1/3 G/L ratio    notional return %
--------------------------------------------------  -----------------------  ------------------  -------------------
TrdPrice< 0.1,   Days2Exp.<=4                                          1997            0.787825               92.397
TrdPrice< 0.1,   Notional<1100                                         7368            0.606629               46.528
TrdPrice< 0.1,   Notional>=1100,   Notional<5500                       1000            0.538462               44.108
TrdPrice< 0.1                                                          8456            0.59728                43.038
TrdPrice< 0.1,   Notional>=12000,   Notional<75000                       35            0.458333               41.272
TrdPrice< 0.1,   % OTM>=90                                              655            0.555819               40.881
TrdPrice< 0.1,   % OTM>24,   % OTM<=45                                 2113            0.551395               36.14
TrdPrice< 0.1,   >Days2Exp.4,   Days2Exp.<=9                           3296            0.638986               35.291
TrdPrice< 0.1,   Notional>=75000                                          4            0.333333               28.539
TrdPrice< 0.1,   Notional>=5500,   Notional<12000                        49            0.580645               24.945
TrdPrice< 0.1,   % OTM>45,   % OTM<90                                  1076            0.591716                8.014
above table for: cheap_recent.csv

Attributes                                            #of satisfying trades    top1/3 G/L ratio    notional return %
--------------------------------------------------  -----------------------  ------------------  -------------------
TrdPrice< 0.2,   Days2Exp.<=4                                          5399            0.687187              110.592
TrdPrice< 0.2,   Notional>=12000,   Notional<75000                      178            0.79798                60.418
TrdPrice< 0.2,   Notional>=5500,   Notional<12000                       416            0.52381                55.02
TrdPrice< 0.2                                                         23967            0.528118               32.865
TrdPrice< 0.2,   Notional>=1100,   Notional<5500                       8248            0.527125               30.846
TrdPrice< 0.2,   Notional<1100                                        15103            0.526172               29.896
TrdPrice< 0.2,   % OTM>=90                                             1462            0.63352                20.674
TrdPrice< 0.2,   >Days2Exp.4,   Days2Exp.<=9                           9029            0.480649               18.329
TrdPrice< 0.2,   % OTM>45,   % OTM<90                                  2840            0.442357               11.206
TrdPrice< 0.2,   % OTM>24,   % OTM<=45                                 4846            0.461399                9.447
TrdPrice< 0.2,   Notional>=75000                                         22            0.466667                2.85
above table for: prettycheap_recent.csv
"""


#ran on all filenames up through 6/05
"""
Attributes                                                                                                                                                                                     #of satisfying trades    top2/3 G/L ratio    notional return %
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
Symbol == 'TSLA',   Symbol != '@@@@'                                                                                                                                                                            1527            0.190179           -26.66
Type == 'PUT',   Type == 'PUT'                                                                                                                                                                                112714            0.237949           -24.8601
Symbol == 'GLD',   Symbol != '@@@@'                                                                                                                                                                             2724            0.274684           -13.9107
Symbol == 'MSFT',   Symbol != '@@@@'                                                                                                                                                                            3415            0.349269           -12.2507
Symbol == 'AMD',   Symbol != '@@@@'                                                                                                                                                                             4809            0.391493           -14.1418
Symbol == 'QQQ',   Symbol != '@@@@'                                                                                                                                                                            14627            0.445784            -9.06922
Notional>200000,   Notional<=400000                                                                                                                                                                             3115            0.494005            -5.26322
Notional>400000,   Notional<=800000                                                                                                                                                                             1356            0.504994            -1.25876
Notional>800000,   Notional>800000                                                                                                                                                                              1221            0.531995             0.523153
Symbol == 'SPY',   Symbol != '@@@@'                                                                                                                                                                            66315            0.532161             0.182009
Symbol == 'GDX',   Symbol != '@@@@'                                                                                                                                                                             2760            0.557562            -5.05976
Notional>70000,   Notional<=200000                                                                                                                                                                             17231            0.561345             0.232914
Symbol == 'AAPL',   Symbol != '@@@@'                                                                                                                                                                            7021            0.575982            -5.28003
Notional>25000,   Notional<=70000                                                                                                                                                                              50693            0.577403             4.57205
% OTM<=-33,   % OTM<=-33                                                                                                                                                                                         865            0.578467            -7.56037
Days2Exp.>54,   Days2Exp.<=59                                                                                                                                                                                    961            0.617845            -8.96599
Symbol == 'FB',   Symbol != '@@@@'                                                                                                                                                                              3855            0.636248            30.6248
% OTM>-2,   <% OTM2                                                                                                                                                                                            69802            0.696735             2.48714
>Days2Exp.4,   Days2Exp.<=9                                                                                                                                                                                    68438            0.708174            -2.93744
Days2Exp.>149,   Days2Exp.<=154                                                                                                                                                                                  600            0.744186            -7.88464
Symbol == 'VXX',   Symbol != '@@@@'                                                                                                                                                                             2085            0.753574            -3.35138
Days2Exp.>49,   Days2Exp.<=54                                                                                                                                                                                    764            0.764434           -16.352
Notional>10000,   Notional<=25000                                                                                                                                                                              66013            0.769406            24.018
Days2Exp.<=4,   Days2Exp.<=4                                                                                                                                                                                   55057            0.775002            14.3779
Symbol == 'IWM',   Symbol != '@@@@'                                                                                                                                                                            12426            0.810842             4.24067
>Days2Exp.9,   Days2Exp.<=14                                                                                                                                                                                   22168            0.815858             1.97469
Days2Exp.>29,   Days2Exp.<=34                                                                                                                                                                                  12804            0.837543             5.45766
Days2Exp.>39,   Days2Exp.<=44                                                                                                                                                                                   8676            0.84478              0.76541
Days2Exp.>19,   Days2Exp.<=24                                                                                                                                                                                  27452            0.846506             8.95965
% OTM>-10,   % OTM<=-2                                                                                                                                                                                         15333            0.859222            -1.87244
% OTM>=2,   % OTM<=10                                                                                                                                                                                         117693            0.871172            10.6987
Symbol != '@@@@',   Symbol != '@@@@'                                                                                                                                                                          300017            0.899816             6.51736
Symbol == 'AAL',   Symbol != '@@@@'                                                                                                                                                                             3712            0.900666            27.5609
Days2Exp.>24,   Days2Exp.<=29                                                                                                                                                                                  23937            0.913429             8.92106
% OTM>10,   % OTM<=20                                                                                                                                                                                          47518            0.919764            15.8537
% OTM>-33,   % OTM<=-10                                                                                                                                                                                         4429            0.930689            -4.57646
Notional>5000,   Notional<=10000                                                                                                                                                                               50881            0.950809            43.5691
Days2Exp.>44,   Days2Exp.<=49                                                                                                                                                                                   5503            1.03513              1.55112
Days2Exp.>14,   Days2Exp.<=19                                                                                                                                                                                  28482            1.05084             16.415
Days2Exp.>74,   Days2Exp.<=79                                                                                                                                                                                   1113            1.05351             12.5338
Days2Exp.>34,   Days2Exp.<=39                                                                                                                                                                                  10293            1.06025              4.61227
Days2Exp.>64,   Days2Exp.<=69                                                                                                                                                                                   1852            1.09029             -1.14891
Notional>2500,   Notional<=5000                                                                                                                                                                                45459            1.12574             63.7821
Symbol not in ['SPY', 'QQQ', 'IWM', 'AAPL', 'BAC', 'GE', 'SLV', 'AAL', 'AMD', 'XLF', 'MSFT', 'FB', 'F', 'WFC', 'BA', 'NIO', 'GLD', 'TSLA', 'HTZ', 'GDX', 'SNAP', 'VXX'],   Symbol != '@@@@'                   131941            1.17955             14.6347
Days2Exp.>84,   Days2Exp.<=89                                                                                                                                                                                   2868            1.19266              4.72115
Symbol == 'SLV',   Symbol != '@@@@'                                                                                                                                                                             8851            1.19464             20.6018
% OTM>20,   % OTM<=33                                                                                                                                                                                          22018            1.20224             23.0119
Days2Exp.>69,   Days2Exp.<=74                                                                                                                                                                                   1564            1.25036              2.38991
Days2Exp.>59,   Days2Exp.<=64                                                                                                                                                                                   1846            1.28465              9.86634
Symbol == 'SNAP',   Symbol != '@@@@'                                                                                                                                                                            2793            1.31784             37.4298
Days2Exp.>89,   Days2Exp.<=94                                                                                                                                                                                   2187            1.34405              8.42966
Notional>1000,   Notional<=2500                                                                                                                                                                                38642            1.38119            104.99
Days2Exp.>124,   Days2Exp.<=134                                                                                                                                                                                  538            1.41256            -13.6835
% OTM>33,   % OTM<=50                                                                                                                                                                                          10629            1.5098              37.8637
Symbol == 'XLF',   Symbol != '@@@@'                                                                                                                                                                             4139            1.52378             23.7444
Symbol == 'F',   Symbol != '@@@@'                                                                                                                                                                               3882            1.52899             45.7382
Notional<=1000,   Notional<=1000                                                                                                                                                                               25406            1.5508             161.972
Days2Exp.>144,   Days2Exp.<=149                                                                                                                                                                                  453            1.57386              9.82248
Symbol == 'HTZ',   Symbol != '@@@@'                                                                                                                                                                             1291            1.58717             10.4322
Days2Exp.>94,   Days2Exp.<=99                                                                                                                                                                                   1213            1.59743             10.3622
Days2Exp.>164,   Days2Exp.<=169                                                                                                                                                                                 3154            1.63933              6.87737
Days2Exp.>79,   Days2Exp.<=84                                                                                                                                                                                   2722            1.70308             12.2879
Days2Exp.>104,   Days2Exp.<=109                                                                                                                                                                                  952            1.76744              7.96719
% OTM>50,   % OTM<=66                                                                                                                                                                                           4449            1.7946              58.9584
Type == 'CALL',   Type == 'CALL'                                                                                                                                                                              187303            1.801               45.5584
Days2Exp.>179,   Days2Exp.<=274                                                                                                                                                                                  344            1.81967             -2.5039
% OTM>66,   % OTM<=100                                                                                                                                                                                          4179            1.85646             35.0015
Symbol == 'GE',   Symbol != '@@@@'                                                                                                                                                                              7408            1.87355             23.7875
Symbol == 'BA',   Symbol != '@@@@'                                                                                                                                                                              1492            1.91977            106.561
Days2Exp.>139,   Days2Exp.<=144                                                                                                                                                                                  307            2.10101              6.08712
Days2Exp.>154,   Days2Exp.<=159                                                                                                                                                                                  915            2.12287             11.891
Days2Exp.>174,   Days2Exp.<=179                                                                                                                                                                                 1335            2.14858             20.419
Days2Exp.>169,   Days2Exp.<=174                                                                                                                                                                                 3146            2.18099             13.2278
Days2Exp.>134,   Days2Exp.<=139                                                                                                                                                                                  314            2.20408             26.2538
Symbol == 'BAC',   Symbol != '@@@@'                                                                                                                                                                             7266            2.20936             39.8071
Symbol == 'NIO',   Symbol != '@@@@'                                                                                                                                                                             2503            2.25065            112.426
Symbol == 'WFC',   Symbol != '@@@@'                                                                                                                                                                             3175            2.32461             57.7601
Days2Exp.>99,   Days2Exp.<=104                                                                                                                                                                                  1059            2.33019              4.8403
Days2Exp.>274,   Days2Exp.<=409                                                                                                                                                                                  258            2.44                16.2568
Days2Exp.>109,   Days2Exp.<=114                                                                                                                                                                                  720            2.5122              33.1115
Days2Exp.>114,   Days2Exp.<=124                                                                                                                                                                                  265            2.68056              5.70618
Days2Exp.>159,   Days2Exp.<=164                                                                                                                                                                                 2433            2.81348              7.80158
Days2Exp.>429,   Days2Exp.>429                                                                                                                                                                                   694            2.94318             37.8458
% OTM>100,   % OTM<=150                                                                                                                                                                                         1827            3.06904             60.1676
Days2Exp.>419,   Days2Exp.<=424                                                                                                                                                                                  898            3.08182             22.0941
% OTM>150,   % OTM>150                                                                                                                                                                                          1275            3.19408             78.6788
Days2Exp.>424,   Days2Exp.<=429                                                                                                                                                                                  986            4.1623              18.0651
Days2Exp.>414,   Days2Exp.<=419                                                                                                                                                                                  670            5.26168             18.2035
Days2Exp.>409,   Days2Exp.<=414                                                                                                                                                                                   76            6.6                 32.7892
"""
