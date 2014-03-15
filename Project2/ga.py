import sys
import random

import nn

NUM_ITER = 100000
V1 = 0.95
SIGMA_ONE = 0.2
SIGMA_TWO = 0.8
MUTATION_ONE = 0.03
MUTATION_TWO = 0.01
MAX_ERROR = 1e-7
EPS = 1e-9

class GA(object):
    """ Genetic algorithm used to train the neural network defined in module nn.
    """

    def __init__(self, dataset, nn, pop_size):
        self.dataset = dataset
        self.nn = nn
        self.pop_size = pop_size
        self.chromosome_size = self.nn.num_params()

    def optimize(self):
        """Main method that does optimization.
        """

        population, evaluation, best_index, min_error, max_error = self.generate_population()
        iters = 1

        while min_error > MAX_ERROR and iters < NUM_ITER:

            population, evaluation, max_error, min_error, best_index = self.three_tournament(
                population, evaluation, best_index, min_error, max_error)

            # if iters % 5000 == 0:
            sys.stdout.write("Iteration: " + str(iters) + " min_error: ")
            sys.stdout.write(str(min_error) + " max error: " + str(max_error) + "\n")
            # print (population[best_index])
            iters += 1

        print ("Min error: " + str(min_error))
        return population[best_index]
    def three_tournament(self, population, evaluation, best_index, min_error, max_error):
        """Does three tournament selection, crossover and mutation.
        """

        rand = random.sample(range(self.pop_size), 3)
        one_index = rand[0]
        two_index = rand[1]
        three_index = rand[2]

        one_val = evaluation[one_index]
        two_val = evaluation[two_index]
        three_val = evaluation[three_index]

        l = [(one_index, one_val), (two_index, two_val), (three_index, three_val)]

        max_ = max(l, key=lambda tup:tup[1])

        if max_[0] == one_index:
            worst = one_index
            parent_one = population[two_index]
            parent_two = population[three_index]

        if max_[0] == two_index:
            worst = two_index
            parent_one = population[one_index]
            parent_two = population[three_index]

        if max_[0] == three_index:
            worst = three_index
            parent_one = population[two_index]
            parent_two = population[one_index]

        # new_spec = self.crossover_(parent_one, parent_two)
        num = random.randint(1, 3)
        if num == 1:
            new_spec = self.crossover_four(parent_one, parent_two)
        elif num == 2:
            new_spec = self.crossover_two(parent_one, parent_two)
        elif num == 3:
            new_spec = self.crossover_five(parent_one, parent_two)

        prob = random.uniform(0,1)

        if prob <= V1:
            new_spec = self.mutation_one(new_spec)
        else:
            new_spec = self.mutation_two(new_spec)

        new_val = self.nn.calc_error(self.dataset, new_spec)
        population[worst] = new_spec
        evaluation[worst] = new_val

        if new_val > max_error:
            max_error = new_val
        if new_val < min_error:
            min_error = new_val
            best_index = worst

        return population, evaluation, max_error, min_error, best_index

    def crossover_one(self, parent_one, parent_two):
        """Does simple arithmetic recombination.
        """

        num = len(parent_one)
        index = random.randint(0, num-1)

        new_spec = parent_one[:index]
        for i in range(index, num):
            new_spec.append((parent_one[i] + parent_two[i]) / float(2))

        return new_spec

    def crossover_two(self, parent_one, parent_two):
        """Does full arithmetic recombination.
        """

        new_spec = []
        num = random.uniform(0,1)
        for i in range(len(parent_one)):
            new_spec.append(parent_one[i] * num + (1-num) * parent_two[i])

        return new_spec

    def crossover_three(self, parent_one, parent_two):
        """Does one break point crossover.
        """

        new_spec = []
        num = random.randint(0, len(parent_one) - 1)
        for i in range(len(parent_one)):
            if i < num:
                new_spec.append(parent_one[i])
            else:
                new_spec.append(parent_two[i])

        return new_spec

    def crossover_five(self, parent_one, parent_two):
        """Does one break point crossover with arithmetic mean.
        """

        new_spec = []
        num = random.randint(0, len(parent_one) - 1)
        for i in range(len(parent_one)):
            if i < num:
                new_spec.append(parent_one[i])
            else:
                new_spec.append((parent_one[i] + parent_two[i]) / 2.)

        return new_spec

    def crossover_four(self, parent_one, parent_two):
        """Does discrete uniform recombination.
        """

        # nums = random.sample(range(len(parent_one)), self.pop_size / 2)

        new_spec = []
        for i in range(len(parent_one)):
            num = random.randint(1,2)
            if num == 1:
                new_spec.append(parent_one[i])
            else:
                new_spec.append(parent_two[i])

        return new_spec


    def mutation_one(self, chromosome):
        """Does mutation according to parameters MUTATION_ONE and SIGMA_ONE.
        """

        new_spec = chromosome
        for i in range(len(new_spec)):
            if random.uniform(0,1) < MUTATION_ONE:
                new_spec[i] += random.gauss(0, SIGMA_ONE)

        return new_spec

    def mutation_two(self, chromosome):
        """Does mutation according to parameters MUTATION_TWO and SIGMA_TWO.
        """

        new_spec = chromosome
        for i in range(len(new_spec)):
            if random.uniform(0,1) < MUTATION_TWO:
                # uniformna mozda logicnija
                new_spec[i] = random.gauss(0, SIGMA_TWO)

        return new_spec


    def generate_population(self):
        """Generates a random chromosome population.
        """

        pop = []
        evaluation = []
        min_error = -1
        max_error = -1
        best_index = 0

        for i in range(self.pop_size):
            chromosome = []
            for j in range(self.chromosome_size):
                chromosome.append(random.uniform(-3,3))

            error = self.nn.calc_error(self.dataset, chromosome)
            evaluation.append(error)
            pop.append(chromosome)

            if min_error == -1:
                min_error = error

            if min_error > error:
                min_error = error
                best_index = i

            if error > max_error:
                max_error = error

        return pop, evaluation, best_index, min_error, max_error
