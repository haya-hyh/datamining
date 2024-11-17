import apriorimodified as ap
import readfile
import aprioritid as aptid
import time
transactions = readfile.read_dataset('T10.dat')
min_support = 50
min_confidence = 0.8

# #apriori part
# Start_time_apriori = time.time()
# apriori = ap.Apriori(min_support)
# apriori.apriori_search(transactions)
# Stup_time_apriori = time.time()

# for i, itemsets in enumerate(apriori.frequent_itemset_list):
#     print(f" {i + 1}-itemset{itemsets}")




#tid part
Start_time_aprioritid = time.time()
apriori_tid = aptid.AprioriTid(min_support, min_confidence)
apriori_tid.apriori_search(transactions)
Stop_time_aprioritid = time.time()


for i, frequent_itemsets in enumerate(apriori_tid.frequent_itemset_list):
    print(f"Frequent {i + 1}-itemsets: {frequent_itemsets}")




# to do list 
# compare time between ap and aptid (select a appropriate dataset part)
