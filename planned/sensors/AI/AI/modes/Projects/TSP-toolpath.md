from itertools import permutations

def tsp_path(coords):
    """Naive TSP path ordering for small prototypes."""
    indices = list(range(len(coords)))
    best_order = indices
    best_len = float("inf")

    for perm in permutations(indices):
        length = sum(math.dist((coords[perm[i]]["x"], coords[perm[i]]["y"]),
                               (coords[perm[i+1]]["x"], coords[perm[i+1]]["y"]))
                     for i in range(len(coords)-1))
        if length < best_len:
            best_len = length
            best_order = perm
    return [coords[i] for i in best_order]

if __name__ == "__main__":
    import json
    coords = json.load(open("phi_lattice_coords.json"))
    ordered = tsp_path(coords[:10])  # small sample for demo
    json.dump(ordered, open("phi_toolpath.json", "w"), indent=2)
    print("Saved phi_toolpath.json")
