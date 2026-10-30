import json, os
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

img = plt.imread("bundelkhand_ref.jpg")
extent = [77.69, 81.08, 23.44, 26.53]
OUT = "bundelkhand_lines.geojson"

data = json.load(open(OUT)) if os.path.exists(OUT) else {"type": "FeatureCollection", "features": []}

while True:
    kind = input("Type (dyke / reef, Enter = khatam): ").strip().lower()
    if not kind:
        break
    old = [f for f in data["features"] if f["properties"]["name"].lower().startswith(kind)]
    start = len(old) + 1
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(img, extent=extent)
    ax.set_title(f"{kind}: har line ke 2 click (shuru + ant), right = undo, Enter = done")
    pts = plt.ginput(n=-1, timeout=0)
    plt.close(fig)
    if len(pts) % 2 == 1:
        print("Akhri point akela tha, hata diya.")
        pts = pts[:-1]
    n = 0
    for i in range(0, len(pts), 2):
        name = f"{kind} {start + n}"
        data["features"].append({"type": "Feature", "properties": {"name": name},
            "geometry": {"type": "LineString", "coordinates": [list(pts[i]), list(pts[i+1])]}})
        n += 1
    json.dump(data, open(OUT, "w"))
    print(f">> {n} {kind} lines SAVED")

print("Total lines:", len(data["features"]))