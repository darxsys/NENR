import sys

class Dataset(object):
    """Class stores all the examples from the training dataset.
    """

    def __init__(self, path):
        """Reads the training dataset from the file given with path.
        """

        dataset = open(path, "r")
        if dataset == None:
            raise ValueError("Could not open the file " + str(path) + "\n")
            sys.exit(1)

        self.examples = []
        for line in dataset:
            example = [float(x) for x in line.strip().split()]
            # print (example)
            self.examples.append(example)

        self.number = len(self.examples)

    def num_examples(self):
        return self.number

    def example_at(self, index):
        if index >= self.number:
            raise ValueError("Index out of bounds.\n")
            sys.exit(1)

        return self.examples[index]

