import numpy as np

def coupling_matrix(coords, m=1e-9):
    """Compute dipole coupling |B| in Tesla for all pairs."""
    mu0 = 4*math.pi*1e-7
    N = len(coords)
    C = np.zeros((N, N))
    
    for i in range(N):
        for j in range(N):
            if i == j: 
                continue
            dx = coords[i]["x"] - coords[j]["x"]
            dy = coords[i]["y"] - coords[j]["y"]
            dz = coords[i]["z"] - coords[j]["z"]
            r = math.sqrt(dx*dx + dy*dy + dz*dz) * 1e-3  # mm → m
            C[i, j] = mu0 / (4*math.pi) * (2*m / (r**3))
    return C

def write_margin(coupling, Hc=0.2):
    """Estimate safe write field margin given coercivity Hc (Tesla)."""
    worst_neighbor_field = np.max(coupling)
    return Hc / worst_neighbor_field if worst_neighbor_field else float('inf')

if __name__ == "__main__":
    import json
    coords = json.load(open("phi_lattice_coords.json"))
    C = coupling_matrix(coords)
    margin = write_margin(C, Hc=0.2)  # example coercivity
    print("Safe write margin factor:", margin)
