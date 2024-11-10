import hw1_class as cs
import readfile 

# readfile
documents = readfile.read_json_files('attachments')

# parameter
k = 5
num_permutations = 100
num_bands = 20
rows_per_band = 5
similarity_threshold = 0.00001

# shingling and generate vocabulary
shingler = cs.Shingling(k)
shingles_list = [shingler.shingle(doc) for doc in documents]
vocas = shingler.vocas_from_documents(*documents)

# generate signature
minhashing = cs.MinHashing(num_permutations, vocas)
signatures = {i: minhashing.compute_minhash_signature(shingles) for i, shingles in enumerate(shingles_list)}

# lsh
lsh = cs.LSH(num_bands, rows_per_band)
candidate_pairs = lsh.find_candidate_pairs(signatures)

# test
print("Candidate pairs:")
for pair in candidate_pairs:
    doc1, doc2 = pair
    jaccard_sim = cs.CompareSets.jaccard_similarity(set(shingles_list[doc1]), set(shingles_list[doc2]))
    if jaccard_sim >= similarity_threshold:
        print(f"Documents {doc1} and {doc2} are similar with Jaccard similarity {jaccard_sim:.2f}")

