from collections import defaultdict
import itertools
from collections.abc import Iterable

class Apriori:
    def __init__(self, min_support):
        self.s = min_support
        self.frequent_itemset_list = []

    def create_C1(self, transactions):
        c_1 = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                c_1[frozenset([item])] += 1  # Use frozenset for immutability
        return c_1

    def filter_candidates(self, candidates):
        filtered_candidates = []
        for key, value in candidates.items():
            if value >= self.s:
                filtered_candidates.append(key)
        return filtered_candidates

    def apriori_gen(self, l_k_minus1):
        Ck = []
        len_k = len(l_k_minus1)
        # join step
        for i in range(len_k):
            for j in range(i + 1, len_k):
                l1 = sorted(list(l_k_minus1[i])) if isinstance(l_k_minus1[i], Iterable) else [l_k_minus1[i]]
                l2 = sorted(list(l_k_minus1[j])) if isinstance(l_k_minus1[j], Iterable) else [l_k_minus1[j]]
                # same for k-1 items
                if l1[:-1] == l2[:-1]:
                    candidate = l1[:-1] + [l1[-1]] + [l2[-1]] if l1[-1] < l2[-1] else l1[:-1] + [l2[-1]] + [l1[-1]]
                    candidate = frozenset(candidate)
                    # prune step
                    if all(frozenset(subset) in l_k_minus1 for subset in itertools.combinations(candidate, len(candidate) - 1)):
                        Ck.append(candidate)
        return Ck

    def count_sublists(self, transactions, mini_list):
        mini_set = set(mini_list)
        count = 0
        for transaction in transactions:
            transaction_set = set(transaction)
            if mini_set.issubset(transaction_set):
                count += 1
        return count

    def apriori_search(self, transactions):
        c_1 = self.create_C1(transactions)
        l1 = self.filter_candidates(c_1)
        self.frequent_itemset_list.append(l1)
        
        k = 2
        lk = l1
        while len(lk) >= 1:
            ck = self.apriori_gen(lk)
            c_k = {}
            for item in ck:
                c_k[item] = self.count_sublists(transactions, item)
            lk = self.filter_candidates(c_k)
            if lk:
                self.frequent_itemset_list.append(lk)
            k += 1
            if(k>=3):break
