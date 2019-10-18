from utils import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


zero_error = -0.5


# Variation naming constants
CONCENTRATION = "concentration"
LENGTH = "length"
TEMPERATURE = "temp"
variations = [CONCENTRATION, LENGTH, TEMPERATURE]

# Wavelength name constants
RED = "red"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
colors = [RED, YELLOW, GREEN, BLUE]

# Sugars Constants
GLUCOSE = "glucose"
FRUCTOSE = "fructose"
sugars = [GLUCOSE, FRUCTOSE]

# Wavelengths
RED_WAVELENGTH = 630
YELLOW_WAVELENGTH = 580
GREEN_WAVELENGTH = 525
BLUE_WAVELENGTH = 468
color_wavelengths = [BLUE_WAVELENGTH, YELLOW_WAVELENGTH, GREEN_WAVELENGTH, BLUE_WAVELENGTH]


def get_concentration_data(color, sugar):
    header, values = get_data_set(color, CONCENTRATION, sugar)

    concentration_column = generate_concentrations()
    # flip = Column([Measurement(-1, 0)] * len(concentration_column))
    # print(flip.to_string(), type(concentration_column))
    # concentration_column = concentration_column * flip
    bg_column = Column([])
    kj_column = Column([])

    row_counter = 0

    for row in values:
        # concentration = Measurement(row[0], concentration_uncert)
        bg = Measurement(row[1], row[2])
        kj = Measurement(row[3], row[4])
        # concentration_column.append(concentration)
        bg_column.append(bg)
        kj_column.append(kj)

        row_counter += 1

    return concentration_column, bg_column, kj_column


def get_length_data(color, sugar):
    header, values = get_data_set(color, LENGTH, sugar)

    length_column = Column([])
    bg_column = Column([])
    kj_column = Column([])

    for row in values:
        length = Measurement(row[0], 0.5)
        length = (Measurement(15.4, 0.5) / Measurement(90, 0.5)) * length * Measurement(0.1, 0)
        bg = Measurement(row[1], row[2])
        kj = Measurement(row[3], row[4])
        length_column.append(length)
        bg_column.append(bg)
        kj_column.append(kj)

    return length_column, bg_column, kj_column


def get_temperature_data(sugar):
    filepath = "raw_data/{}-temperature.txt".format(sugar)
    header, values = get_data_from_filepath(filepath)

    temperature_column = Column([])
    red_column = Column([])
    yellow_column = Column([])
    green_column = Column([])
    blue_column = Column([])

    for row in values:
        temperature = Measurement(row[0] + 273.15, row[1])
        red = Measurement(row[2], row[3] / 2)
        yellow = Measurement(row[4], row[5] / 2)
        green = Measurement(row[6], row[7] / 2)
        blue = Measurement(row[8], row[9] / 2)

        temperature_column.append(temperature)
        red_column.append(red)
        yellow_column.append(yellow)
        green_column.append(green)
        blue_column.append(blue)

    return temperature_column, [red_column, yellow_column, green_column, blue_column]


def get_data_set(color, variation, sugar):
    filepath = "raw_data/" + sugar + "-" + variation + "-" + color + ".txt"
    return get_data_from_filepath(filepath)


def get_data_from_filepath(filepath):
    """
    Gets the data from a filepath and returns the header and columns
    Parameters
    ----------
    filepath : str
    """
    print("Getting filepath: ", filepath)
    file = open(filepath, "r")

    header = []
    columns = []

    line_counter = 0
    for line in file:
        row = []
        if line_counter != 0:
            columns.append([])

        index = 0

        while True:
            try:
                row.append(line.split('\t')[index])
                index += 1
            except IndexError:
                break

        try:
            current_row_string = ""
            for i in range(len(row)):
                row[i] = float(row[i])
                number_of_spaces = len(header[i]) - len(str(row[i])) + 5
                current_row_string += str(row[i]) + " " * number_of_spaces
                columns[line_counter - 1].append(row[i])
            print(current_row_string)
        except ValueError:
            header_string = ""
            for i in range(len(row)):
                header.append(row[i].replace('\n', ''))
                if i == len(row) - 1:
                    header_string += header[i]
                else:
                    header_string += header[i] + "  |  "
            print(header_string)

        line_counter += 1

    file.close()

    return header, columns




