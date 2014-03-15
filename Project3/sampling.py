import sys
import math

def sample2D(xrange, yrange, output_file, function):
    with open(output_file, "w") as f:
        for x in xrange:
            for y in yrange:
                f.write(str(x) + " " + str(y) + " ")
                f.write(str(function(x, y)) + "\n")


def main(path, function, xrange, yrange):
    sample2D(xrange, yrange, path, function)

def function_one(x, y):
    return ((x-1)**2. + (y+2)**2 - 5 * x * y + 3) * math.cos(x/5.)**2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Output file, please.")

    main(sys.argv[1], function_one, [x for x in range(-4, 5)], [y for y in range(-4, 5)])
