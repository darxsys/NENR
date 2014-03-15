import sys
from domain import *
import utils

class FuzzySet(object):

	def __init__(self, name, domain, membership_values):

		self.domain = domain
		self.membership = membership_values
		self.name = name

	def getDomain(self):
		return self.domain

	def getMembershipFor(self, value):

		# print value
		index = self.domain.getIndexOfElement(value)

		if index == None:
			return 0
		return self.membership[index]

	def getName(self):
		return self.name

	def __str__(self):

		out = self.name + ": {"
		
		for i in range(len(self.membership)):
			if self.membership[i] > 0:
				out += str(self.membership[i]) + "/" + str(self.domain.elementAt(i)) + ", "

		if len(out) == len(self.name) + len(": {"):
			out += "}"
		else:
			out = out[:-2] + "}"

		return out

	def setName(self, name):
		self.name = name

	def checkIfReflexive(self):

		if not self.checkIfBinaryRelation():
			return False

		elements = self.domain.getDomains()[0].getElements()

		for elem in elements:
			# print elem, elem
			if abs(self.getMembershipFor(tuple([elem, elem])) - 1) > utils.EPSILON:
				return False

		return True

	def checkIfSymmetric(self):

		if not self.checkIfBinaryRelation():
			return False

		elements = self.domain.getElements()

		for (one, two) in elements:

			if abs(self.getMembershipFor((one, two)) - self.getMembershipFor((two, one))) > utils.EPSILON:
				return False

		return True

	def checkIfMaxMinTransitive(self):

		if not self.checkIfBinaryRelation():
			return False

		elements = self.domain.getElements()
		elements_first = self.domain.getDomains()[0].getElements()
		elements_second = self.domain.getDomains()[1].getElements()

		max_ = 0

		for (x, z) in elements:

			for second in elements_second:

					min_ = min(self.getMembershipFor((x, second)), self.getMembershipFor((second, z)))
					if min_ > max_:
						max_ = min_

			if max_ > self.getMembershipFor((x, z)):
				return False

			max_ = 0

		return True

	def checkIfMaxProductTransitive(self):

		if not self.checkIfBinaryRelation():
			return False

		elements = self.domain.getElements()
		elements_first = self.domain.getDomains()[0].getElements()
		elements_second = self.domain.getDomains()[1].getElements()

		max_ = 0

		for (x, z) in elements:

			for second in elements_second:

					min_ = self.getMembershipFor((x, second)) * self.getMembershipFor((second, z))
					if min_ > max_:
						max_ = min_

			if max_ > self.getMembershipFor((x, z)):
				return False

			max_ = 0

		return True

	def checkIfBinaryRelation(self):

		if not self.domain.getType() == "cartesian":
			print ("ERROR: this set is not a binary relation.")
			return False

		if not len(self.domain.getDomains()) == 2 or not self.domain.getDomains()[0] == self.domain.getDomains()[1]:
			print ("ERROR: this set is not a binary relation on one universal set.")
			return False	

		return True	


	def makeProjection(self, domain):

		if not self.domain.getType() == "cartesian":
			print ("ERROR: Set " + self.name + " is not a cartesian domain.")
			return None

		original_domains = self.getDomain().getDomains()

		if not utils.isSubset(original_domains, tuple(domain.getDomains())):
			print ("ERROR: Domain " + str(domain) + " is not a subset of domain " + str(self.domain) + ".")
			return None

		new_elements = domain.getElements()
		old_elements = self.domain.getElements()

		memberships = [None] * len(new_elements)

		for elem in new_elements:
			max_ = 0
			for old in old_elements:

				if utils.isSubset(old, elem):
					mem = self.getMembershipFor(old)
					if mem > max_:
						max_ = mem

			memberships[domain.getIndexOfElement(elem)] = max_

		return memberships

	def makeCylindricalExtension(self, domain):

		if not utils.isSubset(domain.getDomains(), self.domain.getDomains()):
			print ("ERROR. Can't extend to a domain that is not a superset of the current.")
			return None

		new_elements = domain.getElements()
		old_elements = self.domain.getElements()

		memberships = [None] * len(new_elements)

		for elem in new_elements:
			for old in old_elements:

				if utils.isSubset(elem, old):
					memberships[domain.getIndexOfElement(elem)] = self.getMembershipFor(old)

		return memberships

