import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import math

benfords_law = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
benfords_law_second = [11.97, 11.39, 10.88, 10.43, 10.03, 9.67, 9.34, 9.04, 8.76, 8.50]

def calculate(filename, start_row = 1, collumn = 1, end_row = None, last_digit = False, digit=1):
    # load the data 
    data = []
    with open("data/" + filename + ".csv") as csvF:
        reader = csv.reader(csvF)
        for row in reader:
            if row != []: data.append(row)

    # save the distribution
    d = [0 for _ in range(9)]
    if digit != 1 or last_digit: d.append(0)

    # get the n digit
    nono_chars = ["-", "", "NA", "0"]
    i = 0
    spalte = ""
    for row in data:
        if i == 0 and start_row >= 1: spalte = row[collumn]

        if i >= start_row and row[collumn] not in nono_chars:
            # prepare the number to read the digits
            number = row[collumn].replace(",", "") # remove kommas
            number = row[collumn].replace(".", "") # remove dots
            number = int(number)
            
            # remove minus
            if number < 0: number *= -1

            if last_digit:
                d[int(str(number)[-1])] += 1
            elif len(str(number)) > digit-1:
                if digit == 1: d[int(str(number)[digit-1])-1] += 1
                else:          d[int(str(number)[digit-1])] += 1

        i += 1
        if end_row != None and i >= end_row: break

    # calculate percentage
    value_sum = sum(d)
    perc = [0 for _ in range(9)]
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

    parser.add_argument("-i", "--ignore-bendford", action='store_true')

    args = parser.parse_args()

    filename = args.data
    start_row = int(args.starting_row)
    if args.ending_row == None:
        ending_row = None
    else:
        ending_row = int(args.ending_row)
    collumn = int(args.collumn)
    last_digit = args.last_digit
    plot_data = args.plot_data
    digit = int(args.digit)
    ignore_bendford = args.ignore_bendford

    if last_digit: digit = 1
    #endregion

    percentage, value_sum, spalte_name = calculate(filename, start_row, collumn, ending_row, last_digit, digit)

    if spalte_name != "": print("Spalte: " + spalte_name)

    for i in range(len(percentage)):
        if digit == 2:                print(f"{i}: {percentage[i]}%  --- {benfords_law_second[i]}%")
        elif digit > 2 or last_digit: print(f"{i}: {percentage[i]}%")
        else:                         print(f"{i+1}: {percentage[i]}%  --- {benfords_law[i]}%")

    print("Errechnet aus " + str(value_sum) + " Datenwerten.")

    if plot_data:
        if digit == 1 and not last_digit:
            x = np.linspace(1, 9, 100)
            for i in range(1,10):
                plt.bar(i, percentage[i-1], width=.8, color="#1f77b4")
        else:
            x = [i for i in range(0, 10)]
            for i in range(0,10):
                plt.bar(i, percentage[i], width=.8, color="#1f77b4")

        if not last_digit and not ignore_bendford and digit == 1:
            plt.plot(x, np.log10(1+(1/x))*100, "r--")
        elif not ignore_bendford and digit == 2:
            plt.plot(x, benfords_law_second, "r--")

        plt.xlabel('Ziffer')
        plt.xticks([x for x in range(0,10)])
        plt.ylabel('Prozent')
        if start_row > 0: plt.title(filename + " / " + spalte_name)
        else:             plt.title(filename)
        plt.show()