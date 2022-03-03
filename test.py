import csv

with open('grade.csv') as csvfile:

    rows = list(csv.reader(csvfile))
    print rows
    for row in rows:
        print(row[0])
