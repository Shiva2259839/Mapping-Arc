import os
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

img = plt.imread("aravalli_ref.jpg")
extent = [71.45, 78.49, 22.67, 28.59]

# Jaanch ke liye shehar: ye map ke shehron par baithne chahiye
cities = {"Udaipur": (73.71, 24.58), "Ajmer": (74.64, 26.45),
          "Jaipur": (75.79, 26.91), "Chittorgarh": (74.63, 24.88)}

out_path = os.path.abspath("aravalli_units.geojson")
if os.path.exists(out_path):
    with open(out_path) as fp:
        features = json.load(fp)["features"]
    print(">> Purani file mili, units: " + ", ".join(f["properties"]["name"] for f in features))
else:
    features = []

while True:
    name = input("Unit ka naam likho (khatam karne ke liye bas Enter): ").strip()
    if not name:
        break

    fig, ax = plt.subplots(figsize=(11, 11))
    ax.imshow(img, extent=extent)
    for c, (x, y) in cities.items():
        ax.plot(x, y, "b+", markersize=14, markeredgewidth=2)
    for f in features:
        if f["properties"]["name"] == name:
            continue
        xs, ys = zip(*f["geometry"]["coordinates"][0])
        ax.plot(xs, ys, color="blue", linewidth=1)
    ax.set_title(name + ": left click = point, right click = undo, Enter = done")
    pts = plt.ginput(n=-1, timeout=0)
    plt.close()

    if len(pts) < 3:
        print(">> Kam se kam 3 point chahiye, kuch nahi badla.")
        continue

    pts.append(pts[0])
    features = [f for f in features if f["properties"]["name"] != name]
    features.append({
        "type": "Feature",
        "properties": {"name": name},
        "geometry": {"type": "Polygon", "coordinates": [[list(p) for p in pts]]},
    })
    with open(out_path, "w") as fp:
        json.dump({"type": "FeatureCollection", "features": features}, fp)
    print(">> " + name + " SAVED (" + str(len(pts)) + " points)")

print("Sab ho gaya! Total units: " + str(len(features)))
print("File yahan hai: " + out_path)