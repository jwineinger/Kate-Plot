from decimal import Decimal
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class BabyPlotter(object):
    def __init__(self, name, kate, fenton, imgdir='www', size=(8,14), dpi=100):
        self.baby = name
        self.setup_baby_info(kate)
        self.setup_fenton_curves(fenton)
        self.image_dir = imgdir

        fig = plt.gcf()
        fig.set_size_inches(*size)
        self.dpi = dpi

    def select_baby_plot(self):
        # start first plot
        plt.subplot(3,1,1)

    def select_daily_change_plot(self):
        # start the second plot
        plt.subplot(3,1,2)

    def select_difference_plot(self):
        # start the third plot
        plt.subplot(3,1,3)

    def setup_baby_plot(self):
        # setup labels, data range, grid, and legend on top plot
        plt.ylabel("Weight (g)")
        plt.xlabel("Week")
        plt.axis([32,40,1000,4000])
        plt.grid(True)
        plt.legend(loc=2, fancybox=True, shadow=True, ncol=2)

        # customize legend
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()  # all the text.Text instance in the legend
        llines = leg.get_lines()  # all the lines.Line2D instance in the legend
        plt.setp(ltext, fontsize='small')    # the legend text fontsize
        plt.setp(llines, linewidth=1.5)      # the legend linewidth

    def setup_daily_changes_plot(self):
        # setup labels, data range, grid, on bottom plot
        plt.ylabel("Weight Change (g)")
        plt.axis([32,40,-30,130])
        plt.grid(True)

    def setup_difference_plot(self):
        # setup labels, data range, grid, on bottom plot
        plt.ylabel("Difference from Fenton (g)")
        plt.axis([32,40,0,1000])
        plt.grid(True)
        plt.legend(loc=2, fancybox=True, shadow=True, ncol=2)

    def setup_baby_info(self, data):
        """
        Reads the baby's weight from the given open file. The file should be
        formatted as CSV data with the following format:
            date,age(days),weight(g) -- 2011-07-05,3,1275
            
        Sets up instance variables for the baby's ages, weights, and first and
        last dates in the file.
        """
        reader = csv.reader(data)
        ages, weights = [], []
        first_date, last_date = None, None
        for line in reader:
            ages.append(32. + (2 + int(line[1])) / 7.)
            weights.append(int(line[2]))
            if first_date is None:
                first_date = line[0]
            last_date = line[0]
        self.ages = ages
        self.weights = weights
        self.dates = (first_date, last_date)

    def setup_fenton_curves(self, data):
        """
        Reads the fenton curve data for preemature infant weight from a CSV file.
        The file includes the percentile curve, gestational age, and infant
        weight in kg.

        This function calculates a cubic iterpolation for each percentile curve
        so that we can evaluate the baby's weight against each curve at any
        point, even though we only start with a data point at each week of
        gestation.
        """
        from scipy.interpolate import interp1d

        pciles = {}
        reader = csv.reader(data)
        for line in reader:
            pcile = int(line[1])
            week = int(line[0])
            val = Decimal(line[2]) * 1000 # convert kg to grams

            if pcile not in pciles:
                pciles[pcile] = {week: val}
            pciles[pcile][week] = val

        self.fentons = {}
        for pcile, data in pciles.iteritems():
            # calculate the interpolated function
            self.fentons[pcile] = interp1d(data.keys(), data.values(), kind='cubic')

    def plot_fenton_curves(self):
        """
        Graphs the entire fenton curves (22 weeks to 50 weeks) for each
        percentile.
        """
        from numpy import linspace
        # generate x-values from 22 weeks to 50 weeks, one point per day
        x = linspace(22, 50, (50 - 22) * 7)
        # process in increasing order of percentiles so the legend is ordered logically
        for pcile, fenton_fn in sorted(self.fentons.iteritems()):
            # plot the data
            plt.plot(x, fenton_fn(x), label='%d%%' % pcile)

    def plot_baby(self):
        """
        Plots the baby's weight and annotates the last point with the actual
        weight value.

        Also annotates the data point where she switched from Prolacta to
        Similac.
        """
        plt.plot(self.ages, self.weights, 'm.-', label=self.baby)

        plt.annotate(
            '%d g' % self.weights[-1],
            xy=(self.ages[-1], self.weights[-1]),
            xycoords='data',
            xytext=(-50, -30),
            textcoords='offset points',
            size=8,
            bbox=dict(boxstyle="round", fc="0.8"),
            arrowprops=dict(arrowstyle="wedge,tail_width=0.7",
                            fc="0.6", ec="none",
                            connectionstyle="arc3,rad=0.3"),
        )

        plt.annotate(
            'Start Similac',
            xy=(self.ages[33], self.weights[33]),
            xycoords='data',
            xytext=(-80, 15),
            textcoords='offset points',
            size=8,
            bbox=dict(boxstyle="round", fc="0.8"),
            arrowprops=dict(arrowstyle="wedge,tail_width=0.7",
                            fc="0.6", ec="none",
                            connectionstyle="arc3,rad=-0.3"),
        )

    def plot_future_averages(self):#plt, ages, weights):
        """
        Plots some extrapolated data from baby's recent average weight changes.
        """
        from numpy import linspace, array
        # generate x-values from baby's last data point to 50 weeks gestation,
        # one point per day
        extrap_range = linspace(self.ages[-1], 50, (50 - self.ages[-1]) * 7)

        def get_ys(avg):
            return array([self.weights[-1] + avg * i for i in range(len(extrap_range))])

        avg_3 = (self.weights[-1] - self.weights[-3]) / 3.
        avg_7 = (self.weights[-1] - self.weights[-7]) / 7.
        avg_14 = (self.weights[-1] - self.weights[-14]) / 14.
        avg_28 = (self.weights[-1] - self.weights[-28]) / 28.
        
        plt.plot(extrap_range, get_ys(avg_3), 'k--', label='3-day avg gain')
        plt.plot(extrap_range, get_ys(avg_7), 'r--', label='7-day avg gain')
        plt.plot(extrap_range, get_ys(avg_14), 'g--', label='14-day avg gain')
        plt.plot(extrap_range, get_ys(avg_28), 'm--', label='28-day avg gain')

    def plot_daily_changes(self):#plt, ages, weights):
        """
        Plots a bar chart of baby's daily weight changes.
        """
        weight_changes, bar_colors = [], []
        i = 0
        # calculate daily weight changes and set colors for positive/negative
        while i <= (len(self.weights) - 2):
            weight_changes.append(self.weights[i+1] - self.weights[i])
            if weight_changes[-1] > 0:
                # positive days are blue
                bar_colors.append('b')
            else:
                # negative days are red
                bar_colors.append('r')
            i += 1

        # since we're calculating daily changes, omit the first day from the
        # x-values. 'align=center' centers the bars over the daily points
        # instead of aligning the edge of the bars with the points
        plt.bar(self.ages[1:], weight_changes, width=1/7., color=bar_colors, align='center')

    def plot_fenton_difference(self):#plt, ages, weights, fenton_fns):
        """
        Plots baby's difference from each of the fenton percentile curves. Uses
        the interpolated fenton curves to evaluate at each day.
        """
        for pcile, fn in sorted(self.fentons.iteritems()):
            pcile_ys = [fn(age) - self.weights[i] for i,age in enumerate(self.ages)]
            plt.plot(self.ages, pcile_ys, label='%d%%' % pcile)

    def save(self):
        from os.path import dirname, abspath, join
        path = dirname(abspath(__file__))
        plt.savefig(
            join(
                path,
                "%s/%s.png" % (self.image_dir, self.dates[1])
            ),
            dpi=self.dpi,
            bbox_inches='tight',
        )

kate = open("chart_weights.txt")
fenton = open("fenton.csv")

bp = BabyPlotter('Kate', kate, fenton)

bp.select_baby_plot()
bp.plot_fenton_curves()
bp.plot_baby()
bp.plot_future_averages()
bp.setup_baby_plot()

bp.select_daily_change_plot()
bp.plot_daily_changes()
bp.setup_daily_changes_plot()

bp.select_difference_plot()
bp.plot_fenton_difference()
bp.setup_difference_plot()

bp.save()
