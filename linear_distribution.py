import matplotlib, os.path
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig = plt.figure(1)
ax=fig.add_axes((0,0,1000,1))
ax.set_axis_off()

plt.axhline(1, color='k', zorder=0)
x = [x * .1 for x in range(1000)]
plt.scatter(x, [1 for v in x], marker='d', s=50, zorder=1)
plt.axis([0,1000,0,2])

fig = plt.gcf()
fig.set_size_inches(5,1)

plt.savefig(
    "/var/www/plotting/linear.png",
    dpi=80,
    bbox='tight',
    facecolor='m',
)
