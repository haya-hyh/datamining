from collections import defaultdict
import random

class Triest_Base:
    def __init__(self, M=6):
        self.M = M
        self.S = set()
        self.t = 0
        self.global_counter = 0
        self.local_counters = defaultdict(int)

    def get_shared_neighbours(self, u, v):
        neighbors_u = {edge[1] for edge in self.S if edge[0] == u} | \
                      {edge[0] for edge in self.S if edge[1] == u}
        neighbors_v = {edge[1] for edge in self.S if edge[0] == v} | \
                      {edge[0] for edge in self.S if edge[1] == v}
        return neighbors_u & neighbors_v


    def sample_edge(self, edge):
        if self.t <= self.M:
            return True

        elif random.randrange(self.M) <= (self.M / self.t):
            edge_to_remove = random.choice(tuple(self.S))
            self.S.remove(edge_to_remove)
            self.update_counters(edge_to_remove, increment=False)
            return True
        else:
            return False
            
    def update_counters(self, edge, increment=True):
        u, v = edge
        shared_neighbors = self.get_shared_neighbours(u, v)
        for vertex in shared_neighbors:
            if increment:
                self.global_counter += 1
                self.local_counters[vertex] += 1
                self.local_counters[u] += 1
                self.local_counters[v] += 1
            else:
                self.global_counter -= 1
                self.local_counters[vertex] -= 1
                self.local_counters[u] -= 1
                self.local_counters[v] -= 1

    def estimation(self):
        if self.t <= self.M:
            return self.global_counter
        scaling_factor = max(1, (self.t * (self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2)))
        return self.global_counter * scaling_factor
    
    def read_edges_from_file(file_path):
        edges = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("#"):
                    continue  # Skip comment lines
                parts = line.strip().split()
                if len(parts) == 2:
                    u, v = map(int, parts)
                    edges.append((u, v))
        return edges


    def algo(self, edges):
        for edge in edges:
            self.t += 1
            if self.sample_edge(edge):
                self.S.add(edge)
                self.update_counters(edge, increment=True)
    
    

    
class Triest_Impr:
    def __init__(self, M=6):
        self.M = M
        self.S = set()
        self.t = 0
        self.global_counter = 0
        self.local_counters = defaultdict(int)

    def get_shared_neighbours(self, u, v):
        neighbors_u = {edge[1] for edge in self.S if edge[0] == u} | \
                      {edge[0] for edge in self.S if edge[1] == u}
        neighbors_v = {edge[1] for edge in self.S if edge[0] == v} | \
                      {edge[0] for edge in self.S if edge[1] == v}
        return neighbors_u & neighbors_v


    def sample_edge(self, edge):
        if self.t <= self.M:
            return True

        elif random.randrange(self.M) <= (self.M / self.t):
            edge_to_remove = random.choice(tuple(self.S))
            self.S.remove(edge_to_remove)
            return True
        else:
            return False
            
    def update_counters(self, edge, increment=True):
        u, v = edge
        shared_neighbors = self.get_shared_neighbours(u, v) 
        n = max(1, ((self.t - 1) * (self.t - 2)) / self.M * (self.M - 1))
        for vertex in shared_neighbors:
            if increment:
                self.global_counter += n
                self.local_counters[vertex] += n
                self.local_counters[u] += n
                self.local_counters[v] += n
            else:
                self.global_counter -= n
                self.local_counters[vertex] -= n
                self.local_counters[u] -= n
                self.local_counters[v] -= n

    def estimation(self):
        if self.t <= self.M:
            return self.global_counter
        scaling_factor = max(1, (self.t * (self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2)))
        return self.global_counter * scaling_factor

    def algo(self, edges):
        for edge in edges:
            self.t += 1
            self.update_counters(edge, increment=True)

            if self.sample_edge(edge):
                self.S.add(edge)



if __name__ == "__main__":
    M = 1000
    triest_base = Triest_Base(M)

    # File path to your dataset
    file_path = "web-NotreDame.txt"

    # Read edges from the file
    edges = Triest_Base.read_edges_from_file(file_path)
    triest_base.algo(edges)
    print(triest_base.estimation())

    tries_impr = Triest_Impr(M)
    tries_impr.algo(edges)
    print(tries_impr.estimation())
    

    
        
    


        
