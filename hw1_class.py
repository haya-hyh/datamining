import random
import numpy as np
import hashlib
from collections import defaultdict

class Shingling:
    def __init__(self, k):
        self.k = k

    def shingle(self, document):
        shingles = set()
        for i in range(len(document) - self.k + 1):
            shingle = document[i:i + self.k]
            shingle_hash = int(hashlib.md5(shingle.encode('utf-8')).hexdigest(), 16) % (2**32)
            #shingle_hash = hash(shingle) % (2**32)
            shingles.add(shingle_hash)
        shingles = list(shingles)
        return shingles
    
    def vocas_from_documents(self, *documents):      
        vocas = set()
        for document in documents:
            vocas.update(self.shingle(document))
        vocas = list(vocas)
        return vocas


class CompareSets:
    @staticmethod
    def jaccard_similarity(set1, set2):
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)




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
    

class CompareSignatures:
    @staticmethod
    def compute_signature_similarity(signature1, signature2):
        count = sum(1 for i in range(len(signature1)) if signature1[i] == signature2[i])
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


