import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#mean value for gaussian is eta mass
mean = .547
#func is a sum of const + gaussian
def func(x, a, b, c, d):
    return a + b*np.exp(-(x - d) ** 2 / (2 * c ** 2))

datapoints = []

f = open("metaVals.txt", "r")
for l in f:
    val = float(l.strip())
    datapoints.append(val)

print("datapoints:")
print(datapoints)

nbins = 20
locut = .4
hicut = .7
#make a histogram with 15 bins
#h = plt.hist(datapoints, nbins, histtype='step')
hist, bin_edges = np.histogram(datapoints, nbins, range=(locut,hicut))
print("bin_edges: " + str(bin_edges))
centers = []
for i in range(len(bin_edges)-1):
    cent = bin_edges[i] + (bin_edges[i+1] - bin_edges[i]) / 2
    centers.append(cent)

print("centers: " + str(centers))
xerrs = [(hicut-locut)/nbins/2 for j in range(len(centers))] 
yerrs = [np.sqrt(j) if j > 0 else 1.2 for j in hist] 
print("hist: " + str(hist))

plt.errorbar(centers, hist, yerrs, xerrs, 's')
popt, pcov = curve_fit(func, centers, hist, bounds=([0, 0, 0, 0], [10, 10, 10, 10]))

print("fit results: (const, gaussNorm, sigma, mean)")
print(popt)
print(pcov)
x = np.array([float(i) for i in np.arange (locut, hicut, .0001)])
y = y = func(x, popt[0], popt[1], popt[2], popt[3])
plt.plot(x, y, linewidth=3)
plt.xlabel("4-lepton invariant mass (GeV)")
plt.ylabel("Events / .015 GeV")
plt.title("mu mu e e")
bottom, top = plt.ylim()  # return the current ylim
plt.ylim((0., top))
#plt.plot(h)
plt.show()
