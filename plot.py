from decimal import Decimal
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def plot_fenton_curves(plt):
    pciles = {}
    weeks = []
    vals = []
    reader = csv.reader(open('fenton.csv'))
    for line in reader:
        pcile = int(line[1])
        week = int(line[0])
        val = Decimal(line[2])
        if pcile not in pciles:
            pciles[pcile] = {week: val * 1000}
        pciles[pcile][week] = val * 1000

    for pcile, data in sorted(pciles.iteritems()):
        plt.plot(data.keys(), data.values(), label='%d%%' % pcile)

def plot_kate(plt):
    reader = csv.reader(open('chart_weights.txt'))
    ages, weights = [], []
    last_date = None
    for line in reader:
        ages.append(32. + (2 + int(line[1])) / 7.)
        weights.append(int(line[2]))
        last_date = line[0]

    plt.plot(ages, weights, 'm.-', label='Kate')

    plt.annotate(
        '%d g' % weights[-1],
        xy=(ages[-1], weights[-1]),
        xycoords='data',
        xytext=(-50, -30),
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="angle,angleA=0,angleB=90,rad=10"),
    )
    return (ages, weights)

def plot_future_averages(plt, ages, weights):
    """
    Plots some extrapolated data from Kate's recent average weight chanegs.
    """
    from numpy import linspace, array
    extrap_range = linspace(ages[-1], 50, (50 - ages[-1]) * 7)

    def get_ys(avg):
        y = []
        for i, v in enumerate(extrap_range):
            y.append(weights[-1] + avg * i)
        return array(y)

    avg_1 = (weights[-1] - weights[-2]) / 1.
    avg_2 = (weights[-1] - weights[-3]) / 2.
    avg_3 = (weights[-1] - weights[-3]) / 3.
    avg_7 = (weights[-1] - weights[-7]) / 7.
    avg_14 = (weights[-1] - weights[-14]) / 14.
    avg_28 = (weights[-1] - weights[-28]) / 28.
    
    plt.plot(extrap_range, get_ys(avg_1), 'b--', label='1-day gain')
    plt.plot(extrap_range, get_ys(avg_2), 'c--', label='2-day avg gain')
    plt.plot(extrap_range, get_ys(avg_3), 'k--', label='3-day avg gain')
    plt.plot(extrap_range, get_ys(avg_7), 'r--', label='7-day avg gain')
    plt.plot(extrap_range, get_ys(avg_14), 'g--', label='14-day avg gain')
    plt.plot(extrap_range, get_ys(avg_28), 'm--', label='28-day avg gain')

def plot_daily_changes(plt, ages, weights):
    weight_changes, bar_colors = [], []
    i = 0
    # calculate daily weight changes and set colors for positive/negative
    while i <= (len(weights) - 2):
        weight_changes.append(weights[i+1] - weights[i])
        if weight_changes[-1] > 0:
            bar_colors.append('b')
        else:
            bar_colors.append('r')
        i += 1
    plt.bar(ages[1:], weight_changes, width=1/7., color=bar_colors, align='center')

# start first plot
plt.subplot(2,1,1)

plot_fenton_curves(plt)
ages, weights = plot_kate(plt)
plot_future_averages(plt, ages, weights)

# setup labels, data range, grid, and legend on top plot
plt.ylabel("Weight (g)")
plt.xlabel("Week")
plt.axis([32,40,1000,4000])
plt.grid(True)
#plt.legend(('3%','10%','50%','90%','97%','Kate'), loc=2, fancybox=True, shadow=True, ncol=2)
plt.legend(loc=2, fancybox=True, shadow=True, ncol=2)


# get legend for customization
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
llines = leg.get_lines()  # all the lines.Line2D instance in the legend

# see text.Text, lines.Line2D, and patches.Rectangle for more info on
# the settable properties of lines, text, and rectangles
plt.setp(ltext, fontsize='small')    # the legend text fontsize
plt.setp(llines, linewidth=1.5)      # the legend linewidth


# start the second plot
plt.subplot(2,1,2)

# setup labels, data range, grid, on bottom plot
plt.ylabel("Weight Change (g)")
plt.axis([32,37,-30,130])
plt.grid(True)

plot_daily_changes(plt, ages, weights)

# set the output figure size (8x10)
fig = plt.gcf()
fig.set_size_inches(8,10)

path = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(path, "www/fenton.png"), dpi=100)
