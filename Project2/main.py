import sys

import nn
import dataset
import ga

def main(path, output):
    d = dataset.Dataset(path)
    print (d.num_examples())

    dimensions = [2,8,3]
    n = nn.NeuralNetwork(dimensions)
    g = ga.GA(d, n, 30)
    params = g.optimize()

    test_and_output(n, dimensions, params, d, output)

def test_and_output(network, dimensions, parameters, dataset, output):
    N = dataset.num_examples()
    correct = 0

    for i in range(N):
        example = dataset.example_at(i)
        out = network.calc_output(parameters, example[:2])
        
        for j in range(3):
            if out[j] >= 0.5:
                out[j] = str(1)
            else:
                out[j] = str(0)

        s = "".join(out)
        t = "".join([str(int(x)) for x in example[2:]])

        cor = "no."
        if s == t:
            correct += 1
            cor = "yes."

        print ("Example class:" + t + " Output: " + s + " Correct? " + cor)

    print ("Correct: " + str(correct) + " out of: " + str(N))
    # output w,s parameters for each neuron
    buf = ""
    for i in range(network.dimensions[1]):
        buf += str(parameters[i * 4]) + " " + str(parameters[i*4 + 2]) + " " + \
        str(parameters[i*4+1]) + " " + str(parameters[i*4+3]) + "\n"

    # print (buf)
    f = open(output, "w")
    if f == None:
        print("Cant open output file.")
        sys.exit(1)

    f.write(buf + "\n")

    buf = [str(x) for x in parameters[(network.dimensions[1] * 4):]]
    buf = " ".join(buf)
    f.write(buf + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough arguments.")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
