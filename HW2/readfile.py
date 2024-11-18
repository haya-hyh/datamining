def read_dataset(filepath):
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transaction = list(map(int, line.strip().split()))
            transactions.append(transaction)
    return transactions