import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import math

def get_probability(x, digit):
    if digit == 1:
        return np.log10(1+1/x)*100

    # this formula only works for digits grater than 1
    # variables for the formula
    lower = int(math.pow(10, digit-2))
    upper = int(math.pow(10, digit-1)-1)

    return sum(np.log10(1+(1/(10*k+x)))*100 for k in range(lower,  upper+1))

def calculate(filename, start_row = 1, collumn = 1, end_row = None, last_digit = False, digit=1, amount=1):
    # load the data 
    data = []
    with open("data/" + filename + ".csv") as csvF:
        reader = csv.reader(csvF)
        for row in reader:
            if row != []: data.append(row)

    # save the distribution
    min = 0
    if digit == 1 and amount == 1 and not last_digit: min += 1
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
            number = int(number)
            
            # remove minus
            if number < 0: number *= -1

            if amount > 1:
                if number >= max:
                    d[int(str(number)[digit-1:amount+(digit-1)])-1] += 1
            else:
                if last_digit:
                    d[int(str(number)[-1])] += 1
                elif len(str(number)) > digit-1:
                    if digit == 1: d[int(str(number)[digit-1])-1] += 1
                    else:          d[int(str(number)[digit-1])] += 1

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

    if last_digit: digit = 1
    if last_digit: amount = 1
    #endregion
    min = int(math.pow(10, amount-1))
    if digit != 1 or last_digit: min = 0
    max = int(math.pow(10, amount))

    percentage, value_sum, spalte_name = calculate(filename, start_row, collumn, ending_row, last_digit, digit, amount)

    if spalte_name != "": print("Spalte: " + spalte_name)

    # generate benfords law
    benfords_law = []
    start = 1 if digit == 1 else 0
    for x in range(start, 10):
        benfords_law.append(round(get_probability(x, digit), 2))

    if amount == 1:
        for i in range(len(percentage)-1):
            if digit >= 2:   print(f"{i}: {percentage[i]}%  --- {benfords_law[i]}%")
            elif last_digit: print(f"{i}: {percentage[i]}%")
            else:            print(f"{i+1}: {percentage[i]}%  --- {benfords_law[i]}%")

    print("Errechnet aus " + str(value_sum) + " Datenwerten.")

    if plot_data:
        if digit == 1 and not last_digit:
            x = np.linspace(min, max-1, 100)
            for i in range(min,max):
                plt.bar(i, percentage[i-1], width=.8, color="#1f77b4")
        else:
            x = np.linspace(min, max-1, 100)
            for i in range(min,max):
                plt.bar(i, percentage[i], width=.8, color="#1f77b4")

        if (digit == 1 or amount == 1) and not ignore_bendford:
            plt.plot(x, get_probability(x, digit), "r--")

        plt.xlabel('Ziffer')
        plt.xticks([x for x in range(min,max, math.ceil(max/20))])
        plt.ylabel('Prozent')
        if start_row > 0: plt.title(filename + " / " + spalte_name)
        else:             plt.title(filename)
        plt.show()