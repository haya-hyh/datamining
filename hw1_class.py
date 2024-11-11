import numpy as np
import hashlib
from collections import defaultdict

'''
A class Shingling that constructs k–shingles of a given length k (e.g., 10) from a given document, computes a hash value for each unique shingle and represents the document in the form of an ordered set of its hashed k-shingles.
'''
class Shingling:
    def __init__(self, k):
        self.k = k

    def shingle(self, document):
        shingles = set()
        for i in range(len(document) - self.k + 1):
            shingle = document[i:i + self.k] # create shingle of length k
            shingle_hash = int(hashlib.md5(shingle.encode('utf-8')).hexdigest(), 16) % (2**32) # hash the shingle and restrict the hash to fit within a 32-bit integer range
            #shingle_hash = hash(shingle) % (2**32)
            shingles.add(shingle_hash) # keep in set to ensure uniqueness
        shingles = list(shingles) # convert back to list
        return shingles
    
    def vocas_from_documents(self, *documents): 
        # take multiple documents to generate the shingles for each document and combine them to know what are the shingles across all documents. universal set. 
        vocas = set()
        for document in documents:
            vocas.update(self.shingle(document))
        vocas = list(vocas)
        return vocas

'''
A class CompareSets computes the Jaccard similarity of two sets of integers – two sets of hashed shingles.
'''
class CompareSets:
    @staticmethod
    def jaccard_similarity(set1, set2):
        return len(set1.intersection(set2)) / len(set1.union(set2))


'''
A class MinHashing that builds a minHash signature (in the form of a vector or a set) of a given length n from a given set of integers (a set of hashed shingles).
'''
class MinHashing:
    def __init__(self, num_permu, vocas,seed=0):
        self.num_permutations = num_permu
        self.seed = seed
        self.vocas = vocas
        self.permutations = self._generate_permu()

    def _generate_permu(self):
        np.random.seed(self.seed)
        permutations = []
        for _ in range(self.num_permutations):
            permutation = np.random.permutation(len(self.vocas))
            permutations.append(permutation)#0 is the first id----------------------------------------------------------
        return permutations

    def compute_minhash_signature(self, shingles):
        signature = []       
        shigles_01list = [1 if i in shingles else 0 for i in self.vocas]    
        for permutation in self.permutations:           
            for i in permutation:
                
                if (shigles_01list[i]==1):
                   signature.append(i) 
                   #signature.append(i+1)    
                   break      
        return signature
    

'''
A class CompareSignatures estimates the similarity of two integer vectors - minhash signatures - as a fraction of components in which they agree.
'''
class CompareSignatures:
    @staticmethod
    def compute_signature_similarity(signature1, signature2):
        count = sum(1 for i in range(len(signature1)) if signature1[i] == signature2[i]) # calculate the number of rows where both signature is the same
        return count / len(signature1)


class LSH:
    def __init__(self, num_bands, num_rows):
        self.b = num_bands
        self.r = num_rows


    def _hash_band(self, band):
        band_str = ''.join(map(str, band))
        #bucket_hash = hash(band_str)
        bucket_hash = hashlib.md5(band_str.encode('utf-8')).hexdigest()
        return bucket_hash
    

    def find_candidate_pairs(self, signatures):
        buckets = defaultdict(list)
        for id, signature in signatures.items():
            for j in range(self.b):
                start = j*self.r
                end = start + self.r
                band = signature[start:end]
                bucket = self._hash_band(band)
                buckets[bucket].append(id)# bucket store id for document
        
        candidate_pairs = set()
        for bucket, candidate in buckets.items():
            if len(candidate) > 1:
                for i in range(len(candidate)):
                    for j in range(i + 1, len(candidate)):
                        candidate_pairs.add((candidate[i], candidate[j]))

        return candidate_pairs


