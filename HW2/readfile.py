import random

def read_dataset(filepath, k=1000):
    "randomly select k lines data"
    transactions = []
    with open(filepath, 'r') as file:
        reservoir = []
        for i, line in enumerate(file):
            stripped_line = line.strip().split()
            if i < k:
                reservoir.append(list(set(map(int, stripped_line))))
            else:
                j = random.randint(0, i)
                if j < k:
                    reservoir[j] = list(set(map(int, stripped_line)))
        transactions = reservoir
    return transactions
