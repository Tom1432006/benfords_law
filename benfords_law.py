import csv
import argparse
import matplotlib.pyplot as plt

# console values
parser = argparse.ArgumentParser(prog="benfords_law", description="shows how often a non 0 digit appears as the lead digit of a given dataset")
parser.add_argument("-d", "--data", required=True)
parser.add_argument("-s", "--starting_row", default=1)
parser.add_argument("-c", "--collumn", default=1)
parser.add_argument("-l", "--last-digit", action='store_true')
parser.add_argument("-p", "--plot-data", action='store_true')

args = parser.parse_args()

filename = args.data
start_row = int(args.starting_row)
collumn = int(args.collumn)
last_digit = args.last_digit
plot_data = args.plot_data

benfords_law = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

# load the data
data = []
with open("data/" + filename + ".csv") as csvF:
    reader = csv.reader(csvF)
    for row in reader:
        if row != []:
            data.append(row)

# save the distribution
d = [0 for _ in range(9)]

# get the first digit
nono_chars = ["-", "", "NA", "0"]
i = 0
for row in data:
    if i == 0 and start_row >= 1:
        spalte = row[collumn]
        print("Spalte: " + spalte)

    if i >= start_row and row[collumn] not in nono_chars:
        number = int(abs(float(row[collumn].replace(",", ""))))
        
        if last_digit:
            if int(str(number)[-1]) == 0: continue
            d[int(str(number)[-1])-1] += 1
        else:
            d[int(str(number)[:1])-1] += 1
    i += 1

# calculate percentage
value_sum = sum(d)
perc = [0 for _ in range(9)]

if value_sum == 0:
    exit("Es gibt dazu keine Daten")

for i in range(len(d)):
    percentage = round((d[i] / value_sum) * 100, 2)
    perc[i] = percentage
    if last_digit:
        print(f"{i+1}: {percentage}%")
    else:
        print(f"{i+1}: {percentage}%  --- {benfords_law[i]}%")
print("Errechnet aus " + str(value_sum) + " Datenwerten.")

if plot_data:
    y = perc
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    plt.bar(x, y, width=.8)
    if not last_digit:
        plt.plot(x, benfords_law, "r--")
    plt.xlabel('Ziffer')
    plt.xticks(x)
    plt.ylabel('Prozent')
    plt.title(filename + " / " + spalte)
    plt.show()
