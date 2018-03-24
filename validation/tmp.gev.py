import numpy as np
from matplotlib import pyplot as plt

from scipy.stats import gumbel_r
from scipy.stats import gumbel_l
from scipy.stats import genextreme

dataN = np.loadtxt("../data/Qdaily.txt")

x_pdf = np.linspace(np.min(dataN),np.max(dataN),num=100)
param = gumbel_r.fit(dataN)
cdf1   = gumbel_r.cdf(x_pdf, *param[:-2], loc=param[-2], scale=param[-1])
plt.plot(x_pdf, -np.log(-np.log(cdf1)), 'o')

print(param)

num_bins = 200
counts, bin_edges = np.histogram(dataN, bins=num_bins)
cdf2 = np.cumsum(counts)/np.sum(counts)
plt.plot(bin_edges[1:], -np.log(-np.log(cdf2)),'x')

plt.show()
