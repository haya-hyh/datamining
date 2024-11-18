from collections import defaultdict
import itertools
from collections.abc import Iterable

class AprioriTid:
    def __init__(self, min_support, min_confidence, n, kmax=2):
        self.s = min_support
        self.c = min_confidence
        self.kmax = kmax
        self.number_transaction = n
        self.frequent_itemset_list = []
        self.rules = []
        self.interest = []
        self.support_info = {}

    def create_C1(self, transactions):
        c_1 = defaultdict(int)
        t_1 = {}
        for tid, transaction in enumerate(transactions):
            t_1[tid] = set()
            for item in transaction:
                itemset = frozenset([item])
                c_1[itemset] += 1
                t_1[tid].add(itemset)
        #filtered c_1
        c_1 = {k: v for k, v in c_1.items() if v >= self.s}
        self.support_info.update(c_1)
        return c_1, t_1

    def apriori_gen(self, l_k_minus1):
        Ck = {}
        items = list(l_k_minus1.keys())
        len_k = len(items)
        for i in range(len_k):
            for j in range(i + 1, len_k):
                l1 = sorted(list(items[i]))
                l2 = sorted(list(items[j]))
                if l1[:-1] == l2[:-1]:
                    candidate = frozenset(l1[:-1] + [l1[-1]] + [l2[-1]])
                    candidate_support = min(
                        l_k_minus1.get(frozenset(subset), 0) for subset in itertools.combinations(candidate, len(candidate) - 1)
                    )
                    if candidate_support >= self.s:
                        Ck[candidate] = candidate_support
                        self.support_info[candidate] = candidate_support
        return Ck

    def generatetk_from_ck(self, tk_minus1, ck, k):
        t_k = {}
        candidate_count = defaultdict(int)
        for tid, candidate_set in tk_minus1.items():
            new_candidate_set = set()
            for c in ck.keys():
                if k == 2:
                    if c[0] in candidate_set and c[1] in candidate_set:
                        new_candidate_set.add(c)
                        candidate_count[c] += 1
                else:
                    c_list = list(c)
                    if frozenset(c_list[:-1]) in candidate_set and frozenset(c_list[:-2] + c_list[-1:]) in candidate_set:
                        new_candidate_set.add(c)
                        candidate_count[c] += 1

            if new_candidate_set:
                t_k[tid] = new_candidate_set
        filtered = {k: v  for k, v in candidate_count.items() if v >= self.s}
        self.support_info.update(filtered)
        return t_k, filtered

    def apriori_search(self, transactions):
        c_1, T = self.create_C1(transactions)
        self.frequent_itemset_list.append(c_1)

        k = 2
        lk = c_1
        Tk = T
        while lk:
            ck = self.apriori_gen(lk)
            Tk, lk = self.generatetk_from_ck(Tk, ck, k)
            if lk:
                self.frequent_itemset_list.append(lk)
            k += 1
            if k > self.kmax:
                break

    def calculate_confidence(self, x, y):
        x_support = self.support_info[x]
        y_support = self.support_info[x.union(y)]
        return y_support / x_support

    def generate_rule(self):
        for frequent_itemsets in self.frequent_itemset_list[1:]:
            for itemset, support in frequent_itemsets.items():
                for i in range(1, len(itemset)):
                    for subset in itertools.combinations(itemset, i):
                        x = frozenset(subset)
                        y = itemset - x
                        if y:
                            confidence = self.calculate_confidence(x, y)
                            interest = confidence - self.support_info[y] / self.number_transaction
                            if confidence >= self.c:
                                self.rules.append((x, y, confidence))
                                self.interest.append((x, y, interest))
