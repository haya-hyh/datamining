from collections import defaultdict
import itertools
from collections.abc import Iterable
#c_k contain itemset and support while lk and cK contain only item set 
#t_k contain id and itemset
#k is the length of itemset
#support_info contain all the frequentitemset and their support
class AprioriTid:
    def __init__(self, min_support, min_confidence):
        self.s = min_support
        self.c = min_confidence
        self.frequent_itemset_list = []
        self.rules = []
        self.support_info={}

    # Create the first candidate set (C1) and transaction list (T1).
    def create_C1(self, transactions):
        c_1 = defaultdict(int)
        t_1 = {}
        for tid, transaction in enumerate(transactions):
            for item in transaction:
                c_1[frozenset([item])] += 1  # Count occurrence of each item
            t_1[tid] = {frozenset([item]) for item in transaction}  # Map transaction ID to itemsets
        return c_1, t_1

    # def filter_candidates(self, candidates):
    #     return [key for key, value in candidates.items() if value >= self.s]
    
    # Filter C_1 based on the minimum support threshold.
    def filter_candidates(self, candidates):
        filtered_candidates = []
        for key, value in candidates.items():
            if value >= self.s:
                filtered_candidates.append(key)  
                self.support_info[key] = value  
        return filtered_candidates 
    
    # Generate candidate itemsets of size k (Ck) from frequent itemsets of size k-1.
    def apriori_gen(self, l_k_minus1):
        Ck = []
        len_k = len(l_k_minus1)
        for i in range(len_k):
            for j in range(i + 1, len_k):
                # Create sorted lists of two itemsets
                l1 = sorted(list(l_k_minus1[i])) if isinstance(l_k_minus1[i], Iterable) else [l_k_minus1[i]]
                l2 = sorted(list(l_k_minus1[j])) if isinstance(l_k_minus1[j], Iterable) else [l_k_minus1[j]]
                if l1[:-1] == l2[:-1]:  # Check if all but the last elements are the same
                    candidate = frozenset(l1[:-1] + [l1[-1]] + [l2[-1]])
                    # Check if all subsets of size k-1 are frequent
                    if all(frozenset(subset) in l_k_minus1 for subset in itertools.combinations(candidate, len(candidate) - 1)):
                        Ck.append(candidate)
        return Ck

    # Generate Tk (transaction ID to candidate itemsets mapping) from Ck.
    def generatetk_from_ck(self, tk_minus1, ck):
        t_k = {}
        for tid, candidate_set in tk_minus1.items():
            new_candidate_set = set()
            for c in ck:
                c_list = list(c)
                if len(c_list) > 1:
                    # Check if subsets of c are in the current transaction's candidates
                    if frozenset(c_list[:-1]) in candidate_set and frozenset(c_list[:-2] + c_list[-1:]) in candidate_set:
                        new_candidate_set.add(c)
                else:
                    if frozenset(c_list) in candidate_set:
                        new_candidate_set.add(c)
            if new_candidate_set:
                t_k[tid] = new_candidate_set # Update Tk with new candidates
        return t_k

    # Count candidate occurrences in Tk and filter based on support threshold.
    def filter_candidates_from_Tk(self,Tk):
        candidate_count = defaultdict(int)
        for candidate_set in Tk.values():
            for candidate in candidate_set:
                candidate_count[candidate] += 1  # Count occurrences of each candidate
        filtered = []
        for candidate, count in candidate_count.items():
            if count >= self.s:
                filtered.append(candidate)  # Keep candidates meeting the support threshold
                self.support_info[candidate] = count  # Save the support count
        return filtered

    # Perform the Apriori-TID algorithm to find all frequent itemsets.
    def apriori_search(self, transactions):
        c_1, T = self.create_C1(transactions)  # Create initial candidate set and transaction mapping
        l1 = self.filter_candidates(c_1)  # Filter C_1
        self.frequent_itemset_list.append(l1)  

        k = 2
        lk = l1
        Tk = T
        while len(lk) != 0:  # Repeat until no more frequent itemsets are found
            ck = self.apriori_gen(lk)  # Generate candidate itemsets of size k
            Tk = self.generatetk_from_ck(Tk, ck)  # Update Tk with new candidates
            lk = self.filter_candidates_from_Tk(ck, Tk)  # Filter candidates to get frequent itemsets
            if lk:
                self.frequent_itemset_list.append(lk) 
            k += 1

# bonus part
    # Calculate the confidence of a rule X -> Y.
    def calculate_confidence(self, x, y):
        "x->y"
        x_support = self.support_info[x]
        y_support = self.support_info[x.union(y)]
        return y_support / x_support


    # Generate association rules from the discovered frequent itemsets.
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