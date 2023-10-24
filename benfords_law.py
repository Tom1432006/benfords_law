import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import os

def check_data(filename, start_row = 1, collumn = 1, end_row = None, last_digit = False, digit=1, amount=1):
    if not os.path.exists("data/" + filename + ".csv"):
        exit("Den Datensatz "+filename+".csv gibt es nicht!")

    # load the data 
    data = []
    with open("data/" + filename + ".csv") as csvF:
        reader = csv.reader(csvF)
        for row in reader:
            if row != []: data.append(row)

    if len(data[0]) < collumn:
        exit("Diese Spalte gibt es nicht")

def get_probability(x, digit):
    # variables for the formula
    lower = int(math.pow(10, digit-2))
    upper = int(math.pow(10, digit-1)-1)

    return sum(np.log10(1+(1/(10*k+x))) for k in range(lower,  upper+1))*100

def calculate(filename, start_row = 1, collumn = 1, end_row = None, last_digit = False, digit=1, amount=1):
    check_data(filename, start_row, collumn, end_row, last_digit, digit, amount)

    # load the data 
    data = []
    with open("data/" + filename + ".csv") as csvF:
        reader = csv.reader(csvF)
        for row in reader:
            if row != []: data.append(row)

    # save the distribution
    min = 0
    max = int(math.pow(10, amount))
    d = [0 for _ in range(min, max)]

    # get the n digit
    nono_chars = ["-", "", "NA", "0"]
    i = 0
    spalte = ""
    for row in data:
        if i == 0 and start_row >= 1: spalte = row[collumn]

        if i >= start_row and row[collumn] not in nono_chars:
            # prepare the number to read the digits
            number = row[collumn]
            number = number.replace(",", "") # remove kommas
            number = number.replace(".", "") # remove dots
            number.lstrip("0") # remove leading zeros
            number.lstrip("-") # remove sign

            if amount > 1:
                if last_digit:
                    d[int(str(number)[-amount:])] += 1
                elif math.pow(10, len(str(number))) >= max:
                    d[int(str(number)[digit-1:amount+(digit-1)])] += 1
            else:
                if last_digit: d[int(str(number)[-1])] += 1
                elif len(str(number)) > digit-1: d[int(str(number)[digit-1])] += 1

        i += 1
        if end_row != None and i >= end_row: break

    # calculate percentage
    value_sum = sum(d)
    perc = [0 for _ in range(min, max)]
    if digit != 1 or last_digit: perc.append(0)

    if value_sum == 0: exit("Es gibt dazu keine Daten")

    for i in range(len(d)):
        percentage = round((d[i] / value_sum) * 100, 2)
        perc[i] = percentage

    return perc, value_sum, spalte

if __name__ == "__main__":
    #region console values
    parser = argparse.ArgumentParser(prog="benfords_law", description="shows how often a non 0 digit appears as the lead digit of a given dataset")
    parser.add_argument("-d", "--data", required=True)
    parser.add_argument("-s", "--starting_row", default=1)
    parser.add_argument("-e", "--ending_row", default=None)
    parser.add_argument("-c", "--collumn", default=1)
    parser.add_argument("-l", "--last-digit", action='store_true')
    parser.add_argument("-p", "--plot-data", action='store_true')
    parser.add_argument("-t", "--digit", default=1)
    parser.add_argument("-a", "--amount", default=1)

    parser.add_argument("-i", "--ignore-bendford", action='store_true')

    args = parser.parse_args()

    filename = args.data
    start_row = int(args.starting_row)
    ending_row = None
    if args.ending_row != None:  ending_row = int(args.ending_row)
    collumn = int(args.collumn)
    last_digit = args.last_digit
    plot_data = args.plot_data
    digit = int(args.digit)
    amount = int(args.amount)
    ignore_bendford = args.ignore_bendford

    if last_digit: 
        digit = 1
        print("-d wurde zurückgesetzt")
    #endregion
    
    # calculate the min and max of the possible combinations
    min = int(math.pow(10, amount-1))
    if digit != 1 or last_digit: min = 0
    max = int(math.pow(10, amount))

    # perform the main calculation
    percentage, value_sum, spalte_name = calculate(filename, start_row, collumn, ending_row, last_digit, digit, amount)
    
    if spalte_name != "": print("Spalte: " + spalte_name)

    # generate benfords law
    benfords_law = [0 for _ in range(max)]
    start = 1 if digit == 1 else 0
    if not last_digit:
        for x in range(min, max):
            benfords_law[x] = round(get_probability(x, digit), 2)

    if amount == 1:
        for i in range(min, max):
            if last_digit: print(f"{i}: {percentage[i]}%")
            else:          print(f"{i}: {percentage[i]}%  --- {benfords_law[i]}%")

    if not last_digit:
        standartabweichung = round(math.sqrt((1/(max-1-min)) * math.pow(sum([abs(percentage[i] - benfords_law[i]) for i in range(min, max-1)]), 2)), 3)
        print("Standartabweichung: " + str(standartabweichung))
        
    print("Errechnet aus " + str(value_sum) + " Datenwerten.")

    width = .8
    if amount > 1: width = 1
    if plot_data:
        x = np.linspace(min, max-1, 100)
        for i in range(min,max):
            plt.bar(i, percentage[i], width=width, color="#1f77b4")

        if (digit == 1 or amount == 1) and not ignore_bendford and not last_digit:
            plt.plot(x, get_probability(x, digit), "r--")

        plt.xlabel('Ziffer')
        plt.xticks([x for x in range(min,max, math.ceil(max/20))])
        plt.ylabel('Prozent')
        if start_row > 0: plt.title(filename + " / " + spalte_name)
        else:             plt.title(filename)
        plt.show()