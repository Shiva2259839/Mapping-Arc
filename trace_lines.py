import json, os
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

img = plt.imread("bundelkhand_ref.jpg")
extent = [77.69, 81.08, 23.44, 26.53]
OUT = "bundelkhand_lines.geojson"

data = {"type": "FeatureCollection", "features": []}
if os.path.exists(OUT):
    data = json.load(open(OUT))

while True:
    name = input("Line name (Enter = khatam): ").strip()
    if not name:
        break
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(img, extent=extent)
    ax.set_title(f"{name}: left click = point, right = undo, Enter = done")
    pts = plt.ginput(n=-1, timeout=0)
    plt.close(fig)
    if len(pts) < 2:
        print("Kam se kam 2 points chahiye, skip.")
        continue
    data["features"] = [f for f in data["features"] if f["properties"]["name"] != name]
    data["features"].append({"type": "Feature", "properties": {"name": name},
        "geometry": {"type": "LineString", "coordinates": [list(p) for p in pts]}})
    json.dump(data, open(OUT, "w"))
    print(f">> {name} SAVED ({len(pts)} points)")

print("File:", os.path.abspath(OUT))