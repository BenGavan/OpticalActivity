from utils import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as ss
from scipy.stats import chisquare

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 19:22:42 2018

@author: iandu
"""
# Variation naming constants
CONCENTRATION = "concentration"
LENGTH = "length"
TEMPERATURE = "temp"

# Wavelength name constants
RED = "red"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"


def get_concentration_data():
    concentration_red = get_data_set(color=RED, variation=CONCENTRATION)
    concentration_yellow = get_data_set(color=YELLOW, variation=CONCENTRATION)
    concentration_green = get_data_set(color=GREEN, variation=CONCENTRATION)
    concentration_blue = get_data_set(color=BLUE, variation=CONCENTRATION)
    return concentration_red, concentration_yellow



def get_data_set(color, variation):
    return []




# Least squares fit for y = mx.
# Modified by MLloyd to run standalone from command line



# ML: put your own data values into arrays x, y and errs, or modify the script
# to read in data from your own text/csv file - see notes on Blackboard about this.


def Prob_Chi2_larger(Ndof, Chi2):
    """   Calculates the probability of getting a chi2 larger than observed
          for the given number of degrees of freedom,   Ndof .
          Uses incomplete gamma function,  defined as
                \frac{1}{\Gamma(a)} \int_0^x t^{a-1} e^{-t} dt        """
    p = ss.gammainc(Ndof / 2.0, Chi2 / 2.0)
    return (p)


def WLSFit_m_c(x, y, u):
    """Weighted Least Squares y = mx + c  """

    print('\n   Weighted Least Squares fit of x y u data points ')
    print('   to a straight line  y = m*x + c ')
    print('   with the slope,m, and  ')
    print('   the intercept,c, determined by Weighted Least Squares. ')

    """
    m = ( wxy - wx*wy    )/  Denom
    c = ( wy * wxx   - wxy * wx ) / Denom
     Denom = wxx - wx*wy
    """

    num = np.size(x)
    print('\nInput: Number of data points ', num)
    # while num <= 2:
    if num <= 1:
        print('Only one data points; Nothing to fit, Return')
        return (0.0, 0.0, 0.0, 0.0, 0.0)

    print('\n  Output \n')

    xa = np.array(x)
    ya = np.array(y)
    ua = np.array(u)
    wa = ua ** (-2)
    wbar = np.mean(wa)
    xwbar = np.mean(xa * wa) / wbar
    ywbar = np.mean(ya * wa) / wbar
    wxxbar = np.mean(wa * xa * xa) / wbar
    Denom = np.mean(wa * (x - xwbar) ** (2)) / wbar

    m = (np.mean(wa * (x - xwbar) * (y - ywbar)) / wbar) / Denom
    print(' Slope:  m  =   {0:8.5} '.format(m))

    u_m = np.sqrt(1 / (Denom * wbar * num))
    # print('Output: Uncertainty in slope, m, is   ',u_m)
    print(' Uncertainty in slope: u_m =  {0:8.5}'.format(u_m))
    # print(' Percentage uncertainty of slope is ',   100.0*u_m/m)
    print(' Percentage uncertainty of slope:   {0:8.5} %'.format(100.0 * u_m / m))
    print('')

    c = ywbar - m * xwbar
    # print('Output: Intercept, c, is  ', c )
    print(' Intercept:  c  =  {0:8.5}'.format(c))

    u_c = np.sqrt(wxxbar / (Denom * wbar * num))
    # print(' Uncertainty in intercept, c, is ', c)
    print(' Uncertainty of intercept:   u_c = {0:8.5}  '.format(u_c))
    print(' Percentage uncertainty of intercept:  {0:8.4g} %'.format(100.0 * (u_c / c)))
    print('')

    print(' Mean weighted x:  xwbar =  {0:8.5}'.format(xwbar))
    print(' Root mean weighted square x: x_rms = {0:8.5} '.format(np.sqrt(Denom)))
    print(' Mean weighted y:   ywbar = {0:8.5}'.format(ywbar))
    u_ywbar = np.sqrt(1 / (num * wbar))
    # print(' Uncertainty in ywbar:     ', u_ywbar )
    print(' Uncertainty in ywbar:   {0:8.5}'.format(u_ywbar))
    print(' Percentage uncertainty of ywbar:   {0:8.3} %'.format(100.0 * u_ywbar / ywbar))
    print('')

    resids = ya - (m * xa + c)
    chi2 = np.sum((resids * resids) * wa)
    Ndof = num - 2
    print(' chi2 = {0:8.4}'.format(chi2))
    print('         for ', Ndof, 'degrees of freedom')
    # print(' Reduced chi2 is ', chi2/Ndof)
    print(' Reduced chi2 is {0:8.3}'.format(chi2 / Ndof))

    prob = Prob_Chi2_larger(Ndof, chi2)
    print(' Probability of getting a chi2 larger(smaller)')
    print('     than {0:8.4}  is {1:8.3} ({2:6.3} ) '.format(chi2, 1.0 - prob, prob))

    if ((1.0 - prob) < 0.2):
        print(' Warning: Chi2 is large; consider uncertainties underestimated', \
              '\n       or data not consistent with assumed relationship.')

    if ((prob) < 0.2):
        print(' Warning: Chi2 is small; consider uncertainties overestimated', \
              '\n       or data selected or correlated.')

    print('\n Note: Uncertainties are calculated from the u, the uncertainties of the y-values. ')
    print('  and are independent of the value of chi2. ')

    print('\n    Summary of data')
    print('index  x-values    y-values    u-values     weights   residuals ')
    for i in range(0, num):
        print('{0:3}{1:12.3g}{2:12.3g}{3:12.3g}{4:12.3g}{5:12.3g}'. \
              format(i, x[i], y[i], u[i], wa[i], resids[i]))

    """  Plots:  y vs x with uncertainty bars and
             residuals vs x 
             x-range extended by 10%    """

    extra_x = 0.1 * (x[num - 1] - x[0])
    xl = x[0] - extra_x
    xh = x[num - 1] + extra_x
    yl = m * xl + c
    yh = m * xh + c

    plt.subplot(2, 1, 1)
    plt.errorbar(xa, ya, ua, fmt='ro')  # plot the data points
    plt.plot([xl, xh], [yl, yh])  # plot the fitted line
    plt.subplot(2, 1, 2)
    plt.errorbar(xa, resids, ua, fmt='ro')  # plot the unceertainty bars
    plt.plot([xl, xh], [0.0, 0.0])  # plot the line y = 0.0
    plt.show()

    return (m, u_m, c, u_c, chi2)


# solve for a and b
def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b


def get_data():

########  Get Red raw data ########
    f = open("raw_data/red-0.1-raw.txt", "r")

    first_col = np.array([])
    second_col = np.array([])
    y_err_col = np.array([])
    x_err_col = np.array([])

    for x in f:
        first = float(x.split('\t')[0])
        second = float(x.split('\t')[1])

        first = first - 180 + 0.5
        second = second - 180 + 0.5

        first_col = np.append(first_col, first)
        second_col = np.append(second_col, second)
        y_err_col = np.append(y_err_col, .5)
        x_err_col = np.append(x_err_col, 0.5)

        print(first, second)

    f.close()

    x_red = first_col
    y_red = second_col
    y_errs_red = y_err_col
    x_errs_red = x_err_col

########  Get Yellow raw data ########
    f = open("raw_data/yellow-0.1-raw.txt", "r")

    first_col = np.array([])
    second_col = np.array([])
    y_err_col = np.array([])
    x_err_col = np.array([])

    for x in f:
        first = float(x.split('\t')[0])
        second = float(x.split('\t')[1])

        first = first - 180 + 0.5
        second = second - 180 + 0.5

        first_col = np.append(first_col, first)
        second_col = np.append(second_col, second)
        y_err_col = np.append(y_err_col, .5)
        x_err_col = np.append(x_err_col, 0.5)

        print(first, second)

    f.close()

    x_yellow = first_col
    y_yellow = second_col
    y_errs_yellow = y_err_col
    x_errs_yellow = x_err_col

########  Get Green raw data ########
    f = open("raw_data/green-0.1-raw.txt", "r")

    first_col = np.array([])
    second_col = np.array([])
    err_col = np.array([])
    x_err_col = np.array([])

    for x in f:
        first = float(x.split('\t')[0])
        second = float(x.split('\t')[1])

        first = first - 180 + 0.5
        second = second - 180 + 0.5

        first_col = np.append(first_col, first)
        second_col = np.append(second_col, second)
        err_col = np.append(err_col, 1.5)
        x_err_col = np.append(x_err_col, 0.5)

        print(first, second)

    f.close()

    x_green = first_col
    y_green = second_col
    y_errs_green = err_col
    x_errs_green = x_err_col

########  Get Blue raw data ########
    f = open("raw_data/blue-0.1-raw.txt", "r")

    first_col = np.array([])
    second_col = np.array([])
    err_col = np.array([])
    x_err_col = np.array([])

    for x in f:
        first = float(x.split('\t')[0])
        second = float(x.split('\t')[1])

        first = first - 180 + 0.5
        second = second - 180 + 0.5

        first_col = np.append(first_col, first)
        second_col = np.append(second_col, second)
        err_col = np.append(err_col, 2.)
        x_err_col = np.append(x_err_col, 0.5)

        print(first, second)

    f.close()

    x_blue = first_col
    y_blue = second_col
    y_errs_blue = err_col
    x_errs_blue = x_err_col

########################################################

    # WLSFit_m_c(x_blue, y_blue, errs_blue)

    ###### Red plotting #####
    plt.errorbar(x_red, y_red, y_errs_red, x_errs_red, fmt='ro')
    # plt.plot(first_col, second_col, 'bo')

    a_red, b = best_fit(x_red, y_red)
    yfit_red = [a_red + b * xi for xi in x_red]
    plt.plot(x_red, yfit_red, "r")

    ###### Yellow plotting #####
    plt.errorbar(x_yellow, y_yellow, err_col, fmt='yo')
    # plt.plot(first_col, second_col, 'bo')

    a, b = best_fit(x_yellow, y_yellow)
    yfit_yellow = [a + b * xi for xi in x_yellow]
    plt.plot(x_yellow, yfit_yellow, "y")

    ###### Green plotting #####
    plt.errorbar(x_green, y_green, y_errs_green, x_errs_green, fmt='go')

    a, b = best_fit(x_green, y_green)
    yfit_green = [a + b * xi for xi in x_green]
    plt.plot(x_green, yfit_green, "g")

    ###### Blue plotting #####
    plt.errorbar(x_blue, y_blue, y_errs_blue, x_errs_blue, fmt='bo')

    a, b = best_fit(x_blue, y_blue)
    yfit_blue = [a + b * xi for xi in x_blue]
    plt.plot(x_blue, yfit_blue, "b")

    #########################

    plt.title("Varying wavelength - concentration of 0.1g/ml")
    plt.xlabel('distance traversed / ml')
    plt.ylabel('polarization angle / deg')

    plt.legend(["Red - ", "Yellow - 580nm", "Green - 525nm", "Blue - 468nm"])

    plt.show()

    chi_squared = chisquare(y_blue)
    print("chi-squared = ", chi_squared)


def chi2():
    pass


get_data()








