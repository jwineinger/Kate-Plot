import numpy
import matplotlib, os.path, csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 2.1 = x
x=numpy.array([83.3,100,100,83.3,66.7,100,66.7,66.7,83.3,66.7,66.7,66.7,83.3,66.7,33.3,66.7,66.7,0,83.3,33.3,50,66.7,16.7,33.3,66.7,50,33.3,83.3,66.7,50,33.3,100,100,66.7,16.7,66.7,])
# 2 = y
y=numpy.array([81.3,85.4,100,72.5,68.8,85.4,68.3,75,66.7,56.3,35.8,91.7,60,50.8,50.4,58.3,47.9,4.2,60,43.3,57.5,62.5,12.5,52.1,79.2,59.6,72.9,81.3,70.8,83.3,15.8,100,100,81.3,21.7,35.8])

print numpy.corrcoef(x,y)

A = numpy.vstack([x, numpy.ones(len(x))]).T
slope, intercept = numpy.linalg.lstsq(A,y)[0]
print "y = %.3fx + %.3f" % (slope, intercept)

plt.plot(x,y,'o', label='Original data', markersize=10)
plt.plot(x, slope*x + intercept, 'r', label='Fitted line')
plt.legend()
from os.path import dirname, abspath, join
path = dirname(abspath(__file__))
plt.savefig(
    join(path, "www/correlation.png"),
    dpi=100,
)
