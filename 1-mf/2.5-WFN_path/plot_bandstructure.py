import matplotlib.pyplot as plt
from matplotlib import rcParamsDefault
import numpy as np

plt.rcParams["figure.dpi"]=150
plt.rcParams["figure.facecolor"]="white"
plt.rcParams["figure.figsize"]=(8, 6)

# load data
data = np.loadtxt('bn_bands.dat.gnu')

k = np.unique(data[:, 0])
bands = np.reshape(data[:, 1], (-1, len(k)))

for band in range(8):
    plt.plot(k, bands[band, :], linewidth=1, alpha=0.5, color='k')
plt.xlim(min(k), max(k))

# Fermi energy
# plt.axhline(6.6416, linestyle=(0, (5, 5)), linewidth=0.75, color='k', alpha=0.5)
# # High symmetry k-points (check bands_pp.out)
plt.axvline(k[100], linewidth=0.75, color='k', alpha=0.5)
plt.axvline(k[200], linewidth=0.75, color='k', alpha=0.5)
plt.axvline(k[300], linewidth=0.75, color='k', alpha=0.5)
# # text labels
plt.xticks(ticks= [k[0], k[100], k[200], k[300], k[400]], labels=['$\Gamma$', 'M', 'K', '$\Gamma$', 'K'])
plt.ylabel("Energy (eV)")
# plt.text(2.3, 5.6, 'Fermi energy', fontsize= small)
plt.savefig("bandstructure.pdf")