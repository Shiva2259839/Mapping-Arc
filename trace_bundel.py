import json, os
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

img = plt.imread("bundelkhand_ref.jpg")
extent = [77.69, 81.08, 23.44, 26.53]   # ye numbers nahi badalne
OUT = "bundelkhand_units.geojson"

# jaanch ke liye shahar (neele cross)
towns = {"Jhansi": (78.57, 25.45), "Mahoba": (79.87, 25.29),
         "Lalitpur": (78.42, 24.69), "Khajuraho": (79.93, 24.85)}

data = {"type": "FeatureCollection", "features": []}
if os.path.exists(OUT):
    data = json.load(open(OUT))
    print("Purani file mili, units:", [f["properties"]["name"] for f in data["features"]])

while True:
    name = input("Unit name (Enter = khatam): ").strip()
    if not name:
        break
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(img, extent=extent)
    for t, (x, y) in towns.items():
        ax.plot(x, y, "b+", markersize=14, mew=2)
    ax.set_title(f"{name}: left click = point, right = undo, Enter = done")
    pts = plt.ginput(n=-1, timeout=0)
    plt.close(fig)
    if len(pts) < 3:
        print("Kam se kam 3 points chahiye, skip.")
        continue
    ring = [list(p) for p in pts] + [list(pts[0])]
    data["features"] = [f for f in data["features"] if f["properties"]["name"] != name]
    data["features"].append({"type": "Feature", "properties": {"name": name},
        "geometry": {"type": "Polygon", "coordinates": [ring]}})
    json.dump(data, open(OUT, "w"))
    print(f">> {name} SAVED ({len(pts)} points)")

print("Total units:", len(data["features"]))
print("File:", os.path.abspath(OUT))