def generate_concentrations():
    concentrations = np.arange(0.1, 0.55, 0.05)

    concentrations = np.flip(concentrations)


    Vc = np.array([])

    i = 0

    while i < len(concentrations) - 1:
        Vc = np.append(Vc, concentrations[i + 1] * 50 / concentrations[i])
        i += 1


    def calc_error(c_number):

        if c_number == 0:
            e = concentrations[0] * np.power((np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2)), 0.5)
            return concentrations[0] * np.power((np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2)), 0.5)

        first_term = (np.power(0.1 / 50, 2) + np.power(0.5 / 100, 2))

        second_term = c_number * np.power(0.5 / 50, 2)

        third_term = 0

        x = 0

        while x < c_number:
            third_term += np.power(0.5 / Vc[x], 2)

            x += 1

        return concentrations[c_number] * np.power(first_term + second_term + third_term, 0.5)

    c_errors = np.array([])

    y = 0

    while y < len(concentrations):
        c_errors = np.append(c_errors, calc_error(y))
        y += 1

    col = Column([])

    for i in range(len(concentrations)):
        col.append(Measurement(concentrations[i], c_errors[i]))

    return col



# def get_concentration_plot_data(color=BLUE, sugar=FRUCTOSE):
#     concentration, bg, kj = get_concentration_data(color=color, sugar=sugar)
#
#     average_col = average_for_each_row(bg, kj)
#
#     average_col = Column([Measurement(180, 0)] * len(average_col.values)) - average_col
#
#     x_vals = concentration.get_just_values()
#     x_unerts = concentration.get_just_uncertainties()
#     y_vals = average_col.get_just_values()
#     y_errs = average_col.get_just_uncertainties()
#
#     chi2, reduced_chi2 = calculate_chi2(x_vals, y_vals, y_errs)
#
#     plt.show()
#
#     fmt = ""
#     if color == RED:
#         fmt = 'r'
#     elif color == YELLOW:
#         fmt = 'y'
#     elif color == GREEN:
#         fmt = 'g'
#     elif color == BLUE:
#         fmt = 'b'
#
#     concentration.to_string()
#     average_col.to_string()
#
#     a, b = best_linear_fit(concentration, average_col)
#     y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
#     m = b
#     c = a
#
#     residuals_x, residual_values = residuals(m, c, concentration, average_col)


