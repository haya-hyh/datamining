def read_dataset(file_path):
    with open(file_path, 'r') as f:
        edges = []
        for line in f:
            if not line.startswith("#"):  # Skip comments
                parts = line.strip().split()
                if len(parts) == 2:
                    edges.append((int(parts[0]), int(parts[1])))
        return edges