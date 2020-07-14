import csv
import re
from tqdm import tqdm
from print import printer
printer('StockScreenerResults_20200710.csv')

def screen(filename):
    data_to_write = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row == [] or row[1] == 'Name' or row[3] == '' or row[10] == '' or row[11] == '' or row[12] == '' or row[13] == '':
                continue
            if float(row[13]) < 0.02 and float(row[12]) < 0.02 and float(row[11]) < 0.02 and float(row[10]) < 0.02 and float(row[3]) < 0.02:
                if float(row[13]) > -0.02 and float(row[12]) > -0.02 and float(row[11]) > -0.02 and float(row[10]) > -0.015 and float(row[3]) > -0.0065:
                    if float(row[2]) > 15 and float(row[5]) > 2000000:
                        data_to_write.append(row[:3])
    with open('screened.csv', 'w') as f:
        writer = csv.writer(f)
        for row in tqdm(data_to_write):
            writer.writerow(row)
screen('StockScreenerResults_20200710.csv')
