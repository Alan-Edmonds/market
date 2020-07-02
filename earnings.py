import csv
import time
import matplotlib.pyplot as plot
import statistics as stats
import numpy
from tqdm import tqdm
from original_combiner import all_combiner
start = time.time()
#   go to https://www.investing.com/earnings-calendar/
#   select desired timeframe and scroll down fully to load all text
#   ctrl+A and copy paste into csv file
special = ['SPY', 'QQQ', 'IWM', 'SLV', 'XLF', 'GLD', 'GDX', 'VXX']
all_tradedays = ['0505', '0507', '0508', '0511', '0512', '0513', '0514', '0515', '0518', '0519', '0520', '0521',
    '0522', '0526', '0527', '0528', '0529', '0601', '0602', '0603', '0604', '0605', '0608', '0609', '0610',
    '0611', '0612', '0615', '0616', '0617', '0618', '0619', '0622', '0623', '0624', '0625', '0626', '0629',
    '0630', '0701']
#all_combiner(all_tradedays) #runtime ~3min

def well_traded(): #a cleaner function that reads in the earnings_calendar.csv file and creates the earnings_well_traded.csv
    dictionary = {} #dictionary mapping file for each date to the set of tickers traded on that date
    print("creating trade_day - tickers dictionary...")
    for d in tqdm(all_tradedays):
        ticker_set = set()
        with open('OptionTradeScreenerResults_2020' + d + '.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                ticker_set.add(row[1])
        dictionary[d] = ticker_set

    print("cleaning data and writing earnings_well_traded.csv...")
    data_to_write = []
    earnings_date = ''
    with open('earnings_calendar.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if len(row) == 3:
                i = row[1].rindex(' ')
                month = row[1][:i]
                if float(row[1][i+1:]) < 10: #converts 507 to 0507
                    day = '0' + row[1][i+1:]
                else:
                    day = row[1][i+1:]
                if month == ' May':
                    earnings_date = '05' + day
                elif month == ' June':
                    earnings_date = '06' + day
                elif month == ' July':
                    earnings_date = '07' + day
                elif month == ' August':
                    earnings_date = '08' + day
                continue
            for i in range(len(row)): #this loop exists because of weird shit have to deal with in the earnings_calendar.csv file
                if earnings_date not in all_tradedays: #this keeps us from writing future earnings dates into earnings_well_traded.csv
                    continue
                if '(' in row[i]:
                    first_parenthesis = row[i].index('(')
                    second_parenthesis = row[i].index(')')
                    ticker = row[i][first_parenthesis + 1 : second_parenthesis]
                    if '_' in ticker:
                        break #removing tickers with annoying _'s cause fuck em
                    #the following lines add the [earnings_date, ticker] row if it was traded in the five trading days leading up to earnings
                    i = all_tradedays.index(earnings_date) #the index (in above list 'dates') of the date for earnings of this row's ticker
                    well = True
                    for d in [all_tradedays[i-5], all_tradedays[i-4], all_tradedays[i-3], all_tradedays[i-2], all_tradedays[i-1]]:
                        if ticker not in dictionary[d]:
                            well = False
                    if well:
                        data_to_write.append([earnings_date, ticker])
                    break
    with open('earnings_well_traded.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data_to_write:
            writer.writerow(row)
#well_traded() #runtime ~30sec

def process_options():
    #   writes earnings_processed_options.csv. row[0] is earnings date, row[1] is specific option, row[2] is a dictionary mapping
    #   trade days to tuples, where tuple[0] is the avg price of the speficic option on that day, and tuple[1] is the avg spot price
    #   of the stock for that day.
    data_to_write = []
    with open('earnings_well_traded.csv') as f1:
        reader1 = csv.reader(f1)
        print("reading in earnings_well_traded.csv...")
        for earnings_row in tqdm(reader1):
            if earnings_row == []:
                continue
            options = {} #dictionary of dictionaries: specific options each mapped to their dictionary which maps trade_day to a list of option's prices on that day
            with open('all_combiner.csv') as f2:
                reader2 = csv.reader(f2)
                print()
                print()
                print("reading in all_combiner.csv and finding satisfying options trades for ", earnings_row, "...")
                for row in tqdm(reader2):
                    if row == []:
                        continue
                    if row[2][-4:] != '2020': #skip if the option expiration isn't in 2020
                        #print("skipped", row[2][-4:])
                        continue
                    if row[1] == earnings_row[1]: #check that the option trade is for the ticker in question
                        specific_opt = (row[1], row[2], row[3], row[4])
                        if specific_opt in options:
                            if row[26] in options[specific_opt]:
                                options[specific_opt][row[26]].append(row[7])
                            else:
                                options[specific_opt][row[26]] = [row[7]] #each dictionary d is a mapping of trade_day to a tuple of two lists; list of the option's prices on that day, and list of corresponding spot prices
                        else:
                            options[specific_opt] = {row[26] : [row[7]]} #each specific_opt option is mapped to a dictionary d
            for specific_opt in options:
                inner_dict = options.get(specific_opt)
                day_before_earnings = all_tradedays[all_tradedays.index(earnings_row[0]) - 1]
                if day_before_earnings not in inner_dict: #skips the specific_opt if I don't have data for it being traded on the day before earnings
                    continue
                if list(inner_dict.keys()).index(day_before_earnings) <= 1: #index of day_before_earnings has to be at least 2. Skips the specific_opt if I don't have data for it being traded on two different trading days before day_before_earnings. In other words, the option has to have date for it being traded on the three trading days before earings.
                    continue
                simplified_inner_dict = {} #each specific_opt has a corresponding simplified_inner_dict. In this dictionary, each trade_day is mapped to the avg option price for that day.
                for trade_day in inner_dict:
                    price_history_strings = inner_dict.get(trade_day)
                    floats = []
                    for price in price_history_strings:
                        floats.append(float(price))
                    simplified_inner_dict[trade_day] = round(stats.mean(floats), 3)
                data_to_write.append((earnings_row[0], specific_opt, simplified_inner_dict))
                print(earnings_row[0], specific_opt, simplified_inner_dict)
    print("writing data into earnings_processed_options.csv...")
    with open('earnings_processed_options.csv', 'w') as f:
        writer = csv.writer(f)
        for row in tqdm(data_to_write):
            writer.writerow(row)
#process_options() #runtime ~80min

def stock_prices():
    tickers_and_dates = {} #maps each ticker from the options earnings_processed_options.csv to the list of trade days for that ticker's options. Starts with base cases of ['SPY', 'QQQ', 'IWM', 'SLV', 'XLF', 'GLD', 'GDX', 'VXX']
    for symbol in special:
        tickers_and_dates[symbol] = set(all_tradedays)
    with open('earnings_processed_options.csv') as f:
        reader = csv.reader(f)
        print("reading in earnings_processed_options.csv and creating tickers_and_dates dictionary...")
        for row in tqdm(reader):
            if row == []:
                continue
            if eval(row[1])[0] in tickers_and_dates:
                for d in eval(row[2]).keys():
                    tickers_and_dates[eval(row[1])[0]].add(d)
            else:
                date_set = set()
                for d in eval(row[2]).keys():
                    date_set.add(d)
                tickers_and_dates[eval(row[1])[0]] = date_set
    with open('earnings_avg_spot_prices.csv', 'w') as f:
        writer = csv.writer(f)
        print("using tickers_and_dates dictionary to read csv files...")
        for ticker in tqdm(tickers_and_dates):
            dict = {} #list of (date, avg spot price) tuples for the ticker
            for date in sorted(list(tickers_and_dates.get(ticker))):
                prices = []
                with open('OptionTradeScreenerResults_2020' + date + '.csv') as f_:
                    reader = csv.reader(f_)
                    for row in reader:
                        if row == []:
                            continue
                        if row[1] == ticker:
                            prices.append(float(row[8]))
                prices.sort()
                outliers_index = round(len(prices)/10)
                if outliers_index == 0:
                    dict[date] = round(stats.mean(prices), 3)
                else: #accounts for outliers in spot price, sometimes an $80 stock has spot price value of like 0.17 randomly
                    dict[date] = round(stats.mean(prices[outliers_index : -1*outliers_index]), 3)
            writer.writerow([ticker, dict])
#stock_prices() #runtime ~60min

def find_strangles_helper():
    #   this helps us find options with potential strangles by writing the earnings_strangles_helper.csv, whose every row
    #   is a tuple of (ticker, trade_day, calls dictionary, puts dictionary). The calls and puts dictionaries map expiry
    #   dates to the list of strike prices for options of that expiry (which are for ticker and were traded on trade_day).
    #   The earnings_strangles_helper.csv along with earnings_avg_spot_prices.csv will make it easier to build the
    #   find_strangles() function. This function finds call options and put options, with the same expiry, and uses the
    #   avg spot price to find a pairing where the call and put are approx the same %otm. This is a valid strangle, and
    #   it's price movement over time is what I'm interested in.
    data_to_write = []
    print("running find_strangles_helper()...")
    with open('earnings_avg_spot_prices.csv') as f:
        reader = csv.reader(f)
        for avg_spot_row in tqdm(reader):
            if avg_spot_row == []:
                continue
            if avg_spot_row[0] in special:
                continue
            print("   ...", avg_spot_row[0])
            for trade_day in eval(avg_spot_row[1]).keys():
                calls = {} #dictionary mapping each expiry to a list of the different strikes traded for call options with that expiry
                puts = {} #same but for expiry_strikes_puts
                with open('earnings_processed_options.csv') as f_:
                    reader_ = csv.reader(f_)
                    for row in reader_:
                        if row == []:
                            continue
                        if eval(row[1])[0] != avg_spot_row[0] or trade_day not in eval(row[2]).keys(): #the specific option represented by row_b is not for the ticker in question from row_a, or it was not traded on trade_day
                            continue
                        expiry = eval(row[1])[1]
                        type = eval(row[1])[2]
                        strike = eval(row[1])[3]
                        if len(expiry) == 8: #changes 5/8/2020 to 5/08/2020 to deal with sorting issues
                            #print('shortlength')
                            expiry = expiry[:2] + '0' + expiry[2:]
                        if len(expiry) == 9: #changes 6/08/2020 to 06/08/2020
                            expiry = '0' + expiry
                        if type == 'CALL':
                            if expiry in calls: #if this expiry already has been added to calls, we add the new strike price to the list of strike prices for that expiry
                                calls[expiry].append(strike)
                            else: #if this expiry has not yet been added to calls
                                calls[expiry] = [strike]
                        elif type == 'PUT':
                            if expiry in puts:
                                puts[expiry].append(strike)
                            else:
                                puts[expiry] = [strike]
                ordered_calls = {}
                ordered_puts = {}
                for k in sorted(calls):
                    ordered_calls[k] = calls.get(k)
                for k in sorted(puts):
                    ordered_puts[k] = puts.get(k)
                data_to_write.append((avg_spot_row[0], trade_day, ordered_calls, ordered_puts))
                #print(avg_spot_row[0], trade_day, calls, puts)
    with open('earnings_strangles_helper.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data_to_write:
            writer.writerow(row)
#find_strangles_helper() #runtime ~3min

def find_strangles():
    strangles = []
    print("creating avg spot price dictionary...")
    avg_spot_price_dictionary = {} #this dictionary maps each ticker to the dictionary in earnings_avg_spot_prices.csv (which maps each trade_day to the avg spot price of the ticker on that day)
    with open('earnings_avg_spot_prices.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            avg_spot_price_dictionary[row[0]] = eval(row[1])
    print("finding strangles...")
    with open('earnings_strangles_helper.csv') as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == []:
                continue
            avg_spot_price = float(avg_spot_price_dictionary.get(row[0]).get(row[1]))
            calls = eval(row[2])
            puts = eval(row[3])
            good_expiries = [] #list of expiries that appear in both calls and puts
            for expiry in puts:
                if expiry in calls:
                    good_expiries.append(expiry)
            for expiry in good_expiries:
                call_strikes = calls.get(expiry)
                put_strikes = puts.get(expiry)
                for c_strike in call_strikes:
                    c_percent_otm = round(100*(float(c_strike) - avg_spot_price)/avg_spot_price, 3)
                    for p_strike in put_strikes:
                        p_percent_otm = round(100*(avg_spot_price - float(p_strike))/avg_spot_price, 3)
                        otm_difference = round(abs(c_percent_otm - p_percent_otm), 3) #differnce in c_strike's %otm and p_strike's %otm
                        otm_midpoint = round(c_percent_otm/2 + p_percent_otm/2, 3) #avg of c_strike's %otm and p_strike's %otm. Only relevant if otm_difference is a small value.
                        if otm_difference < 8:
                            strangles.append([row[1], row[0], avg_spot_price, otm_difference, otm_midpoint, (expiry, c_strike, c_percent_otm, p_strike, p_percent_otm)])
    otm_differences = []
    with open('earnings_strangles.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['TradeDay', 'Ticker', 'AvgSpotPrice', 'otm_difference', 'otm_midpoint', '(expiry, c_strike, c_%otm, p_strike, p_%otm)'])
        for row in strangles:
            writer.writerow(row)
            otm_differences.append(row[3])
    print(numpy.quantile(otm_differences, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
find_strangles()


def no_earnings(): #looks at changes in options prices for certain non-earnings symbols as a standard for general market conditions
    tickers = ['SPY', 'QQQ', 'IWM', 'SLV', 'XLF', 'GLD', 'GDX', 'VXX']
    with open('earnings_no_earnings.csv', 'w') as f:
        writer = csv.writer(f)
        for ticker in tqdm(tickers):
            options = {} #dictionary of dictionaries: specific options each mapped to their dictionary which maps trade_day to a list of option's prices on that day
            with open('all_combiner.csv') as f2:
                reader = csv.reader(f2)
                print()
                print()
                print("reading in all_combiner.csv and finding satisfying options trades for", ticker, "...")
                for row in tqdm(reader):
                    if row == []:
                        continue
                    if row[1] == ticker: #check that the option trade is for the ticker in question
                        specific_opt = (row[1], row[2], row[3], row[4])
                        if specific_opt in options:
                            if row[26] in options[specific_opt]:
                                options[specific_opt][row[26]].append(row[7])
                            else:
                                options[specific_opt][row[26]] = [row[7]] #each dictionary d is a mapping of trade_day to a list of the option's prices on that day
                        else:
                            options[specific_opt] = {row[26] : [row[7]]} #each specific_opt option is mapped to a dictionary d
            for specific_opt in options:
                inner_dict = options.get(specific_opt)
                if len(inner_dict) < 2:
                    continue
                simplified_inner_dict = {}
                for trade_day in inner_dict:
                    sum = 0
                    for price in inner_dict.get(trade_day):
                        sum += float(price)
                    simplified_inner_dict[trade_day] = round(sum/len(inner_dict.get(trade_day)), 3) #this value is the avg price on trade_day
                writer.writerow([specific_opt, simplified_inner_dict])
                print(specific_opt, simplified_inner_dict)
    print("done.")
#no_earnings()


#things to look at:
#   open interest of option vs stock volume
#   price movement of the stock itself: can look at strangles of a certain %otm, and see how, for example, a 10%otm strangle on 5/08 cost vs 10%otm strangle on 6/08 for a company with earnings on 6/09
#   standard to be compared to should be a comparable spy/vix/qqq strangle on the same time frame.
#   can also look at how a specific strangle performed from 5/08 to 6/08 without taking all factors into account (keeping strike prices the same throughout, maybe even for a stock with lots of price movement leading up to earnings)
#   in the end, try to use intractable algos to find ways for predicting which stocks will experience the best iv surges before earnings. will have to use lots of relevant data, possibly including price movement of stock leading
#       up to earnings, volume of stock, open interest of stock contracts vs normal stock volume, short interest, general state of market/vix, 'hype level' of the stock (how big of a name it is, media attention/twitter mentions?),
#   Even further, it will benefit to know which strangle will work best. For example, sometimes a close atm strangle doesn't gain much leading up to earnings but the far otm strangle gains immensely, or vice versa.
#       to build upon that, we can go further by not looking just at %otm but also at expiry dates. Maybe even will be able to identify if a certain expiry date's volatility hasnt caught up with the rest of the options and is
#       thus underpriced. For example, maybe earnings are on july1st, and the july10 options have increased by 50% in past weeek, but july17 options only increased by 30%




print("time elapsed:", time.time() - start)
