# col_one = Column([Measurement(0, 0),
#                   Measurement(1, 1),
#                   Measurement(2, 2),
#                   Measurement(3, 3)])
#
# col_two = Column([Measurement(0, 0),
#                   Measurement(1, 1),
#                   Measurement(2, 2),
#                   Measurement(3, 3)])
#
#
# col_three = col_one + col_two
#
# for val in col_three.values:
#     (val.value, val.uncertainty)
from utils import *

# test_col = Column([Measurement(1, 1), Measurement(1, 1)])
# (test_col.to_string())
#
#
# x = test_col.sum()
#
# (x.to_string())

# def generate_concentration(n):
# #     start_mass = Measurement(50, 0.1)
# #     start_volumn = Measurement(100, 0.5)
# #     start_concentration = start_mass / start_volumn
# #
# #     previous_concentration = start_concentration
# #
# #     current_concentration = start_concentration
# #     previous_mass = start_mass
# #     (current_concentration.to_string())
# #
# #     for i in range(n):
# #         volumn_required = previous_mass / previous_concentration
# #         current_concentration = (previous_concentration * volumn_required) / Measurement(50, 0.5)
# #         previous_mass = current_concentration * Measurement(50, 0.5)
# #         previous_concentration = current_concentration
# #         (current_concentration.to_string())
# #
# #     return current_concentration


def concentration(n):
    if n == 0:
        c_0 = Measurement(50, 0.1) / Measurement(100, 0.5)
        return c_0.value
    return 0.5 - 0.05 * (n - 1)


def volume_carried(n):
    return concentration(n + 1) * 100 / concentration(n)


def uncertainty_for_concentration(n):
    c_0 = Measurement(50, 0.1) / Measurement(100, 0.5)

    if n == 0:
        return c_0.uncertainty
    c_n_value = 0.5 - 0.05 * (n - 1)
    # first_term = pow(0.1 / 50, 2) + pow(0.5 / 100, 2)
    first_term = pow(c_0.uncertainty / c_0.value, 2)
    second_term = n * pow(0.5 / 100, 2)
    third_term = 0
    for i in range(1, n):
        third_term += pow(0.5 / volume_carried(i), 2)
    delta_c_n = c_n_value * pow(first_term + second_term + third_term, 0.5)
    return delta_c_n


if __name__ == '__main__':
    mass = Measurement(50, 0.1)
    vol = Measurement(100, 0.5)
    c_0 = mass/vol
    (c_0.to_string())

    x = Measurement(50, 0.1) / Measurement(100, 0.5)
    (x.to_string())

    first_term = pow(c_0.uncertainty / c_0.value, 2)
    print(first_term)
    # for i in range(1, 9):
    #     print(uncertainty_for_concentration(i))
    #     # print(volume_caried(i))





