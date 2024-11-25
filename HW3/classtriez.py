import random
from collections import defaultdict

class TriestBase:
    def __init__(self, sample_size):
        self.sample_size = sample_size
        self.sample = set()  # Stores the edge sample.
        self.t = 0  # Tracks the number of processed edges.
        self.global_triangles = 0  # Counter for global triangles.
        self.neigbor_list = defaultdict(set)  # Stores the adjacency list.

    def normalize_edge(self, edge):
        """
        In couting triagnles,should have edges(1,2)=(2,1)
        """
        u, v = edge
        return (u, v) if u < v else (v, u)

    def process_edge(self, edge):
        edge = self.normalize_edge(edge)

        if edge in self.sample:
            return  # Skip duplicate edges without incrementing t.

        u, v = edge
        if u == v:
            return  

        self.t += 1  # Increment t only for unique edges.

        if len(self.sample) < self.sample_size:
            # Add edge to the sample directly if the sample is not full.
            self.sample.add(edge)
            self.add_edge_to_neigbor_list(u, v)
            self.update_counters(u, v, add=True)
        else:
            # Replace an edge in the sample with a probability.
            head = self.sample_size / self.t
            if random.random() < head:
                removed_edge = random.choice(list(self.sample))
                self.sample.remove(removed_edge)
                self.remove_edge_from_neigbor_list(*removed_edge)
                self.update_counters(*removed_edge, add=False)

                self.sample.add(edge)
                self.add_edge_to_neigbor_list(u, v)
                self.update_counters(u, v, add=True)

    def add_edge_to_neigbor_list(self, u, v):
        self.neigbor_list[u].add(v)
        self.neigbor_list[v].add(u)

    def remove_edge_from_neigbor_list(self, u, v):
        if u in self.neigbor_list and v in self.neigbor_list[u]:
            self.neigbor_list[u].remove(v)
            # if not self.neigbor_list[u]:  
            #     del self.neigbor_list[u]

        if v in self.neigbor_list and u in self.neigbor_list[v]:
            self.neigbor_list[v].remove(u)
            # if not self.neigbor_list[v]: 
            #     del self.neigbor_list[v]

    def update_counters(self, u, v, add):
        common_neighbors = self.neigbor_list[u].intersection(self.neigbor_list[v])
        delta = len(common_neighbors)

        if add:
            self.global_triangles += delta
        else:
            self.global_triangles -= delta

    def estimate(self):
        if self.t <= self.sample_size:
            return self.global_triangles
        factor = ((self.t * (self.t - 1) * (self.t - 2)) /
                          (self.sample_size * (self.sample_size - 1) * (self.sample_size - 2)))
        return int(self.global_triangles * factor)


class TriestImpr:
    def __init__(self, sample_size):
        self.sample_size = sample_size
        self.sample = set()  # Stores the edge sample.
        self.t = 0  # Tracks the number of processed edges.
        self.global_triangles = 0  # Counter for global triangles.
        self.neigbor_list = defaultdict(set)  # Stores the neigbor list.

    def normalize_edge(self, edge):
        u, v = edge
        return (u, v) if u < v else (v, u)

    def process_edge(self, edge):
        edge = self.normalize_edge(edge)
        u, v = edge
        if u == v:
            return  

        if edge in self.sample:
            return  
        self.t += 1 

         
        weight = self.get_weight()
        self.update_counters(u, v, add=True, weight=weight)

        if len(self.sample) < self.sample_size:
            self.sample.add(edge)
            self.add_edge_to_neigbor_list(u, v)
        else:
            prob_head = self.sample_size / self.t
            if random.random() < prob_head:
                removed_edge = random.choice(list(self.sample))
                self.sample.remove(removed_edge)
                self.remove_edge_from_neigbor_list(*removed_edge)
                # self.update_counters(*removed_edge, add=False, weight=weight)
                self.sample.add(edge)
                self.add_edge_to_neigbor_list(u, v)

    def get_weight(self):
        if self.t <= 2:
            return 1
        return max(1, ((self.t - 1) * (self.t - 2)) / (self.sample_size * (self.sample_size - 1)))

    def add_edge_to_neigbor_list(self, u, v):
        self.neigbor_list[u].add(v)
        self.neigbor_list[v].add(u)

    def remove_edge_from_neigbor_list(self, u, v):
        if u in self.neigbor_list and v in self.neigbor_list[u]:
            self.neigbor_list[u].remove(v)
            # if not self.neigbor_list[u]:
            #     del self.neigbor_list[u]

        if v in self.neigbor_list and u in self.neigbor_list[v]:
            self.neigbor_list[v].remove(u)
            # if not self.neigbor_list[v]:
            #     del self.neigbor_list[v]

    def update_counters(self, u, v, add, weight):
        common_neighbors = self.neigbor_list[u].intersection(self.neigbor_list[v])
        delta = len(common_neighbors) * weight

        if add:
            self.global_triangles += delta
        else:
            self.global_triangles -= delta

    def estimate(self):
        return int(self.global_triangles)
