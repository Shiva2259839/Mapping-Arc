import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

img = plt.imread("aravalli_ref.jpg")
extent = [70.73, 78.92, 22.59, 28.90]

fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(img, extent=extent)
ax.set_title("Kram se click: Ajmer, Jaipur, Udaipur, Chittorgarh ke kaale bindu. Phir Enter.")
pts = plt.ginput(n=4, timeout=0)
plt.close()

true = {"Ajmer": 26.45, "Jaipur": 26.91, "Udaipur": 24.58, "Chittorgarh": 24.88}
diffs = []
for (name, lat), (x, y) in zip(true.items(), pts):
    print(name, "map par y =", round(y, 2), " asli =", lat, " farq =", round(y - lat, 2))
    diffs.append(y - lat)
d = sum(diffs) / len(diffs)
print("Naya extent = [70.73, 78.92, %.2f, %.2f]" % (22.59 - d, 28.90 - d))