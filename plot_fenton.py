from decimal import Decimal
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
path = os.path.dirname(os.path.abspath(__file__))

#reader = csv.reader(open('weights.txt'))
#dates, weights = [], []
#for line in reader:
    #dates.append(line[1])
    #weights.append(line[2])

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

for pcile, data in pciles.iteritems():
    plt.plot(data.keys(), data.values())
plt.ylabel("Weight (kg)")
plt.xlabel("Week")
plt.axis("tight")
plt.grid(True)
plt.savefig(os.path.join(path, "www/fenton.png"))
