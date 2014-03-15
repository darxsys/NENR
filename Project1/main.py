import sys

from domain import *
from fuzzy_set import *
from utils import *
from parser import *

def test():

	if not len(sys.argv) == 2:
		print ("python main.py filename")
		sys.exit(1)

	domains = {}
	sets = {}
	operators = {}
	operators["+"] = ("ZadehS",)
	operators["*"] = ("ZadehT",)
	operators["!"] = ("ZadehNot",)
	operators["->"] = ("'max-min'",)


	parser = Parser(sys.argv[1], domains, sets, operators)
	parser.parse()

	# print sets["f1"]
	# sys.stdout.flush()
	# print sets["f2"]
	# sys.stdout.flush()
	# for domain in domains:
	# 	print domains[domain]

	# for set_ in sets:
	# 	print sets[set_]

	# definition = ["x1", "x2", "x3", "x4"]
	# d1 = DomainEnum("d1", definition)


if __name__ == "__main__":
	test()