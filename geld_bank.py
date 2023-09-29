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

if __name__ == "__main__":
    percentage, _, _ = benfords_law.calculate("geld_bank", 0, 0, 20)

    y = percentage
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    plt.clf()
    plt.bar(x, y, width=.8)
    plt.xlabel('Ziffer')
    plt.xticks(x)
    plt.ylabel('Prozent')
    plt.title("Geld Bank / 20")
    plt.pause(.001)

    input("start animation: ")

    for a in range(20, 201):
        percentage, _, _ = benfords_law.calculate("geld_bank", 0, 0, a)

        y = percentage
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        plt.clf()
        plt.bar(x, y, width=.8)
        plt.xlabel('Ziffer')
        plt.xticks(x)
        plt.ylabel('Prozent')
        plt.title("Geld Bank / " + str(a))
        plt.pause(.00000001)

    benfords_law = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    input("show benfords law: ")
    plt.plot(x, benfords_law, "r--")
    plt.pause(.1)
    input("close: ")
    plt.close()