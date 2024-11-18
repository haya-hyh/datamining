from collections import defaultdict
import itertools

class AprioriTid:
    def __init__(self, min_support, min_confidence, kmax=2):
        self.min_support = min_support
        self.c = min_confidence
        self.kmax = kmax
        self.frequent_itemset_list = []
        self.rules = []
        self.support_info={}

    def create_transactions(self, path):
        with open(path, 'r') as inFile:
            transactions = [frozenset(line.strip().split(" ")) for line in inFile]
        return transactions

    def generate_singletons(self, transactions):
        candidate_set = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                candidate_set[frozenset([item])] += 1
        return candidate_set

    def filter_candidates(self, candidates):
        filtered_candidates = {}
        for itemset, count in candidates.items():
            if count >= self.min_support:
                filtered_candidates[itemset] = count
                self.support_info[itemset] = count
        return filtered_candidates

    def apriori_gen(self, previous_itemset):
        candidate_set = {}
        previous_items = list(previous_itemset.keys())
        for x, y in itertools.combinations(previous_items, 2):
            if len(x.union(y)) == len(x) + 1:
                candidate_set[x.union(y)] = 0
        return candidate_set

    def scan_transactions(self, transactions, candidates, k):
        if k <= 4:
            # Optimize with intersections for smaller sets
            candidates_list = set(candidates.keys())
            new_transactions = []
            for transaction in transactions:
                comb_list = set(
                    frozenset(comb) for comb in itertools.combinations(transaction, k)
                )
                common = candidates_list & comb_list
                for el in common:
                    candidates[el] += 1
                if common:
                    new_transactions.append(transaction)
            return candidates, new_transactions
        else:
            # Full subset checking for larger sets
            new_transactions = []
            for transaction in transactions:
                keep = False
                for candidate in candidates.keys():
                    if candidate.issubset(transaction):
                        candidates[candidate] += 1
                        keep = True
                if keep:
                    new_transactions.append(transaction)
            return candidates, new_transactions

    def apriori_search(self, path):
        transactions = self.create_transactions(path)
        singletons = self.generate_singletons(transactions)
        filtered_singletons = self.filter_candidates(singletons)
        self.frequent_itemset_list.append(filtered_singletons)

        current_itemset = filtered_singletons
        k = 2
        while current_itemset and k <= self.kmax:
            print(f"Generating candidates of size {k}...")
            candidates = self.apriori_gen(current_itemset)
            print(f"Scanning transactions for {len(candidates)} candidates...")
            candidates, transactions = self.scan_transactions(transactions, candidates, k)
            current_itemset = self.filter_candidates(candidates)
            if current_itemset:
                self.frequent_itemset_list.append(current_itemset)
            print(f"Found {len(current_itemset)} frequent itemsets of size {k}")
            k += 1

        return self.frequent_itemset_list
    

# bonus part
    def calculate_confidence(self, x, y):
        "x->y"
        x_support = self.support_info[x]
        y_support = self.support_info[x.union(y)]
        return y_support / x_support



    def generate_rule(self):
        for frequent_itemsets in self.frequent_itemset_list[1:]:
            for itemset in frequent_itemsets:
                for i in range(1, len(itemset)):
                    for subset in itertools.combinations(itemset, i):
                        x = frozenset(subset)                       
                        y = itemset - x
                        if y:
                            confidence = self.calculate_confidence(x, y)
                            if confidence >= self.c:
                                self.rules.append((x, y, confidence))


# Usage Example
if __name__ == "__main__":
    apriori_tid = AprioriTid(min_support=1000, min_confidence=0.5, kmax=10)
    path = "dataset/T10I4D100K.dat"
    result = apriori_tid.apriori_search(path)
    print("Final Frequent Itemsets:")
    for level, itemsets in enumerate(result, 1):
        print(f"Level {level}: {len(itemsets)} itemsets")
    apriori_tid.generate_rule()
    print(apriori_tid.rules)
