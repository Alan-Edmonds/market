import csv
from tqdm import tqdm
def reverse_csv(filename):
    with open(filename[:-4] + '_reversed.csv', 'w') as f:
        writer = csv.writer(f)
        with open(filename) as original_f:
            reverse_reader = reversed(list(csv.reader(original_f)))
            for row in tqdm(reverse_reader):
                writer.writerow(row)
reverse_csv('tsla_intraday_5min.csv')

def find_wedges(filename, down_percent, down_minutes, up_percent, up_minutes): #finds a selloff that 'qualifies' these four parameters (a wedge that is even more extreme than the numbers set by the input parameter also qualifies)
    #this logic doesnt account for weird situations where bottom_time + up_minutes <= start_time + down_minutes... but this will only happen with strange inputs for find_wedges()
    data_to_write = []
    start_time, start_price = None, None
    start_row, bottom_row = None, None
    with open(filename) as f:
        reader = csv.reader(f)
        for row in tqdm(reader):
            if row == [] or row[0][2] != '/':
                continue
            t = float(row[0][-5:-3])*60 + float(row[0][-2:]) - 570 #09:30 = 570 - 570, 16:00 = 960 - 570
            #print(row[0], t)
            if t < 0 or t >= 390: #we have hit after hours... time to look at a new trading day
                start_time = None
                continue
            if start_time == None: #set new start_time
                start_time = t
                start_price = float(row[1])
                start_row = row
                continue
            if t == start_time + down_minutes: #potential to find a super steep drop that happened quicker than start_time + down_minutes
                if 100*(float(row[1]) - start_price)/start_price > down_percent: #the price didn't drop enough during this partial timeframe
                    start_time = None
                    continue
                bottom_price = float(row[1])
                bottom_row = row
                continue

            if t == start_time + down_minutes + up_minutes: #having gotten this far with the conditionals, it is already given that t > start_time + down_minutes and a bottom_time has been found
                if 100*(float(row[1]) - bottom_price)/bottom_price < up_percent:
                    start_time = None
                    continue
                data_to_write.append(start_row[:2] + ['--start--'])
                data_to_write.append(bottom_row[:2] + [str(round(100*(float(bottom_row[1]) - float(start_row[1]))/float(start_row[1]), 3)) + '%'])
                data_to_write.append(row[:2] + [str(round(100*(float(row[1]) - float(bottom_row[1]))/float(bottom_row[1]), 3)) + '%'])
    print('wedges found:', len(data_to_write)/3)
    with open('wedges.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Time','Open','%Change'])
        for row in data_to_write:
            writer.writerow(row)
find_wedges('tsla_intraday_5min_reversed.csv', -2, 10, 2, 30) #this means down at least 3% in 10 minutes, then rebouneded at least 3% in 30 minutes
