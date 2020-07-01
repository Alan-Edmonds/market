#TODO:
#Make it so that group attributes lets me input a certain range of days for which the scores should be calculated
#As in for range[7-11 days]:
#   maybe an option expirying 10/16/2020 was bought on 5/08/2020. Only calculate the 'Score:all' or 'Score:top2/3'
#   using a historical price list of the option's average mid value from 5/15 to 5/19
import csv
import math
import statistics as stats
import numpy
import time
from tabulate import tabulate
from tqdm import tqdm
from operator import itemgetter
start = time.time()
print("start #####################################################################################################################")
#when new option trade files are added, rerun: all_combiner(), buys_all_combiner(), scorer(). Will also have to update the trade_day conditionals in all_combiner()
filenames = ['OptionTradeScreenerResults_20200601', 'OptionTradeScreenerResults_20200602', 'OptionTradeScreenerResults_20200603',
'OptionTradeScreenerResults_20200604', 'OptionTradeScreenerResults_20200605', 'OptionTradeScreenerResults_20200608',
    'OptionTradeScreenerResults_20200609', 'OptionTradeScreenerResults_20200610', 'OptionTradeScreenerResults_20200611',
    'OptionTradeScreenerResults_20200612', 'OptionTradeScreenerResults_20200615', 'OptionTradeScreenerResults_20200616',
    'OptionTradeScreenerResults_20200617', 'OptionTradeScreenerResults_20200618', 'OptionTradeScreenerResults_20200619',
    'OptionTradeScreenerResults_20200622', 'OptionTradeScreenerResults_20200623', 'OptionTradeScreenerResults_20200624',
    'OptionTradeScreenerResults_20200625', 'OptionTradeScreenerResults_20200626']
def print4():
    for i in range(4):
        print()
def print2():
    print()
    print()
#this function all_combines trades from all filenames into one csv file. will need to rerun this when filenames is updated.
    #Also appends trade_day parameter to each trade
