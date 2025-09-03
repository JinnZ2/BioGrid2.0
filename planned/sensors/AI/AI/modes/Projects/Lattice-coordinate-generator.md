import math
import json

def phi_lattice(num_points=200, radius=50.0, h=2.0, layers=4):
    """Generates (x,y,z) coords for a stacked phi-lattice."""
    phi_angle = math.radians(137.50776405003785)  # golden angle in radians
    coords = []
    
    for layer in range(layers):
        for k in range(num_points):
            r = math.sqrt(k / float(num_points)) * radius
            theta = k * phi_angle
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = layer * h
            coords.append({
                "layer": layer,
                "index": k,
                "x": round(x, 4),
                "y": round(y, 4),
                "z": round(z, 4)
            })
    return coords

if __name__ == "__main__":
    coords = phi_lattice(num_points=120, radius=25.0, h=1.5, layers=4)
    with open("phi_lattice_coords.json", "w") as f:
        json.dump(coords, f, indent=2)
    print("Saved phi_lattice_coords.json with", len(coords), "points.")
