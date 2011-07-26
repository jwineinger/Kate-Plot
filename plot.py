from decimal import Decimal
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
path = os.path.dirname(os.path.abspath(__file__))

reader = csv.reader(open('weights.txt'))
ages, weights = [], []
last_date = None
for line in reader:
    ages.append(32. + (2 + int(line[1])) / 7.)
    weights.append(int(line[2]) / 1000.)
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
        pciles[pcile] = {week:val}
    pciles[pcile][week] = val

for pcile, data in sorted(pciles.iteritems()):
    plt.plot(data.keys(), data.values())

plt.plot(ages, weights, 'mo-')
plt.ylabel("Weight (kg)")
plt.xlabel("Week")
plt.axis([31,40,.5,4.0])
plt.grid(True)
plt.legend(('3%','10%','50%','90%','97%','Kate'))
plt.annotate(
    '%d g on %s' % (weights[-1] * 1000, last_date),
    xy=(ages[-1] + .1, weights[-1] - .05),
    xytext=(ages[-1] + .5, weights[-1] - .3),
    arrowprops=dict(facecolor='black', shrink=0),
)
plt.savefig(os.path.join(path, "www/fenton.png"))
