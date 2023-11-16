import benfords_law
import matplotlib.pyplot as plt

def calculate_new_money(a):
    numbers = [1]

    for i in range(1, a):
        new_n = numbers[i-1] * 1.2
        numbers.append(new_n)

    with open("data/geld_bank.csv", "w") as f:
        for n in numbers:
            f.write(str(format(n, 'f')) + "\n")

def plot(a, show_benford=False):
    benfords_law_dist = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
    percentage, _, _ = benfords_law.calculate("geld_bank", 0, 0, a)

    percentage.pop(0)
    y = percentage
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    plt.clf()
    plt.bar(x, y, width=.8)
    plt.xlabel('Ziffer')
    plt.xticks(x)
    plt.ylabel('Prozent')
    plt.title("Geld Bank / " + str(a) + " Tage")
    if show_benford: plt.plot(x, benfords_law_dist, "r--")
    plt.pause(.0000000000001)

if __name__ == "__main__":
    start = 20
    plot(start)

    input("start animation: ")

    for a in range(start, 201):
        plot(a)

    benfords_law_dist = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    input("show benfords law: ")
    plt.plot(x, benfords_law_dist, "r--")
    plt.pause(.0001)

    input("1000: ")
    for a in range(200, 1001, 10):
        plot(a, True)

    input("close: ")
    plt.close()