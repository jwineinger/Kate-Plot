import matplotlib, os.path
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig=plt.figure(1, figsize=(5,1), dpi=80)
ax=fig.add_axes((0,0,1,1))
ax.set_xlim(-3, 103)
ax.set_axis_off()
x = [0, 12, 13, 15, 50, 60, 80, 90, 95, 100]
ax.scatter(x, [1 for v in x], s=50, marker='d', zorder=1)
ax.axhline(1, xmin=.02, xmax=.98, zorder=0, color='k', solid_capstyle='butt')
#ax.plot([1,3,1,2,3])

plt.savefig(
    "/var/www/plotting/linear.png",
    dpi=80,
    bbox='tight',
    facecolor='m',
)
