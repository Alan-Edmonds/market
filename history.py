import csv
import time
from tqdm import tqdm
start = time.time()
def printer(option):
    with open('buys_with_scores.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            r = (row[1], row[2], row[3], row[4])
            if r == option:
                print()
                print(r)
                print(row[26])
                print(row[35])
                print()
                print()
                break
#printer(('VXX', '5/15/2020', 'PUT', '250'))
for option in [( 'QQQ',      '6/19/2020',  'CALL',         '254'), ( 'QQQ',      '6/19/2020',  'CALL',         '250')]:
    """
    ( 'AAPL',      '6/26/2020',  'CALL',         '390'),
    ( 'AAPL',      '6/26/2020',  'CALL',         '400'),
    ( 'QQQ',      '6/26/2020',  'CALL',         '256'),
    ( 'VXX',      '6/26/2020',  'PUT',         '30'),
    ( 'VXX',      '6/26/2020',  'PUT',         '31'),
    """



    printer(option)

for i in range(4):
    print()
print("time elapsed:", time.time() - start)



"""
Attributes                                                                                                                            #of satisfying trades    top1/3 G/L ratio    notional return %
----------------------------------------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
Symbol == 'WFC',   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                                                          11             1e+10               1707.26
Symbol == 'VXX',   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                                                           8             3                   1206.07
Symbol == 'AAPL',   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                                                         42             6                   1076.91
Symbol == 'SPY',   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                                                          40             3.44444              425.691
Symbol == 'QQQ',   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                                                           7             6                    232.409
Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL'],   float(Date[0]) == 6,   float(Date[2:]) == 8,   TrdPrice< 0.2,   Days2Exp.==4                      988             1.12931              128.068
above table for: prettycheap_recent.csv
"""
"""
Attributes                                                                                                                             #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
Symbol == 'QQQ',   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                                                          39            1e+10                 202.976
Symbol == 'SPY',   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                                                         152            1.53333                11.935
Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL'],   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                     1374            0.466382              -17.613
Symbol == 'AAPL',   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                                                         22            0.375                 -23.522
Symbol == 'WFC',   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                                                          16            0.230769              -33.829
Symbol == 'VXX',   float(Date[0]) == 6,   float(Date[2:]) == 15,   TrdPrice< 0.2,   Days2Exp.==4                                                          10            0                     -54.581
above table for: prettycheap_recent.csv
"""
"""
Attributes                                                                                                                             #of satisfying trades    top1/3 G/L ratio    notional return %
-----------------------------------------------------------------------------------------------------------------------------------  -----------------------  ------------------  -------------------
Symbol == 'VXX',   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                                                           7            1e+10                  45.84
Symbol == 'QQQ',   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                                                           1            1e+10                  38.889
Symbol == 'AAPL',   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                                                         11            4.5                    30.597
Symbol not in ['QQQ', 'WFC', 'VXX', 'SPY', 'AAPL'],   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                      678            0.458065               18.544
Symbol == 'WFC',   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                                                          13            0.3                     5.667
Symbol == 'SPY',   float(Date[0]) == 6,   float(Date[2:]) == 22,   TrdPrice< 0.2,   Days2Exp.==4                                                          64            0                     -40.632
above table for: prettycheap_recent.csv
"""
