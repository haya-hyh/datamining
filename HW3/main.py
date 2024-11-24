import readfile as rf
import classtriez as cs

# Load dataset
dataset_path = "web-NotreDame/web-NotreDame.txt"
edges = rf.read_dataset(dataset_path)

# Initialize algorithms
sample_size = 1000
triest_base = cs.TriestBase(sample_size)
triest_impr = cs.TriestImpr(sample_size)

# Process the stream
for edge in edges:
    triest_base.process_edge(edge)
    triest_impr.process_edge(edge)

# Print results
print("TRIÈST-BASE Triangle Estimate:", triest_base.get_estimate())
print("TRIÈST-IMPR Triangle Estimate:", triest_impr.get_estimate())
