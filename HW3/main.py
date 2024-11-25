import readfile as rf
import classtriez as cs
import time

# Load dataset
dataset_path = "web-Stanford.txt/web-Stanford.txt"
edges = rf.read_dataset(dataset_path)

# Parameters
sample_size = 4000
num_runs = 5  
true_triangle_num = 11329473  

# Initialize results lists
base_results = []
impr_results = []

# Run the experiments
start_time = time.time()
for run in range(num_runs):
    # Initialize algorithms for each run
    triest_base = cs.TriestBase(sample_size)
    triest_impr = cs.TriestImpr(sample_size)

    # Process the stream
    for edge in edges:
        triest_base.process_edge(edge)
        triest_impr.process_edge(edge)

    # Store results
    base_results.append(triest_base.estimate() / true_triangle_num)
    impr_results.append(triest_impr.estimate() / true_triangle_num)

end_time = time.time()

# Compute averages
base_avg = sum(base_results) / num_runs
impr_avg = sum(impr_results) / num_runs


print(f"\nTotal Time Taken: {(end_time - start_time)/num_runs:.2f} seconds")
# Output results
print("TRIÈST-BASE Results:")
print("  Individual Estimates:", base_results)
print("  Average Estimate:", base_avg)


print("TRIÈST-impr Results:")
print("  Individual Estimates:", impr_results)
print("  Average Estimate:", impr_avg)


