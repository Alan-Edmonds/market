import math
import numpy
listt = [2, 5, 3, 4]
print(listt.sort())

print(math.ceil(9/2))

x = 0
print(eval('x>10'))

if eval(str('AAL' in ['A', 'AAL'])):
    print('yes')
else:
    print('no')

if not eval("'AAL'" + " not in ['SPY', 'QQQ', 'IWM']"):
    print('aal')
else:
    print(69)

print('' == None)

count = 0
for i in ['Time', 'Symbol', 'Option Expiration', 'Type', 'Strike', 'Spot Price', 'Open Interest', 'Trade Price', 'Bid Size', 'Bid',
    'Ask', 'Ask Size', 'Notional', 'Trade IV', 'Condition', 'Execution', 'Delta', 'Bid Ask Spread', 'Days To Exp', 'Trade Quantity vs OI',
    'Day of Trade', 'Spread/Mid ratio', 'Bid/Ask Percentile', '% OTM', 'Score: all', 'Score: top 2/3', 'Score: top 1/2', 'Score: top 1/3']:
    count += 1
print(count)

x = '-9.2344'
print(float(x))

s = 'alan'
print(s[:-2])

print(float('09') + 1)

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
    'OptionTradeScreenerResults_20200622', 'OptionTradeScreenerResults_20200623', 'OptionTradeScreenerResults_20200624',
    'OptionTradeScreenerResults_20200625', 'OptionTradeScreenerResults_20200626']
days = []
for f in filenames:
    days.append(f[-4:])
print(days)


cutoff_list = [-10000, 1,2,3,4,5,6,7,800,9, 10]
print(numpy.quantile(cutoff_list, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
cutoff_list.sort()
print(cutoff_list)

list = [1,2,3,4]
outliers_index = round(len(list)/10)
print(list[outliers_index : -1*outliers_index])

dict = {'5/15/2020': ['10', '9', '7', '8', '8.5'], '6/19/2020': ['7.5'], '5/22/2020': ['8'], '5/8/2020': ['8.5', '8'], '1/15/2021': ['7.5']}
print(sorted(dict.items()))

sortt =  [('10/16/2020', ['9']), ('05/29/2020', ['8.5']), ('06/19/2020', ['10', '9']), ('07/17/2020', ['8', '9'])]
print(sorted(sortt))
