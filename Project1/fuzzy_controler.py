import sys

from domain import *
from fuzzy_set import *
from parser import *

class FuzzyControler(object):

	def __init__(self, angle_rules, acc_rules, domains_angle, domains_acc):

		self.angle_rules = angle_rules
		self.acc_rules = acc_rules
		self.domains_angle = domains_angle
		self.domains_acc = domains_acc

		self.intervals = []
		self.intervals.append(0)

		i = 1
		while i <= 2048:
			self.intervals.append(i)
			i *= 2

	def calculateNewAccAndAngle(self, L, D, LK, DK, V, S):

		left = (L, LK, S)
		right = (D, DK, S)

		left = self.transformToInterval(left)
		right = self.transformToInterval(right)

		left_acc = (left[0], right[0], V)
		right_acc = (left[1], right[1], V)

		angle = self.calcAngle(left, right, self.angle_rules, self.domains_angle)
		acc = self.calcAcc(left_acc, right_acc, self.acc_rules, self.domains_acc)
		sys.stderr.write(str(angle) + " " + str(acc) + "\n")
		return acc, angle

	def calcAngle(self, left, right, angle_rules, domains):

		# print domains
		angle_domain = domains["angle_domain"]
		cardinality = angle_domain.getCardinality()
		new_memberships = []
		domain_elements = angle_domain.getElements()

		# print "here"

		for i in range(cardinality):
# 
			y = domain_elements[i]

			left_elem = left + (y,)
			right_elem = right + (y,)

			# sys.stderr.write(str(left_elem) + "\n")
			# sys.stderr.write(str(right_elem) + "\n")
			# print right_elem

			max_ = 0

			for rule in angle_rules:
				# print "here"
				# print rule.name
				if rule.name.startswith("RULE_LEFT"):
					# print "here"
					min_ = rule.getMembershipFor(left_elem)
				else:
					min_ = rule.getMembershipFor(right_elem)

				# print min_
				if min_ > max_:
					max_ = min_

			new_memberships.append(max_)

		# print self.centerOfArea(new_memberships, domain_elements)
		result = int(self.centerOfArea(new_memberships, domain_elements))
		return result

	def calcAcc(self, left, right, acc_rules, domains):

		# print domains
		acc_domain = domains["acc_domain"]
		cardinality = acc_domain.getCardinality()
		new_memberships = []
		domain_elements = acc_domain.getElements()

		for i in range(cardinality):
# 
			y = domain_elements[i]

			left_elem = left + (y,)
			right_elem = right + (y,)

			max_ = 0

			for rule in acc_rules:
				# print "here"
				# print rule.name
				if rule.name.startswith("RULE_LD"):
					# print "here"
					min_ = rule.getMembershipFor(left_elem)
				else:
					sys.stderr.write(str(right_elem) + "\n")
					min_ = rule.getMembershipFor(right_elem)

				# print min_
				if min_ > max_:
					max_ = min_

			new_memberships.append(max_)

		# print self.centerOfArea(new_memberships, domain_elements)
		result = int(self.centerOfArea(new_memberships, domain_elements))
		return result

	def centerOfArea(self, memberships, elements):

		# print memberships, elements
		# print len(memberships)
		result = 0
		numerator = 0
		denominator = 0

		for i in range(len(memberships)):

			numerator += memberships[i] * elements[i]
			denominator += memberships[i]

		if denominator == 0:
			return 0
		result = float(numerator) / denominator
		return result

	def transformToInterval(self, elem):

		val = list(elem)
		for i in range(len(elem)):
			for j in range(1, len(self.intervals)):

				if elem[i] < self.intervals[j] and elem[i] >= self.intervals[j-1]:
					val[i] = self.intervals[j-1]

		return tuple(val)

def main():

	domains_angle = {}
	domains_acc = {}
	sets_angle = {}
	sets_acc = {}
	operators = {}
	operators["+"] = ("ZadehS",)
	operators["*"] = ("ZadehT",)
	operators["!"] = ("ZadehNot",)
	operators["->"] = ("'max-min'",)

	parser = Parser(sys.argv[1], domains_angle, sets_angle, operators)
	parser.parse()
	sets_angle = parser.rules

	parser = Parser(sys.argv[2], domains_acc, sets_acc, operators)
	parser.parse()
	sets_acc = parser.rules

	controler = FuzzyControler(sets_angle, sets_acc, domains_angle, domains_acc)

	while True:
	  	
	  	# print "here"
		line = sys.stdin.readline()

		if line == "KRAJ\n":
	  		break

		L,D,LK,DK,V,S = [int(s) for s in line.split() if s.isdigit()]
		akcel, kormilo = controler.calculateNewAccAndAngle(L, D, LK, DK, V, S)

		print akcel, kormilo
		sys.stdout.flush()

if __name__ == "__main__":
	main()
	
