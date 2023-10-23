numbers = [3, 1]

for i in range(2, 10000):
    numbers.append(numbers[i-1] + numbers[i-2])

with open("data/tom_numbers.csv", "w") as f:
    for n in numbers:
        f.write(str(n) + "\n")