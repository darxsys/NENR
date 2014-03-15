import sys
import math
import numpy as np

def calc_output_single(parameters, input_):
    """Calculates output for an anfis with two inputs and one output.
    """

    # print ("Num rules: " + str(parameters.shape[0]))
    result = np.zeros((parameters.shape[0], 4))
    # print (result)
    sum_w = 0.
    result_sum = 0.

    for i in range(parameters.shape[0]):
        result[i][0] = sigmo(parameters[i][0], parameters[i][1], input_[0])
        result[i][1] = sigmo(parameters[i][2], parameters[i][3], input_[1])
        result[i][2] = einstein(result[i][0], result[i][1])
        result[i][3] = parameters[i][4] * input_[0] + parameters[i][5] * input_[1] + \
            parameters[i][6]
        sum_w += result[i][2]

    for i in range(parameters.shape[0]):
        result_sum += (float(result[i][2]) * result[i][3])

    result_sum /= float(sum_w)
    return result, result_sum, sum_w

def sigmo(a, b, x):
    return 1./(1. + math.exp(b * (x - a)))

def einstein(a, b):
    return float(a) * b / (2. - (a + b - a * float(b)))