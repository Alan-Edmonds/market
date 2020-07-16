import os

path = 'C:\\Users\\Alan\\Downloads'


files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(file)

for f in files:
    print(f)