class FuzzySetOperator(FuzzySet):

	def __init__(self, name, left_set, right_set):

		self.left_set = left_set
		self.right_set = right_set
		self.domain = left_set.getDomain()
		self.membership = None
		self.name = name

	def __str__(self):

		# print "here"

		i = 0
		out = self. name + ": {"

		while not self.domain.elementAt(i) == None:

			# print i

			mem = self.getMembershipFor(self.domain.elementAt(i))
			# print mem
			if mem > 0:
				out += str(mem) + "/" + str(self.domain.elementAt(i)) + ", "

			i += 1

		if len(out) == len(self.name) + len(": {"):
			out += "}"
		else:
			out = out[:-2] + "}"

		return out

	def getLeftSet(self):
		return self.left_set

	def getRightSet(self):
		return self.right_set

class FuzzySetPlusZadeh(FuzzySetOperator):

	def __init__(self, name, left_set, right_set):
		FuzzySetOperator.__init__(self, name, left_set, right_set)

	def getMembershipFor(self, value):

		left_val = self.left_set.getMembershipFor(value)
		right_val = self.right_set.getMembershipFor(value)

		if left_val == -1 or right_val == -1:
			return -1

		return max(left_val, right_val)

class FuzzySetTimesZadeh(FuzzySetOperator):

	def __init__(self, name, left_set, right_set):
		FuzzySetOperator.__init__(self, name, left_set, right_set)

	def getMembershipFor(self, value):

		left_val = self.left_set.getMembershipFor(value)
		right_val = self.right_set.getMembershipFor(value)

		return min(left_val, right_val)		

class FuzzySetTimesProduct(FuzzySetOperator):

	def __init__(self, name, left_set, right_set):
		FuzzySetOperator.__init__(self, name, left_set, right_set)

	def getMembershipFor(self, value):

		left_val = self.left_set.getMembershipFor(value)
		right_val = self.right_set.getMembershipFor(value)

		return left_val * right_val		

class FuzzySetComplementZadeh(FuzzySetOperator):

	def __init__(self, name, source_set):

		self.source = source_set
		self.domain = source_set.getDomain()
		self.membership = None
		self.name = name

	def getMembershipFor(self, value):

		source_val = self.source.getMembershipFor(value)

		if source_val == -1:
			return -1
		return 1 - source_val

class FuzzySetPlusHammacher(FuzzySetOperator):

	def __init__(self, name, left_set, right_set, param):

		FuzzySetOperator.__init__(self, name, left_set, right_set)
		self.param = param

	def getMembershipFor(self, value):

		a = self.left_set.getMembershipFor(value)
		b = self.right_set.getMembershipFor(value)

		if a == -1 or b == -1:
			return -1

		return (a + b - (2 - self.param) * a * b) / float(1 - (1 - self.param) * a * b)

class FuzzySetTimesHammacher(FuzzySetOperator):

	def __init__(self, name, left_set, right_set, param):

		FuzzySetOperator.__init__(self, name, left_set, right_set)
		self.param = param

	def getMembershipFor(self, value):

		a = self.left_set.getMembershipFor(value)
		b = self.right_set.getMembershipFor(value)

		if a == -1 or b == -1:
			return -1

		return (a * b) / float(self.param + (1 - self.param) * (a + b - a * b))

class FuzzySetMamdani(FuzzySetOperator):

	def __init__(self, name, left_set, right_set):

		FuzzySetOperator.__init__(self, name, left_set, right_set)
		definition = list(left_set.getDomain().getDomains()) + (right_set.getDomain().getDomains())
		d = DomainCartesianControl(name + "set", definition, "cartesian")
		self.domain = d

		self.left_len = 1
		if left_set.getDomain().getType() == "cartesian":
			self.left_len = len(left_set.getDomain().getElements()[0])

		self.right_len = 1
		if right_set.getDomain().getType() == "cartesian":
			self.right_len = len(right_set.getDomain().getElements()[0])	

	def getMembershipFor(self, value):

		left = ""
		right = ""

		if self.left_len > 1:
			left = value[:self.left_len]
		else:
			left = value[0]

		if self.right_len > 1:
			right = value[self.left_len:self.right_len + 1]
		else:
			right = value[-1]

		# print left, right

		left = self.left_set.getMembershipFor(left)
		right = self.right_set.getMembershipFor(right)

		# sys.stderr.write(str((left, right)) + "\n")

		return (left, right)

class FuzzySetMamdaniMin(FuzzySetMamdani):

	def __init__(self, name, left_set, right_set):
		FuzzySetMamdani.__init__(self, name, left_set, right_set)

	def getMembershipFor(self, value):

		# print value
		left, right = FuzzySetMamdani.getMembershipFor(self, value)
		# print left, right
		return min(left, right)

class FuzzySetMamdaniProduct(FuzzySetMamdani):

	def __init__(self, name, left_set, right_set):
		FuzzySetMamdani.__init__(self, name, left_set, right_set)

	def getMembershipFor(self, value):

		left, right = FuzzySetMamdani.getMembershipFor(self, value)
		return left * right

