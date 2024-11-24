import random
from collections import defaultdict

class TriestBase:
    def __init__(self, sample_size):
        """
        初始化 TRIÈST-BASE 算法。
        :param sample_size: 采样子集的大小
        """
        self.sample_size = sample_size
        self.sample = set()  # 用于存储采样的边
        self.t = 0  # 已处理的边的数量
        self.global_triangles = 0  # 全局三角形计数器
        self.adjacency_list = defaultdict(set)  # 存储邻接表

    def process_edge(self, edge):
        """
        处理一条边并更新采样子集与三角形计数。
        :param edge: 需要处理的边 (u, v)
        """
        self.t += 1
        u, v = edge

        if u == v:
            return  # 忽略自环边

        if len(self.sample) < self.sample_size:
            # 采样子集未满，直接添加边
            self.sample.add(edge)
            self.add_edge_to_adjacency_list(u, v)
            self.update_counters(u, v, add=True)
        else:
            # 采样子集已满，按概率替换边
            prob = self.sample_size / self.t
            if random.random() < prob:
                removed_edge = random.choice(list(self.sample))
                self.sample.remove(removed_edge)
                self.remove_edge_from_adjacency_list(*removed_edge)
                self.update_counters(*removed_edge, add=False)
                
                self.sample.add(edge)
                self.add_edge_to_adjacency_list(u, v)
                self.update_counters(u, v, add=True)

    def add_edge_to_adjacency_list(self, u, v):
        """
        将一条边添加到邻接表中。
        :param u: 边的起点
        :param v: 边的终点
        """
        self.adjacency_list[u].add(v)
        self.adjacency_list[v].add(u)

    def remove_edge_from_adjacency_list(self, u, v):
        """
        从邻接表中移除一条边。
        :param u: 边的起点
        :param v: 边的终点
        """
        # 安全删除 u -> v
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u].remove(v)
            if not self.adjacency_list[u]:  # 如果 u 无邻居
                del self.adjacency_list[u]

        # 安全删除 v -> u
        if v in self.adjacency_list and u in self.adjacency_list[v]:
            self.adjacency_list[v].remove(u)
            if not self.adjacency_list[v]:  # 如果 v 无邻居
                del self.adjacency_list[v]

    def update_counters(self, u, v, add):
        """
        更新三角形计数器。
        :param u: 边的起点
        :param v: 边的终点
        :param add: 如果为 True，则增加计数；否则减少计数
        """
        # 找到 u 和 v 的公共邻居
        common_neighbors = self.adjacency_list[u].intersection(self.adjacency_list[v])
        delta = len(common_neighbors)

        if add:
            self.global_triangles += delta
        else:
            self.global_triangles -= delta

    def get_estimate(self):
        """
        返回全局三角形数量的估算值。
        """
        if self.t <= self.sample_size:
            return self.global_triangles
        scaling_factor = ((self.t * (self.t - 1) * (self.t - 2)) /
                          (self.sample_size * (self.sample_size - 1) * (self.sample_size - 2)))
        return int(self.global_triangles * scaling_factor)


