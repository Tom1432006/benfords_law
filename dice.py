from random import randint
import benfords_law
import matplotlib.pyplot as plt

def roll():
    res = 1
    for _ in range(8):
        res *= randint(1, 7)
    
    return res

def calculate():
    numbers = [roll() for _ in range(10000)]

    with open("data/dice.csv", "w") as f:
        for n in numbers:
            f.write(str(n) + "\n")


def plot(a, show_benford=False):
    benfords_law_dist = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
    percentage, _, _ = benfords_law.calculate("dice", 0, 0, a)

    y = percentage
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    plt.clf()
    plt.bar(x, y, width=.8)
    plt.xlabel('Ziffer')
    plt.xticks(x)
    plt.ylabel('Prozent')
    plt.title("Würfel / " + str(a) + " Würfe")
    if show_benford: plt.plot(x, benfords_law_dist, "r--")
    plt.pause(.0000000000001)

if __name__ == "__main__":
    start = 20
    plot(start)

    input("start animation: ")

    for a in range(start, 401, 4):
        plot(a)

    benfords_law_dist = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    input("show benfords law: ")
    plt.plot(x, benfords_law_dist, "r--")
    plt.pause(.0001)

    input("2000: ")
    for a in range(300, 2001, 20):
        plot(a, True)
    
    
    input("10000: ")
    for a in range(2000, 10001, 50):
        plot(a, True)

    input("close: ")
    plt.close()