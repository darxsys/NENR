import sys
import numpy as np

import anfis

ERROR_THRESHOLD_ST = 0.2
ERROR_THRESHOLD_BT = 0.9

def stochastic_descent(num_rules, example_set, eta):
    """Does optimal parameter finding for an ANFIS with num_rules rules, two inputs and one
    output. Returns the parameters in an array of arrays.
    """

    rules_params = np.random.random_sample((num_rules, 7)) + 0.1
    # rules_params[0] = rules_params[1] = rules_params[2] = rules_params[3] = 1
    # print (rules_params)
    # max_error = calc_max_error(rules_params)
    max_error = -1
    N = len(example_set)
    # print (N)
    iter_num = 1
    while max_error < 0 or max_error > ERROR_THRESHOLD_ST:
        # max_error = 0.
        error = 0.
        # min_error = 1e9
        for i in range(len(example_set)):
            out_params, o, sum_w = anfis.calc_output_single(rules_params, example_set[i][:-1])
            delta = example_set[i][-1] - o

            error += 0.5 / N * (delta ** 2)
            # print (str(i) + " " + str(error))
            # set parameters of each rule to new values
            for j in range(num_rules):
                f_j = out_params[j][-1]
                sum_f = 0.
                for k in range(num_rules):
                    sum_f += out_params[k][-2] * (f_j - out_params[k][-1])
                # a_j
                mu_a_j = out_params[j][0]
                mu_b_j = out_params[j][1]
                w_j = out_params[j][2]
                a_j = rules_params[j][0]
                b_j = rules_params[j][1]
                c_j = rules_params[j][2]
                d_j = rules_params[j][3]
                p_j = rules_params[j][4]
                q_j = rules_params[j][5]
                r_j = rules_params[j][6]
                const_part = float(eta) * delta * sum_f / (sum_w ** 2.) / ((2-(mu_a_j + mu_b_j - mu_a_j * mu_b_j))**2.)

                # a_j
                rules_params[j][0] += const_part * b_j * mu_b_j * mu_a_j * (1 - mu_a_j) * (2 - mu_b_j)
                # b_j
                rules_params[j][1] += const_part * mu_b_j * (example_set[i][0] - a_j) * mu_a_j * (1 - mu_a_j) * (mu_b_j - 2)
                # c_j
                rules_params[j][2] += const_part * d_j * mu_a_j * mu_b_j * (1 - mu_b_j) * (2 - mu_a_j)
                # d_j
                rules_params[j][3] += const_part * mu_a_j * (example_set[i][1] - c_j) * mu_b_j * (1 - mu_b_j) * (mu_a_j - 2)
                # p_j
                rules_params[j][4] += float(eta) * delta * w_j * example_set[i][0] / sum_w
                # q_j
                rules_params[j][5] += float(eta) * delta * w_j * example_set[i][1] / sum_w
                # r_j
                rules_params[j][6] += float(eta) * delta * w_j / sum_w

        # error /= float(N)
        # print ("current error: " + str(error))
        print (str(iter_num) + " " + str(error))
        iter_num += 1
        if (error < ERROR_THRESHOLD_ST):
            break

    return rules_params

def batch_descent(num_rules, example_set, eta):
    """Does optimal parameter finding for an ANFIS with num_rules rules, two inputs and one
    output. Returns the parameters in an array of arrays.
    """

    rules_params = np.random.random_sample((num_rules, 7)) + 0.1
    # rules_params[0] = rules_params[1] = rules_params[2] = rules_params[3] = 1
    # print (rules_params)
    # max_error = calc_max_error(rules_params)
    error = -1
    N = len(example_set)
    # print (N)
    iter_num = 1
    while error < 0 or error > ERROR_THRESHOLD_BT:
        temp_sum = np.zeros((num_rules, 7))
        error = 0.

        for i in range(len(example_set)):
            # print (example_set[i])
            out_params, o, sum_w = anfis.calc_output_single(rules_params, example_set[i][:-1])
            delta = example_set[i][-1] - o

            error += 0.5*(delta ** 2)
            # if error > max_error:
            #     max_error = error

            # set parameters of each rule to new values
            for j in range(num_rules):
                f_j = out_params[j][-1]
                sum_f = 0.
                for k in range(num_rules):
                    sum_f += out_params[k][-2] * (f_j - out_params[k][-1])
                # a_j
                mu_a_j = out_params[j][0]
                mu_b_j = out_params[j][1]
                w_j = out_params[j][2]
                a_j = rules_params[j][0]
                b_j = rules_params[j][1]
                c_j = rules_params[j][2]
                d_j = rules_params[j][3]
                p_j = rules_params[j][4]
                q_j = rules_params[j][5]
                r_j = rules_params[j][6]
                const_part = float(eta) / N * delta * sum_f / (sum_w ** 2) / ((2-(mu_a_j + mu_b_j - mu_a_j * mu_b_j))**2)

                # a_j
                temp_sum[j][0] += const_part * b_j * mu_b_j * mu_a_j * (1 - mu_a_j) * (2 - mu_b_j)
                # b_j
                temp_sum[j][1] += const_part * mu_b_j * (example_set[i][0] - a_j) * mu_a_j * (1 - mu_a_j) * (mu_b_j - 2)
                # c_j
                temp_sum[j][2] += const_part * d_j * mu_a_j * mu_b_j * (1 - mu_b_j) * (2 - mu_a_j)
                # d_j
                temp_sum[j][3] += const_part * mu_a_j * (example_set[i][1] - c_j) * mu_b_j * (1 - mu_b_j) * (mu_a_j - 2)
                # p_j
                temp_sum[j][4] += float(eta) / N * delta * w_j * example_set[i][0] / sum_w
                # q_j
                temp_sum[j][5] += float(eta) / N * delta * w_j * example_set[i][1] / sum_w
                # r_j
                temp_sum[j][6] += float(eta) / N * delta * w_j / sum_w

        for j in range(num_rules):
            rules_params[j][0] += temp_sum[j][0]
            rules_params[j][1] += temp_sum[j][1]
            rules_params[j][2] += temp_sum[j][2]
            rules_params[j][3] += temp_sum[j][3]
            rules_params[j][4] += temp_sum[j][4]
            rules_params[j][5] += temp_sum[j][5]
            rules_params[j][6] += temp_sum[j][6]

        error /= float(N)
        # print ("current error: " + str(error))
        print (str(iter_num) + " " + str(error))
        iter_num += 1

    return rules_params    
