#https://en.wikipedia.org/wiki/TracyâWidom_distribution
import skrmt #scikit-rmt: random matrix theory. must enable local packages to use, by executing site.main()
from skrmt.ensemble import TracyWidomDistribution as TWD

figure()
TWD().plot_cdf()
