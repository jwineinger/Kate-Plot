from decimal import Decimal
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

plt.subplot(2,1,1)

reader = csv.reader(open('chart_weights.txt'))
ages, weights = [], []
last_date = None
for line in reader:
    ages.append(32. + (2 + int(line[1])) / 7.)
    weights.append(int(line[2]))
    last_date = line[0]

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
    plt.plot(data.keys(), data.values())

plt.plot(ages, weights, 'mo-')
plt.ylabel("Weight (g)")
plt.xlabel("Week")
plt.axis([30,40,500,5000])
plt.grid(True)
plt.legend(('3%','10%','50%','90%','97%','Kate'), loc=2, fancybox=True, shadow=True, ncol=2)
plt.annotate(
    '%d g' % weights[-1],
    xy=(ages[-1], weights[-1]),
    xycoords='data',
    xytext=(20, -50),
    textcoords='offset points',
    arrowprops=dict(arrowstyle="->",
                    connectionstyle="angle,angleA=0,angleB=90,rad=10"),
)

# start the second plot
plt.subplot(2,1,2)
plt.ylabel("Weight Change (g)")
plt.axis([30,40,-30,130])
plt.grid(True)

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

fig = plt.gcf()
fig.set_size_inches(8,10)

path = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(path, "www/fenton.png"), dpi=100)
