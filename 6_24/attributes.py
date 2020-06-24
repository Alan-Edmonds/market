import csv
import time
from tqdm import tqdm
from tabulate import tabulate
from original_combiner import grouped_attributes
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
    'OptionTradeScreenerResults_20200617', 'OptionTradeScreenerResults_20200618', 'OptionTradeScreenerResults_20200619',
    'OptionTradeScreenerResults_20200622', 'OptionTradeScreenerResults_20200623']
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
symbol_stuff = read_symbols()
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
list_of_lists = [symbol_stuff, days_to_exp_list, notionals_list, otm_list, types]
length_multiplicative = 1
length_sum = 0
for i in range(len(list_of_lists)):
    length_multiplicative *= len(list_of_lists[i])
    length_sum += len(list_of_lists[i])
print("total number of combinations: ", length_multiplicative, "    total number of grouped_attributes() calls: ", length_sum)
everything_list = []
for L in list_of_lists:
    for x in L:
        everything_list.append(x)

combinations = []
for i in symbol_stuff:
    for j in days_to_exp_list:
        for k in notionals_list:
            combinations.append([(3, " == 'PUT'"), i[0], i[1], j[0], j[1], k[0], k[1]]) #adjustable: right now looking at what seems to work in terms of puts

def write(conditionals, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for x in tqdm(conditionals):
            writer.writerow(grouped_attributes(x))
write(combinations, 'attribute_combos.csv')
write(everything_list, 'attribute_basics.csv')


def read(filename):
    print(filename)
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
    headers = ['Attributes', '#of satisfying trades', 'top2/3 G/L ratio', 'notional return %']
    print(tabulate(sorted_rows, headers))
read('attribute_combos.csv')
read('attribute_basics.csv')

print("time elapsed:", time.time() - start)

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
