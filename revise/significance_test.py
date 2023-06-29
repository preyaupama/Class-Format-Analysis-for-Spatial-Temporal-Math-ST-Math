import pandas
import csv
from statistics import mean,variance
from math import sqrt
from scipy import stats

lab = pandas.read_csv("lab.csv")
free = pandas.read_csv("free.csv")
rotation = pandas.read_csv("rotation.csv")

def cohend(d1, d2):
    # calculate the size of samples
	n1, n2 = len(d1), len(d2)
	# calculate the variance of the samples
	s1, s2 = variance(d1), variance(d2)
	# calculate the pooled standard deviation
	s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	# calculate the means of the samples
	u1, u2 = mean(d1), mean(d2)
	# calculate the effect size
	return (u1 - u2) / s
print(stats.normaltest(lab['performance']))
print(stats.normaltest(free['performance']))
print(stats.normaltest(rotation['performance']))
print(cohend(lab['performance'],free['performance']))
print(cohend(lab['performance'],rotation['performance']))
print(cohend(free['performance'],rotation['performance']))
print(stats.mannwhitneyu(lab['performance'],free['performance']))
print(stats.mannwhitneyu(lab['performance'],rotation['performance']))
print(stats.mannwhitneyu(free['performance'],rotation['performance']))