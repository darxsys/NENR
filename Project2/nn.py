import sys
import math

import dataset

class NeuralNetwork(object):
    """ Class models a neural network with an input layer with two neurons, one hidden layer of neurons
    of type one, and zero or more hidden layers of neurons of type two. Network also has an output layer
    consisting of three neurons of type two.
    """

    def __init__(self, dimensions):
        """Accepts an array of values which are used as dimensions. For example, 2,8,3 creates a network
        of dimensions 2x8x3. Array has to have at least three elements.
        """

        if len(dimensions) < 3:
            raise ValueError ("Network has to have at least three layers.")
            sys.exit(1)

        if not dimensions[0] == 2 or not dimensions[-1] == 3:
            raise ValueError("This neural network supports only 2 input \
            neurons and 3 output neurons")
            sys.exit(1)

        self.dimensions = dimensions
        self.num_neurons = sum(dimensions)
        self.output = [None] * self.num_neurons
        self.num_parameters = 0
        self.num_parameters += self.dimensions[1] * 2 * 2
        for i in range(2, len(self.dimensions)):
            self.num_parameters += self.dimensions[i] * (self.dimensions[i-1] + 1)

    def num_params(self):
        """Returns number of parameters of the current neural network.
        """

        return self.num_parameters

    def calc_output(self, parameters, input_):
        """For given network parameters and input values, calculates network output.
        """

        if not len(parameters) == self.num_parameters:
            raise ValueError("Number of parameters does not match.\n")
            sys.exit(1)

        if not len(input_) == self.dimensions[0]:
            raise ValueError("Number of input variables not the same as \
                number of input neurons")
            sys.exit(1)

        # input layer
        for i in range(2):
            self.output[i] = input_[i]

        # first hidden layer - neurons of type 1
        for i in range(self.dimensions[1]):
            sum_ = 0
            sum_ += abs(input_[0] - parameters[4*i]) / float(abs(
                parameters[4*i + 1]))

            sum_ += abs(input_[1] - parameters[4*i + 2]) / float(abs(
                parameters[4*i + 3]))

            self.output[i+2] = float(1) / (1. + sum_)

        # all other layers - neurons of type 2
        param_offset = self.dimensions[1] * 4
        result_offset = self.dimensions[1] + 2

        for i in range(2, len(self.dimensions)):
            num_before = self.dimensions[i-1]
            for j in range(self.dimensions[i]):
                current_offset =  j * (num_before + 1)
                net = parameters[param_offset + current_offset]

                for k in range(num_before):
                    net += parameters[param_offset + k + 1 + current_offset] * \
                        float(self.output[result_offset - num_before + k])

                self.output[result_offset + j] = float(1) / (1. + math.exp(-net))

            param_offset += self.dimensions[i] * (num_before + 1)
            result_offset += self.dimensions[i]

        out = []
        out.append(self.output[-3])
        out.append(self.output[-2])
        out.append(self.output[-1])

        return out

    def calc_error(self, dataset, parameters):
        """ Calculates NN mean squared error on the dataset.
        """

        error = 0
        N = dataset.num_examples()
        
        for i in range(N):
            example = dataset.example_at(i)
            output = self.calc_output(parameters, example[:2])

            error += (float(example[2]) - output[0]) ** 2
            error += (float(example[3]) - output[1]) ** 2
            error += (float(example[4]) - output[2]) ** 2

        error /= float(N)
        return error