def all_combiner(input): #this writes the all_combiner_recent.csv, which is all of the block trades near ask from all the input files
    data = []
    trade_day = 601
    #relative_trade_day = 0  #don't really need this, because of the Days To Exp param
    print("Reading csv downloads...")
    for filename in tqdm(input):
        with open(filename + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == [] or row[14] == 'Trade Price':
                    continue
                important = [0, 1, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 28, 29, 30, 32, 33, 34, 35, 37, 38, 39, 40, 43, 47]
                trimmed_row = []
                for i in important:
                    if i in [32, 33]:
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
    with open('all_combiner_recent.csv', 'w') as f:
        writer = csv.writer(f)
        print("writing data into all_combiner_recent.csv...")
        for row in tqdm(data):
            writer.writerow(row)
#all_combiner(filenames)

#this reads in all_combiner_recent.csv and writes the buy trades into buys_recent.csv. Also calculates and appends a few more variables for each trade:
    #appends (1): bid-ask spread divided by mid, (2): bid/ask percentile of the buy (mid would be 50, ask would be 100),
    #(3): % OTM, (4): IV20day divided by IV1year
def filter_buys():
    rows = []
    print("Reading all_combiner_recent.csv. Running filter_buys()...")
    with open('all_combiner_recent.csv') as f:
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
            if type == 'CALL': #unlimited otm% for a call
                row.append(round(100*(strike - spot)/spot, 2))
            elif type == 'PUT': #reminder that maximum otm% for a put is <100
                row.append(round(100*(spot - strike)/spot, 2))
            if row[20] != '' and row[22] != '':
                IV20day = float(row[20])
                IV1year = float(row[22])
                row.append(round(IV20day/IV1year, 2))
            else:
                row.append('')
            rows.append(row)
    with open('buys_recent.csv', 'w') as f:
        writer = csv.writer(f)
        print("writing data into buys_recent.csv...")
        for row in tqdm(rows):
            writer.writerow(row)
#filter_buys()

def price_history(): #return value lets us see how the price of a specific option changed
    dict = {} #maps each specific option to their dictionary, where keys are days_to_exp and values
        #are a list of mids from that specific days_to_exp value (for trades of said option)
    print("Reading all_combiner_recent.csv. Running price_history()...")
    with open('all_combiner_recent.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            symbol, expiry, type, strike = row[1], row[2], row[3], row[4]
            trade_day = row[26]
            mid = round((float(row[9]) + float(row[10]))/2, 3)
            if (symbol, expiry, type, strike) in dict:
                if trade_day in dict.get((symbol, expiry, type, strike)):
                    dict.get((symbol, expiry, type, strike)).get(trade_day).append(mid)
                else:
                    dict.get((symbol, expiry, type, strike))[trade_day] = [mid]
            else:
                dict[(symbol, expiry, type, strike)] = {trade_day: [mid]}
    options_and_tuples = {} #modified version of dict above. Maps each specific option to a list of tuples,
        #where tuple[0] is trade_day, and tuple[1] is the average mid for trades with that value tuple[0] on that trade_day (of said option).
    print("Running price_history(). Building simplified dictionary...")
    for option in tqdm(dict):
        d = dict.get(option)
        if len(d) < 4: #only options traded on 4+ different days
            continue
        tuples = []
        for trade_day in d:
            mids_list = d.get(trade_day)
            sum = 0
            for mid in mids_list:
                sum += mid
            tuples.append((trade_day, round(sum/len(mids_list), 3))) #tuple of (days_to_exp, average mid) *avg mid for trades with that value of days_to_exp
        options_and_tuples[option] = tuples
    #print stuff
    """
    i = 0
    printed_count = 0
    for opt in options_and_tuples:
        i += 1
        if i % 1000 == 0 and printed_count < 50:
            print(opt, "     ", options_and_tuples.get(opt))
            printed_count += 1
    print('num of specific options traded on 4+ different days:', len(options_and_tuples))
    print()
    """
    return options_and_tuples

#this function reads in buys_recent.csv and for each buy trade, calculates a score for that trade based on how the price of
    #the option changed over time. Right now only calculates for options that were traded 3+ times after the day they were bought.
def scorer():
    options_and_tuples = price_history()
    with_scores = []
    with open('buys_recent.csv') as f:
        reader = csv.reader(f)
        print('reading buys_recent.csv. Running scorer()...')
        count = 0
        for row in tqdm(reader):
            count += 1
            if row == [] or float(row[5]) == 0:
                continue
            option = (row[1], row[2], row[3], row[4])
            if option in options_and_tuples:
                this_trade_day = 100*int(row[26][0]) + int(row[26][2:])
                mids_list = []
                for tuple in options_and_tuples.get(option):
                    if 100*int(tuple[0][0]) + int(tuple[0][2:]) > this_trade_day:
                        mids_list.append(tuple[1])
                if len(mids_list) == 0: #option must have been traded on >0 different days AFTER the buy occured
                    continue
                mids_list.sort(reverse = True) #high to low
                cutoff1 = len(mids_list)
                cutoff2 = math.ceil(len(mids_list)*2/3)
                cutoff3 = math.ceil(len(mids_list)/2)
                cutoff4 = math.ceil(len(mids_list)/3)
                trade_price = float(row[7])
                for cutoff in [cutoff1, cutoff2, cutoff3, cutoff4]:
                    score = 0
                    for i in range(cutoff):
                        percent_inc = 100*(mids_list[i] - trade_price) / trade_price
                        score += percent_inc
                    row.append(round(score/cutoff, 3))
                row.append(options_and_tuples.get(option))
                with_scores.append(row)
    with open('buys_with_scores_recent.csv', 'w') as f:
        writer = csv.writer(f)
        print("writing scores...")
        for row in tqdm(with_scores):
            writer.writerow(row)
#scorer()

#reusable mini-function for printing some basic stats, given an input list of scores
def stats_printer(scores_dict):
    output = None
    for cutoff in scores_dict:
        if cutoff != 'Scores:top2/3': #adjustable: right now computes gains/losses using Scores:all
            continue
            None
        gains, losses = 0, 0
        cutoff_list = scores_dict.get(cutoff)
        for score in cutoff_list:
            if score > 0:
                gains += 1
            else:
                losses += 1
        if gains == 0:
            return 0
        if losses == 0:
            return 9999999999
        #decile printing stuff
        """
        print2()
        print(cutoff)
        print("deciles: ")
        for i in range(9):
            x = i+1
            print(x, 'th decile: ', round(numpy.quantile(cutoff_list, x/10), 3))
        """
        print("number of satisfying trades:", len(cutoff_list), "    median:", round(stats.median(cutoff_list), 3),
            "    mean:", round(stats.mean(cutoff_list), 3), "    std dev:", round(stats.stdev(cutoff_list), 3))
        print("gains and losses:", gains, losses, "   ratio:", gains/losses)
        output = gains/losses
        #print2()
    return output

#current idea: input is a dictionary mapping param index to respective conditional
def grouped_attributes(input):
    all_headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'B.Size', 'Bid', 'Ask', 'A.Size', 'Notional', 'TradeIV',
        '1-day IV Chg', 'IV % Rank', 'Cond.', 'Exec.', 'Delta', 'Spread', '20DayHistIV', 'TradeIV vs 20DayIV (% diff)', '1YearHistIV',
        'TradeIV vs 1YearIV (% diff)', 'Days2Exp.', 'Qty.vsOI', 'Date', 'Spread/Mid', 'B/A.Percentile', '% OTM', '20DayIV / 1YearIV',
        'Score:all', 'Score:top2/3', 'Score:top1/2', 'Score:top1/3','Hist.Prices']
    attributes = "Specific attributes: "
    for tuple in input:
        if len(tuple[1]) == 2:
            attributes += tuple[1][0] + all_headers[tuple[0]] + tuple[1][1] + ",   "
            continue
        attributes += all_headers[tuple[0]] + tuple[1] + ",   "
    if attributes == "Specific attributes: ":
        attributes = "Specific attributes:   None. All trades from buys_with_scores_recent.csv"
    #print(attributes)

    count = 0
    price_history = []
    table_rows = []
    notional_adjusted_scores_sum = 0
    original_notionals_sum = 0
    distinct_symbols = set()
    exceed_100 = False
    scores_dict = {'Scores:all' : [], 'Scores:top2/3' : [], 'Scores:top1/2': [], 'Scores:top1/3': []}
    with open('buys_with_scores_recent.csv') as f:
        reader = csv.reader(f)
        print("running grouped_attributes()... @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        for row in tqdm(reader):
            if row == []:
                continue
            #conditionals for filtering out trades that don't satisfy our input
            satisfies = True
            for tuple in input:
                if tuple[0] in [1, 3, 16, 17]:
                    if not eval("'" + row[tuple[0]] + "'" + tuple[1]):
                        satisfies = False
                        break
                elif tuple[0] in [2, 26]:
                    if not eval(tuple[1][0] + "'" + row[tuple[0]] + "'" + tuple[1][1]):
                        satisfies = False
                        break
                elif tuple[0] == 0:
                    it = row[tuple[0]][:2]
                    if it == '09':
                        it = '9'
                    if not eval("float(" + it + ")" + tuple[1]):
                        satisfies = False
                        break
                else:
                    if not eval(row[tuple[0]] + tuple[1]):
                        satisfies = False
                        break
            if not satisfies:
                continue

            scores_dict['Scores:all'].append(float(row[31]))
            scores_dict['Scores:top2/3'].append(float(row[32]))
            scores_dict['Scores:top1/2'].append(float(row[33]))
            scores_dict['Scores:top1/3'].append(float(row[34]))
            count += 1
            #adjustable: right now notional scores are calculated using Scores:top2/3
            notional_adjusted_scores_sum += float(row[12])*(1 + float(row[32])/100)
            original_notionals_sum += float(row[12])

            if len(table_rows) > 100 and exceed_100 == False:
                table_rows.append([])
                exceed_100 = True
            if row[1] not in distinct_symbols and exceed_100 == True and len(table_rows) < 150:
                table_rows.append(row[:8] + row[9:11] + [row[12]] + row[16:18] + row[24:27] + row[31:35])
                distinct_symbols.add(row[1])
            elif exceed_100 == False:
                table_rows.append(row[:8] + row[9:11] + [row[12]] + row[16:18] + row[24:27] + row[31:35])
                price_history.append(row[:8] + row[9:11] + [row[12]] + row[16:18] + row[24:27] + row[31:])
                distinct_symbols.add(row[1])

    #table printing
    table_headers = ['Time', 'Symbol', 'Expiry', 'Type', 'Strike', 'Spot', 'OI', 'TrdPrice', 'Bid', 'Ask', 'Notional', 'Cond.',
        'Exec.', 'Days2Exp.', 'Qty.vsOI', 'Date', 'Score:all', 'Score:top2/3', 'Score:top1/2', 'Score:top1/3']
    print('Satisfying trades:')
    print(tabulate(table_rows, table_headers)) #adjustable: choose whether to see the table of trades or not
    print("------  --------  ---------  ------  --------  -------  -----  ----------  -----  -----  ----------  -------  -------  -----------  ----------  ------  -----------  --------------  --------------  --------------")
    print("Time    Symbol    Expiry     Type      Strike     Spot     OI    TrdPrice    Bid    Ask    Notional  Cond.    Exec.      Days2Exp.    Qty.vsOI  Date      Score:all    Score:top2/3    Score:top1/2    Score:top1/3")
    print("table rows exceeded 100:", exceed_100)
    print2()

    print(attributes, "  #of trades:", count)
    print()
    gain_loss_ratio = stats_printer(scores_dict)
    print2()
    """
    #price history printing
    for row in price_history:
        print()
        print(row[1], row[2], row[3], row[4])
        print(row[15] + ":", eval(row[21])[-7:])
        print2()
    """
    print(attributes, "  #of trades:", count)
    return_percent = None
    if count != 0:
        return_percent = round(100*(notional_adjusted_scores_sum - original_notionals_sum)/original_notionals_sum, 3)
    print("Return percentage (for buying these trades with the same notional, and realizing a top2/3 score)", return_percent)

    print4()
    return attributes[20:-4], count, gain_loss_ratio, return_percent
#grouped_attributes([]) #sanity check. scores for all buys in buys_with_scores, with no other restrictions
#grouped_attributes([(1, " == 'VXX'"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8"))])

#function only to show/hide results of previous attribute all_combinations
def attr():
    """
    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (12, '<5000')])              #top2/3 G/L ratio: 3.75    notional return: 111.5%    #of trades:   973
    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (29, '>50')])                #top2/3 G/L ratio: 4.70    notional return: 152.0%    #of trades:   359
    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (12, '<5000'), (29, '>50')]) #top2/3 G/L ratio: 6.11    notional return: 193.3%    #of trades:   277

    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (12, '<2500')])              #top2/3 G/L ratio:  6.13    notional return: 165.2%    #of trades:   556
    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (29, '>66')])                #top2/3 G/L ratio:  7.00    notional return: 179.1%    #of trades:   224
    grouped_attributes([(12, "<300"), (26, ("float(", "[0]) == 6")), (26, ("float(", "[2:]) >= 8")), (24, '>79'), (24, '<=84'), (12, '<2500'), (29, '>66')]) #top2/3 G/L ratio: 16.40    notional return: 240.7%    #of trades:   139




    grouped_attributes([(24, '>79'), (24, '<=84')])                             #top2/3 G/L ratio: 2.04    notional return:  23.1%    #of trades:  3745
    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<8500')])              #top2/3 G/L ratio: 3.21    notional return:  89.4%    #of trades:  1461
    grouped_attributes([(24, '>79'), (24, '<=84'), (29, '>33')])                #top2/3 G/L ratio: 3.43    notional return:  90.7%    #of trades:   669
    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<8500'), (29, '>33')]) #top2/3 G/L ratio: 3.83    notional return: 127.4%    #of trades:   575

    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<5000')])              #top2/3 G/L ratio: 3.75    notional return: 111.5%    #of trades:   973
    grouped_attributes([(24, '>79'), (24, '<=84'), (29, '>50')])                #top2/3 G/L ratio: 4.70    notional return: 152.0%    #of trades:   359
    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<5000'), (29, '>50')]) #top2/3 G/L ratio: 6.11    notional return: 193.3%    #of trades:   277

    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<2500')])              #top2/3 G/L ratio:  6.13    notional return: 165.2%    #of trades:   556
    grouped_attributes([(24, '>79'), (24, '<=84'), (29, '>66')])                #top2/3 G/L ratio:  7.00    notional return: 179.1%    #of trades:   224
    grouped_attributes([(24, '>79'), (24, '<=84'), (12, '<2500'), (29, '>66')]) #top2/3 G/L ratio: 16.40    notional return: 240.7%    #of trades:   139



    #important timeframes:

    grouped_attributes([])                              #top2/3 G/L ratio: 0.93    notional return: 10.6%    #of trades:534543
    grouped_attributes([(24, '<=4')])                   #top2/3 G/L ratio: 0.80    notional return: 18.5%    #of trades: 80854
    grouped_attributes([(24, '>4'), (24, '<=9')])       #top2/3 G/L ratio: 0.66    notional return: -1.3%    #of trades:132761
    grouped_attributes([(24, '>9'), (24, '<=14')])      #top2/3 G/L ratio: 1.00    notional return:  8.7%    #of trades: 57678
    grouped_attributes([(24, '>14'), (24, '<=19')])     #top2/3 G/L ratio: 1.01    notional return: 21.4%    #of trades: 38322
    grouped_attributes([(24, '>19'), (24, '<=24')])     #top2/3 G/L ratio: 0.82    notional return:  5.6%    #of trades: 39811
    grouped_attributes([(24, '>24'), (24, '<=29')])     #top2/3 G/L ratio: 0.88    notional return: 13.8%    #of trades: 52649
    grouped_attributes([(24, '>29'), (24, '<=34')])     #top2/3 G/L ratio: 1.35    notional return: 18.5%    #of trades: 24231
    grouped_attributes([(24, '>34'), (24, '<=39')])     #top2/3 G/L ratio: 1.16    notional return:  8.6%    #of trades: 12126
    grouped_attributes([(24, '>39'), (24, '<=44')])     #top2/3 G/L ratio: 0.89    notional return:  4.6%    #of trades:  9565
    grouped_attributes([(24, '>44'), (24, '<=49')])     #top2/3 G/L ratio: 0.89    notional return:  2.4%    #of trades:  6957
    grouped_attributes([(24, '>49'), (24, '<=54')])     #top2/3 G/L ratio: 1.40    notional return: 19.1%    #of trades:  6989
    grouped_attributes([(24, '>54'), (24, '<=59')])     #top2/3 G/L ratio: 2.37    notional return: 17.8%    #of trades:  3315
    grouped_attributes([(24, '>59'), (24, '<=64')])     #top2/3 G/L ratio: 1.55    notional return:  7.0%    #of trades:  2369
    grouped_attributes([(24, '>64'), (24, '<=69')])     #top2/3 G/L ratio: 1.26    notional return:  6.1%    #of trades:  3933
    grouped_attributes([(24, '>69'), (24, '<=74')])     #top2/3 G/L ratio: 1.40    notional return:  9.9%    #of trades:  6261
    grouped_attributes([(24, '>74'), (24, '<=79')])     #top2/3 G/L ratio: 2.22    notional return: 21.8%    #of trades:  3035
    grouped_attributes([(24, '>79'), (24, '<=84')])     #top2/3 G/L ratio: 2.04    notional return: 23.1%    #of trades:  3745
    grouped_attributes([(24, '>84'), (24, '<=89')])     #top2/3 G/L ratio: 1.26    notional return:  7.9%    #of trades:  4081
    grouped_attributes([(24, '>89'), (24, '<=94')])     #top2/3 G/L ratio: 1.16    notional return: 11.9%    #of trades:  4898
    grouped_attributes([(24, '>94'), (24, '<=99')])     #top2/3 G/L ratio: 1.81    notional return:  9.9%    #of trades:  2027
    grouped_attributes([(24, '>99'), (24, '<=104')])    #top2/3 G/L ratio: 2.19    notional return: 10.0%    #of trades:  1473
    grouped_attributes([(24, '>104'), (24, '<=109')])   #top2/3 G/L ratio: 1.78    notional return: 11.6%    #of trades:  1207
    grouped_attributes([(24, '>109'), (24, '<=114')])   #top2/3 G/L ratio: 2.61    notional return: 34.2%    #of trades:   961
    grouped_attributes([(24, '>114'), (24, '<=124')])   #top2/3 G/L ratio: 2.12    notional return: 18.8%    #of trades:  1155
    grouped_attributes([(24, '>124'), (24, '<=134')])   #top2/3 G/L ratio: 1.50    notional return: -5.8%    #of trades:   954
    grouped_attributes([(24, '>134'), (24, '<=139')])   #top2/3 G/L ratio: 1.51    notional return: 20.7%    #of trades:  1133
    grouped_attributes([(24, '>139'), (24, '<=144')])   #top2/3 G/L ratio: 3.09    notional return:  4.5%    #of trades:   887
    grouped_attributes([(24, '>144'), (24, '<=149')])   #top2/3 G/L ratio: 1.54    notional return: 13.4%    #of trades:   895
    grouped_attributes([(24, '>149'), (24, '<=154')])   #top2/3 G/L ratio: 0.66    notional return: -3.5%    #of trades:  4729
    grouped_attributes([(24, '>154'), (24, '<=159')])   #top2/3 G/L ratio: 3.00    notional return: 16.0%    #of trades:  5390
    grouped_attributes([(24, '>159'), (24, '<=164')])   #top2/3 G/L ratio: 2.80    notional return: 19.5%    #of trades:  3453
    grouped_attributes([(24, '>164'), (24, '<=169')])   #top2/3 G/L ratio: 1.71    notional return: 13.6%    #of trades:  3741
    grouped_attributes([(24, '>169'), (24, '<=174')])   #top2/3 G/L ratio: 1.71    notional return: 13.6%    #of trades:  3619
    grouped_attributes([(24, '>174'), (24, '<=179')])   #top2/3 G/L ratio: 2.15    notional return: 25.2%    #of trades:  1455
    grouped_attributes([(24, '>179'), (24, '<=274')])   #top2/3 G/L ratio: 2.23    notional return:  5.4%    #of trades:   985
    grouped_attributes([(24, '>274'),(24, '<=409')])    #top2/3 G/L ratio: 1.21    notional return:  8.8%    #of trades:  1240
    grouped_attributes([(24, '>409'),(24, '<=414')])    #top2/3 G/L ratio: 1.99    notional return: 16.5%    #of trades:  1566
    grouped_attributes([(24, '>414'),(24, '<=419')])    #top2/3 G/L ratio: 4.05    notional return: 20.7%    #of trades:  1056
    grouped_attributes([(24, '>419'),(24, '<=424')])    #top2/3 G/L ratio: 3.05    notional return: 18.9%    #of trades:  1114
    grouped_attributes([(24, '>424'),(24, '<=429')])    #top2/3 G/L ratio: 3.57    notional return: 20.4%    #of trades:  1093
    grouped_attributes([(24, '>429')])                  #top2/3 G/L ratio: 3.31    notional return: 50.2%    #of trades:   828
    """

print("time elapsed:", time.time() - start)
#ideas for groups:
    #parameters in isolation:
    #high otm %
    #short expiry
    #long expiry
    #high notional
    #low open interest
    #floor trades
    #expiration is within 1 week of trade date

#high notional should be all_combiner with all previously isolated params
#calls vs puts should be examined for all previously isolated params
#otm/itm % can be all_combiner with other params too
#this ends up being about maybe 40 combos just listed here. kinda should automate param inputs into a certain flexible function
