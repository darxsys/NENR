import sys
import numpy as np 

import gradient
import anfis

NUM_RULES = 4
ETA_STOCH = 0.001
ETA_BATCH = 0.005
OUTPUT_ANFIS = False

""" Good params:
STOCHASTIC: ETA = 0.001
BATCH: ETA  = 0.006
"""

def main(examples_path, output_path, anfis_out=None):
    examples = []
    with open(examples_path, "r") as f:
        for line in f:
            a,b,c = line.strip().split()
            examples.append((float(a), float(b), float(c)))
#
    params = gradient.stochastic_descent(NUM_RULES, examples, ETA_STOCH)
    # params = gradient.batch_descent(NUM_RULES, examples, ETA_BATCH)
    with open(output_path, "w") as f:
        for i in range(NUM_RULES):
            for j in range(7):
                f.write(str(params[i][j]) + " ")
            f.write("\n")

    # return params
    if OUTPUT_ANFIS == True:    
        if anfis_out == None:
            raise ValueError("No anfis out file given.")
        output_anfis_values(params, examples, anfis_out)

def output_anfis_values(params, dataset, path):
    """Outputs values of anfis function to stdout for all
    members of the dataset.
    """
    with open(path, "w") as f:
        for example in dataset:
            f.write(str(example[0]) + " " + str(example[1]) + " " + \
                str(anfis.calc_output_single(params, example[:2])[1] - example[2]) + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("File with examples and parameter output file please.")

    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2])
