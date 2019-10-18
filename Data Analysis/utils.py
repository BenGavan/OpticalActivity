import numpy as np


class Measurement:

    def __init__(self, value, uncertainty):
        self.value = value
        self.uncertainty = uncertainty

    def __add__(self, other):
        if type(self) == type(other):
            return self.add(other)
        else:
            other_value = Measurement(other, 0)
            return self.add(other_value)

    def __sub__(self, other):
        new_value = self.value - other.value
        new_uncert = self.add_uncertainty(other)
        return Measurement(new_value, new_uncert)

    def __mul__(self, other):
        new_value = self.value * other.value
        new_uncert = self.multiply_uncertainty(other, new_value)
        return Measurement(new_value, new_uncert)

    def __truediv__(self, other):
        new_value = self.value / other.value
        new_uncert = self.multiply_uncertainty(other, new_value)
        return Measurement(new_value, new_uncert)

    def add(self, other):
        new_value = self.value + other.value
        new_uncert = self.add_uncertainty(other)
        return Measurement(new_value, new_uncert)

    def add_uncertainty(self, other):
        return pow((self.uncertainty * self.uncertainty) + (other.uncertainty * other.uncertainty), 0.5)

    def multiply_uncertainty(self, other, new_value):
        return pow(pow(self.uncertainty / self.value, 2) + pow(other.uncertainty / other.value, 2), 0.5) * abs(new_value)

    def __print__(self):
        return str(self.value) + "±" + str(self.uncertainty)

    def to_string(self):
        """
        Generates a string representing all the values and uncertainties in the column
        :return:
        """
        return "{:.3f} ± {:.3f}".format(self.value, self.uncertainty)


class Column:

    def __init__(self, values):
        self.values = values

    def __add__(self, other):
        if len(self.values) != len(other.values):
            print("ERROR: Column lengths do not match")
            return

        new_column_values = []

        for i in range(len(self.values)):
            new_value = self.values[i] + other.values[i]
            new_column_values.append(new_value)

        return Column(new_column_values)

    def __sub__(self, other):
        if len(self.values) != len(other.values):
            print("ERROR: Column lengths do not match")
            return

        new_column_values = []

        for i in range(len(self.values)):
            new_value = self.values[i] - other.values[i]
            new_column_values.append(new_value)

        return Column(new_column_values)

    def __mul__(self, other):
        if len(self.values) != len(other.values):
            print("ERROR: Column lengths do not match")
            return

        new_column_values = []

        for i in range(len(self.values)):
            new_value = self.values[i] * other.values[i]
            new_column_values.append(new_value)

        return Column(new_column_values)

    def __truediv__(self, other):
        if len(self.values) != len(other.values):
            print("ERROR: Column lengths do not match")
            return

        new_column_values = []

        for i in range(len(self.values)):
            new_value = self.values[i] / other.values[i]
            new_column_values.append(new_value)

        return Column(new_column_values)

    def __len__(self):
        return len(self.values)

    def append(self, measurement):
        self.values.append(measurement)

    def to_string(self):
        out_string = ""
        for val in self.values:
            out_string += str(val.value) + " ± " + str(val.uncertainty) + "\n"
        return out_string

    def get_just_values(self):
        vals = []
        for value in self.values:
            vals.append(value.value)
        return vals

    def get_just_uncertainties(self):
        uncerts = []
        for value in self.values:
            uncerts.append(value.uncertainty)
        return uncerts

    def sum(self):
        total = Measurement(0, 0)
        for value in self.values:
            total += value
        return total


class Table:

    def __init__(self, headers, columns):
        self.headers = headers
        self.columns = columns


def average_for_each_row(column_one, column_two):
    """"
    calculates the average of each row in the column
    Parameters
    ----------
    column_one : Column
    column_two : Column
    """
    div_col = []
    for i in range(len(column_one.values)):
        div_col.append(Measurement(2, 0))
    div_column = Column(div_col)
    return (column_one + column_two) / div_column


