from utils import *
from analysis import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


temperatures = Column([Measurement(20, 0.5), Measurement(30, 1), Measurement(50, 1), Measurement(60, 2), Measurement(70, 2), Measurement(90, 3)])
polarization = Column([Measurement(216, 1), Measurement(211, 1), Measurement(208, 1), Measurement(205, 1), Measurement(200, 1), Measurement(200, 1)])



color = RED
sugar = FRUCTOSE


polarization = Column([Measurement(180, 0)] * len(polarization.values)) - polarization

x_vals = temperatures.get_just_values()
x_unerts = temperatures.get_just_uncertainties()

y_vals = polarization.get_just_values()
y_errs = polarization.get_just_uncertainties()

chi2, reduced_chi2 = calculate_chi2(x_vals, y_vals, y_errs)

a, b = best_linear_fit(temperatures, polarization)
y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
m = b
c = a

residuals_x, residual_values = residuals(m, c, temperatures, polarization)

    ##### Plotting ######
plt.figure(figsize=(10, 9))
gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])

plt.subplot(gs[0])

sugar_string = sugar
if sugar == GLUCOSE:
    sugar_string = "Sucrose"

plt.title("Varying Temperature - {} - {}".format(color, sugar_string))
plt.xlabel('Temperature - K')
plt.ylabel('polarization angle / deg')
plt.errorbar(x_vals, y_vals, xerr=x_unerts, yerr=y_errs, fmt='kx')
plt.plot(x_vals, y_best_fit_vals, 'k')

plt.subplot(gs[1])
plt.title('Residuals in Polarization Angle')
plt.errorbar(residuals_x.get_just_values(), residual_values.get_just_values(), yerr=y_errs, fmt='kx')
plt.plot([x_vals[0], x_vals[len(x_vals) - 1]], [0, 0])

plt.annotate('chi2 = {:.4f},'.format(chi2), (0, 0), (0, -40),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')
plt.annotate('reduced chi2 = {:.4f}'.format(reduced_chi2), (0, 0), (250, -40),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')
plt.annotate('y = ({:.2f} ± {:.2f})x + ({:.2f} ± {:.2f}),'.format(b.value, b.uncertainty, a.value, a.uncertainty), (0, 0), (0, -60),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')

plt.tight_layout()

plt.show()
print("-------------------------------------------------")

if __name__ == "__main__":
    pass