def plot_concentration_data(color=BLUE, sugar=FRUCTOSE):
    concentration, bg, kj = get_concentration_data(color=color, sugar=sugar)

    average_col = average_for_each_row(bg, kj)

    average_col = Column([Measurement(180, 0)] * len(average_col.values)) - average_col

    x_vals = concentration.get_just_values()
    x_unerts = concentration.get_just_uncertainties()
    y_vals = average_col.get_just_values()
    y_errs = average_col.get_just_uncertainties()

    chi2, reduced_chi2 = calculate_chi2(x_vals, y_vals, y_errs)

    fmt = get_fmt(color)

    concentration.to_string()
    average_col.to_string()

    a, b = best_linear_fit(concentration, average_col)
    y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
    m = b
    c = a

    volumn = Measurement(50, 0.5)
    specific_rotation = calculate_specific_rotation_for_concentration(volumn, m)

    print("Specific rotation = {:.6f}".format(specific_rotation.value), specific_rotation.to_string())

    residuals_x, residual_values = residuals(m, c, concentration, average_col)

    ##### Plotting ######
    plt.figure(figsize=(10, 9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])

    plt.subplot(gs[0])
    sugar_string = sugar
    if sugar == GLUCOSE:
        sugar_string = "Sucrose"

    wavelength = color_wavelengths[get_color_index(color)]

    plt.title("Varying concentration - {} ({}nm) - {}".format(color, wavelength,sugar_string))
    plt.xlabel('concentration g/ml')
    plt.ylabel('polarization angle / deg')
    plt.errorbar(x_vals, y_vals, xerr=x_unerts, yerr=y_errs, fmt=fmt + 'x')
    plt.plot(x_vals, y_best_fit_vals, fmt)

    plt.subplot(gs[1])
    plt.title('Residuals in Polarization Angle')
    plt.errorbar(residuals_x.get_just_values(), residual_values.get_just_values(), yerr=y_errs, fmt=fmt + 'x')
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
    plt.annotate('specific rotation = {} deg dm^-1 cm^3 g^-1'.format(specific_rotation.to_string()), (0, 0), (250, -60),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')

    plt.tight_layout()
    plt.savefig('concentration-{}.pdf'.format(color))

    plt.savefig('plots/concentration/{}-{}-varying-concentration.png'.format(sugar, color))

    plt.show()
    print("-------------------------------------------------")


def get_fmt(color):
    fmt = ""
    if color == RED:
        fmt = 'r'
    elif color == YELLOW:
        fmt = 'y'
    elif color == GREEN:
        fmt = 'g'
    elif color == BLUE:
        fmt = 'b'
    return fmt


def calculate_specific_rotation_for_concentration(volume, gradient):
    """
    calculates the specific rotation from the fixed volume and gradient with varying concentration
    Parameters
    ----------
    volume : Measurement
    gradient : Measurement
    """
    length = (volume * (Measurement(15.4, 0.05) / Measurement(90, 0.5))) * Measurement(0.1, 0)
    specific_rotation = gradient / length
    return specific_rotation


def calculate_specific_rotation_for_length(concentration, gradient):
    """"
    calculates the specific rotation from the fixed concentration and gradient with varying length/(volume)
    Parameters
    ----------
    concentration : Measurement
    gradient : Measurement
    """
    specific_rotation = gradient / concentration
    return specific_rotation


blue_xs = []
blue_x_uncerts = []
blue_ys = []
blue_ys_uncerts = []

green_xs = []
green_x_uncerts = []
green_ys = []
green_ys_uncerts = []

yellow_xs = []
yellow_x_uncerts = []
yellow_ys = []
yellow_ys_uncerts = []

red_xs = []
red_x_uncerts = []
red_ys = []
red_ys_uncerts = []


def get_color_index(color):
    if color == RED:
        return 0
    elif color == YELLOW:
        return 1
    elif color == GREEN:
        return 2
    else:
        return 3


def plot_all_concentration(sugar):

    specific_rotations = []

    for color in colors:
        concentration, bg, kj = get_concentration_data(color=color, sugar=sugar)

        average_col = average_for_each_row(bg, kj)

        average_col = Column([Measurement(180, 0)] * len(average_col.values)) - average_col

        x_vals = concentration.get_just_values()
        x_unerts = concentration.get_just_uncertainties()
        y_vals = average_col.get_just_values()
        y_errs = average_col.get_just_uncertainties()

        a, b = best_linear_fit(concentration, average_col)
        y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
        m = b
        c = a

        volume = Measurement(50, 0.5)
        specific_rotation = calculate_specific_rotation_for_concentration(volume, m)
        print("specific rotation = ", specific_rotation.to_string())

        specific_rotations.append(specific_rotation.value)

        fmt = get_fmt(color)

        plt.errorbar(x_vals, y_vals, xerr=x_unerts, yerr=y_errs, fmt=fmt + 'x')
        plt.plot(x_vals, y_best_fit_vals, fmt)

    volume = 50
    if sugar == GLUCOSE:
        volume = 70

    sugar_string = "Sucrose"
    if sugar == FRUCTOSE:
        sugar_string = FRUCTOSE

    plt.title("Varying Concentration - volume  of {}ml - {}".format(volume, sugar_string))
    plt.xlabel('concentration - g/ml')
    plt.ylabel('polarization angle / deg')
    plt.legend(["Red - 630nm", "Yellow - 580nm", "Green - 525nm", "Blue - 468nm"])

    plt.savefig('plots/concentration/all-colors-{}.png'.format(sugar))

    plt.show()
    #
    # xs = [468, 528, 580, 630]
    # ys = Column(specific_rotations)
    #
    # plt.errorbar(xs, ys.get_just_values(), y_errs=ys.get_just_uncertainties())
    # plt.show()
    print("-------------------------------------------------")




def plot_length_data(color=BLUE, sugar=GLUCOSE):
    lengths, bg, kj = get_length_data(color=color, sugar=sugar)

    average_col = average_for_each_row(bg, kj)

    average_col = Column([Measurement(180, 0)] * len(average_col.values)) - average_col

    x_vals = lengths.get_just_values()
    x_unerts = lengths.get_just_uncertainties()
    y_vals = average_col.get_just_values()
    y_errs = average_col.get_just_uncertainties()

    chi2, reduced_chi2 = calculate_chi2(x_vals, y_vals, y_errs)

    fmt = get_fmt(color)

    a, b = best_linear_fit(lengths, average_col)
    y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
    m = b
    c = a

    concentration = Measurement(50, 0.1) / Measurement(100, 0.5)
    specific_rotation = calculate_specific_rotation_for_length(concentration, m)
    print("Specific rotation = ", specific_rotation.to_string())

    residuals_x, residual_values = residuals(m, c, lengths, average_col)

    ##### Plotting ######
    plt.figure(figsize=(10, 9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])

    plt.subplot(gs[0])

    sugar_string = sugar
    if sugar == GLUCOSE:
        sugar_string = "Sucrose"

    wavelength = color_wavelengths[get_color_index(color)]

    plt.title("Varying Volume/Length Traversed - {} ({}) - {}".format(color, wavelength,sugar_string))
    plt.xlabel('length traversed - dm')
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
    plt.annotate('specific rotation / deg dm^-1 cm^3 g^-1 = {}'.format(specific_rotation.to_string()), (0, 0), (250, -60),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')

    plt.tight_layout()
    plt.savefig('plots/length/{}-{}-length.png'.format(sugar, color))

    plt.show()
    print("-------------------------------------------------")


def plot_all_length_on_one(sugar):
    for color in colors:
        lengths, bg, kj = get_length_data(color=color, sugar=sugar)

        average_col = average_for_each_row(bg, kj)

        average_col = Column([Measurement(180, 0)] * len(average_col.values)) - average_col

        x_vals = lengths.get_just_values()
        x_unerts = lengths.get_just_uncertainties()
        y_vals = average_col.get_just_values()
        y_errs = average_col.get_just_uncertainties()

        a, b = best_linear_fit(lengths, average_col)
        y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
        m = b
        c = a

        fmt = get_fmt(color)

        plt.errorbar(x_vals, y_vals, xerr=x_unerts, yerr=y_errs, fmt=fmt + 'x')
        plt.plot(x_vals, y_best_fit_vals, fmt)

    sugar_string = sugar
    if sugar == GLUCOSE:
        sugar_string = "Sucrose"
    plt.title("Varying Length traversed- {} ".format(sugar_string))
    plt.xlabel('length traversed - dm')
    plt.ylabel('polarization angle / deg')
    plt.legend(["Red - 630nm", "Yellow - 580nm", "Green - 525nm", "Blue - 468nm"])

    plt.savefig('plots/length/all-colors-{}.png'.format(sugar))

    plt.show()
    print("-------------------------------------------------")


def plot_all_temperature_on_one(sugar):
    for color in colors:
        temperature_column, all_colors_columns_polarization = get_temperature_data(sugar=sugar)

        index = get_color_index(color)

        current_polarization_column = all_colors_columns_polarization[index]

        current_polarization_column = Column([Measurement(180, 0)] * len(current_polarization_column.values)) - current_polarization_column

        x_vals = temperature_column.get_just_values()
        x_unerts = temperature_column.get_just_uncertainties()
        y_vals = current_polarization_column.get_just_values()
        y_errs = current_polarization_column.get_just_uncertainties()

        a, b = best_linear_fit(temperature_column, current_polarization_column)
        y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
        m = b
        c = a

        fmt = get_fmt(color)

        plt.errorbar(x_vals, y_vals, xerr=x_unerts, yerr=y_errs, fmt=fmt + 'x')
        plt.plot(x_vals, y_best_fit_vals, fmt)

    volume = 'ml'
    if sugar == FRUCTOSE:
        volume = 50
    else:
        volume = 70

    sugar_string = "Sucrose"
    if sugar == FRUCTOSE:
        sugar_string = "Fructose"

    plt.title("Varying Temperature - volume of {}ml - {}".format(volume, sugar_string))
    plt.xlabel('Tmperature - K')
    plt.ylabel('polarization angle / deg')
    plt.legend(["Red - 630nm", "Yellow - 580nm", "Green - 525nm", "Blue - 468nm"])

    plt.savefig('plots/temperature/all-colors-{}.png'.format(sugar))

    plt.show()
    print("-------------------------------------------------")


def get_sugar_string(sugar):
    sugar_string = sugar
    if sugar == GLUCOSE:
        sugar_string = "Sucrose"
    return sugar_string


def plot_temperature(color, sugar):
    temperatures, all_colors = get_temperature_data(sugar)

    color_column = all_colors[get_color_index(color)]

    color_column = Column([Measurement(180, 0)] * len(color_column.values)) - color_column

    x_vals = temperatures.get_just_values()
    x_unerts = temperatures.get_just_uncertainties()

    y_vals = color_column.get_just_values()
    y_errs = color_column.get_just_uncertainties()

    chi2, reduced_chi2 = calculate_chi2(x_vals, y_vals, y_errs)

    fmt = get_fmt(color)

    a, b = best_linear_fit(temperatures, color_column)
    y_best_fit_vals = [a.value + b.value * xi for xi in x_vals]
    m = b
    c = a

    residuals_x, residual_values = residuals(m, c, temperatures, color_column)

    ##### Plotting ######
    plt.figure(figsize=(10, 9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])

    plt.subplot(gs[0])
    sugar_string = sugar
    volume = 50
    if sugar == GLUCOSE:
        sugar_string = "Sucrose"
        volume = 70

    wavelength = color_wavelengths[get_color_index(color)]

    plt.title("Varying Temperature - {} ({}nm) - {}".format(color, wavelength, sugar_string))
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
    plt.annotate('Volme traversed = {}ml'.format(volume),
                 (0, 0), (250, -60),
                 xycoords='axes fraction', textcoords='offset points',
                 va='top')

    plt.tight_layout()
    plt.savefig('plots/temperature/{}-{}-temperature.png'.format(sugar, color))

    plt.show()
    print("-------------------------------------------------")


def generate_concentration_plots():
    plot_all_concentration(FRUCTOSE)
    plot_all_concentration(GLUCOSE)
    for color in colors:
        plot_concentration_data(color, GLUCOSE)
        plot_concentration_data(color, FRUCTOSE)


def generate_length_plots():
    plot_all_length_on_one(FRUCTOSE)
    plot_all_length_on_one(GLUCOSE)
    for color in colors:
        plot_length_data(color, GLUCOSE)
        plot_length_data(color, FRUCTOSE)


def generate_temperature_plots():
    plot_all_temperature_on_one(FRUCTOSE)
    plot_all_temperature_on_one(GLUCOSE)
    for color in colors:
        plot_temperature(color, GLUCOSE)
        plot_temperature(color, FRUCTOSE)

# plot_all_concentration(FRUCTOSE)
#
# for color in colors:
#     # plot_concentration_data(color, GLUCOSE)
#     plot_length_data(color, FRUCTOSE)
#     plot_length_data(color, GLUCOSE)
#
#     print("-------------------------------------------------")

generate_temperature_plots()
generate_length_plots()
generate_concentration_plots()


# plot_concentration_data(RED)