# solve for m and c
def best_linear_fit(x_col, y_col):
    """
    Generates m and c of the best fit line
    Parameters
    ----------
    x_col : Column
    y_col : Column
    ----------
    """

    print("x errors:")
    print(x_col.get_just_uncertainties())
    print("\ny errors:")
    print(y_col.get_just_uncertainties())
    # for x in x_col.get_just_uncertainties():
    #     print("{:.6f}".format(x))


    total_x = Measurement(0, 0)
    for x in x_col.values:
        total_x += x
    average_x = total_x / Measurement(len(x_col), 0)

    total_y = Measurement(0, 0)
    for y in y_col.values:
        total_y += y
    average_y = total_y / Measurement(len(y_col), 0)

    total_xy = Measurement(0, 0)
    for x, y in zip(x_col.values, y_col.values):
        total_xy += x * y
    average_xy = total_xy / Measurement(len(x_col), 0)

    total_x_2 = Measurement(0, 0)
    for x in x_col.values:
        total_x_2 += x * x
    average_x_2 = total_x_2 / Measurement(len(x_col), 0)

    gradient = ((average_x * average_y) - average_xy) / ((average_x * average_x) - average_x_2)

    y_intercept = average_y - gradient * average_x

    print('best fit line:\ny = {:} + {:}x'.format(y_intercept.to_string(), gradient.to_string()))
    return y_intercept, gradient


def calculate_weight_of_each_point(errors):
    weight_of_each_point = []

    if min(errors) > 0:
        for error in errors:
            weight_of_each_point.append(1 / error)
    return weight_of_each_point


def calculate_chi2(x, y, errors):
    weight_of_each_point = calculate_weight_of_each_point(errors)
    number_of_parameters = 2
    order = 1
    fitted_structure = np.polyfit(x, y, order, cov=True, w=weight_of_each_point)
    degrees_of_freedom = len(x) - number_of_parameters

    chisqrd = 0
    p = fitted_structure[0]

    for i, j, k in zip(x, y, errors):
        c = pow(((j - np.polyval(p, i)) / k), 2)
        chisqrd += c

    reduced_chi2 = chisqrd / degrees_of_freedom

    return chisqrd, reduced_chi2


def residuals(m, c, xs, ys):
    residuals = []
    for i in range(len(xs)):
        current_x = xs.values[i]
        bestfit_y = (m * current_x) + c

        residual = ys.values[i] - bestfit_y
        residuals.append(residual)

    return xs, Column(residuals)


def print_table(header, columns):
    header_string = ""
    for i in range(len(header)):
        if i == len(header) - 1:
            header_string += header[i]
        else:
            header_string += header[i] + "  |  "
    print(header_string)
    print("number of columns = ", number_of_columns(columns))
    print("column length = ", len(columns[0]))
    print("text value", columns[1][1])

    for row_index in range(len(columns[0])):
        current_row_string = ""
        for column_index in range(number_of_columns(columns)):
            print(row_index, column_index)
            print(current_row_string)
            number_of_spaces = len(header[column_index]) - len(str(columns[column_index][row_index])) + 5
            current_row_string += str(columns[column_index][row_index]) + " " * number_of_spaces
        print(current_row_string)



def plot(x, y, x_uncert, y_uncert):
    pass







def number_of_columns(columns):
    counter = 0
    for col in columns:
        counter += 1
    return counter





# def generate_concentration(n):
#     start_mass = Measurement(50, 0.1)
#     start_volumn = Measurement(100, 0.5)
#     start_concentration = start_mass / start_volumn
#     previous_concentration = start_concentration
#     mass = start_mass
#     volumn = start_volumn
#     current_concentration = None
#     for i in range(n):
#         desired_conventration = start_concentration - Measurement(0.05, 0)
#         mass_needed = desired_conventration * Measurement(50, 0.5)
#         volumn_of_previous_needed = previous_concentration * mass_needed
#         current_concentration = mass_needed / Measurement(50, 0.5)
#     return current_concentration
#
#
# def concentration(n):
#     if n == 0:
#         c_0 = Measurement(50, 0.1) / Measurement(100, 0.5)
#         return c_0.value
#     return 0.5 - 0.05 * (n - 1)
#
#
# def volume_carried(n):
#     return concentration(n + 1) * 100 / concentration(n)
#
#
# def uncertainty_in_concentration(n):
#     c_0 = Measurement(50, 0.1) / Measurement(100, 0.5)
#
#     if n == 0:
#         return c_0.uncertainty
#     c_n_value = 0.5 - 0.05 * (n - 1)
#     first_term = pow(c_0.uncertainty / c_0.value, 2)
#     second_term = n * pow(0.5 / 100, 2)
#     third_term = 0
#     for i in range(1, n):
#         third_term += pow(0.5 / volume_carried(i), 2)
#     delta_c_n = c_n_value * pow(first_term + second_term + third_term, 0.5)
#     return delta_c_n