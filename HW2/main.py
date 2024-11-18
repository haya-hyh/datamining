import readfile
import aprioritid as aptid
import time


k = 5 #number of transaction 
transactions = readfile.read_dataset('test.dat',k)
min_support = 2
min_confidence = 0.1

# #apriori part
# Start_time_apriori = time.time()
# apriori = ap.Apriori(min_support)
# apriori.apriori_search(transactions)
# Stup_time_apriori = time.time()

# for i, itemsets in enumerate(apriori.frequent_itemset_list):
#     print(f" {i + 1}-itemset{itemsets}")




#tid part
Start_time_aprioritid = time.time()
apriori_tid = aptid.AprioriTid(min_support, min_confidence,k)
apriori_tid.apriori_search(transactions)
Stop_time_aprioritid = time.time()


for i, frequent_itemsets in enumerate(apriori_tid.frequent_itemset_list):
    print(f"Frequent {i + 1}-itemsets: {frequent_itemsets}")
    
# apriori_tid.generate_rule()
print(apriori_tid.interest)
print(apriori_tid.rules)

# to do list 
# compare time between ap and aptid (select a appropriate dataset part)
# need a dataset and good parameter to test generate rule function
