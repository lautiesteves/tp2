import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

"""# make data

x = np.linspace(0, 10, 100)
y = x
# plot:
fig, ax = plt.subplots()
ax.plot(x, y, linewidth=2.0)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.linspace(1, 8))

plt.show()"""

# make data
np.random.seed(1)
x = np.random.normal(0, 10, 100)

# plot:
fig, ax = plt.subplots()

ax.hist(x, bins=10, linewidth=1, edgecolor="black")

ax.set(xlim=(0, 100), xticks=np.arange(1, 100),
       ylim=(0, 50), yticks=np.linspace(0, 50, 50))

plt.show()