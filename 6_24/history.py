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
                print(row[36])
                print()
                print()
                break
#printer(('VXX', '5/15/2020', 'PUT', '250'))
printer(('MU',        '6/19/2020',  'CALL',          '65'))

for i in range(4):
    print()
print("time elapsed:", time.time() - start)
