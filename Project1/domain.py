import sys
import itertools

import utils

class Domain(object):

	def __init__(self, name, definition, type_):

		self.name = name
		self.elements = definition
		self.indices = {}
		self.cardinality = len(definition)
		self.type = type_

		for i in range(0, len(self.elements)):
			self.indices[self.elements[i]] = i

	def fromStringRepresentation(self, value):
		return None
		
	def getIndexOfElement(self, value):

		# print "here"

		val = None
		try:
			val = self.indices[value]
		except:
			pass

		return val

	def elementAt(self, index):

		val = None
		try:
			val = self.elements[index]
		except:
			pass

		return val

	def getCardinality(self):

		return self.cardinality

	def getName(self):

		return self.name

	def getElements(self):
		return self.elements

	def getType(self):
		return self.type

	def __str__(self):
		return str(self.name)

	def getDomains(self):
		res = []
		res.append(self)
		return res

class DomainEnum(Domain):

	def fromStringRepresentation(self, value):

		val = None
		try:
			val = str(value)
		except:
			pass

		return val

class DomainInt(Domain):

	def fromStringRepresentation(self, value):

		val = None
		try:
			val = int(value)
		except:
			pass

		return val		

class DomainReal(Domain):

	def fromStringRepresentation(self, value):

		val = None
		try:
			val = float(value)
		except:
			pass

		return val		

	def getIndexOfElement(self, value):

		val = None

		for elem in self.elements:
			if abs(value - elem) < utils.EPSILON:
				val = self.indices[elem]

		return val

class DomainCartesian(Domain):

	def __init__(self, name, definition, type_):

		self.name = name
		self.domains = tuple(definition)
		self.type = type_

		val = 1
		for domain in self.domains:
				val *= domain.getCardinality()
		self.cardinality = val

		self.elements = self.__generateElements(definition)
		# print self.elements

	def fromStringRepresentation(self, value):

		val = []

		if len(value) != len(self.domains):
			return None

		for i in range(0, len(value)):

			temp = self.domains[i].fromStringRepresentation(value[i])
			if temp == None:
				return None
			val.append(temp)

		return tuple(val)

	def getIndexOfElement(self, value):

		# val = None
		if not len(value) == len(self.elements[0]):
			return val

		for i in range(len(self.elements)):

			equal = True
			for j in range(len(value)):

				if type(value[j]) == float:

					if not abs(value[j] - self.elements[i][j]) < utils.EPSILON:
						equal = False
						break
				else:

					if not value[j] == self.elements[i][j]:
						equal = False
						break

			if equal == True:
				return i

		return None

	def elementAt(self, index):

		# print index
		val = None
		try:
			val = self.elements[index]
		except:
			return val

		if len(val) == 1:
			val = val[0]
			
		return val


	def __str__(self):
		return str(self.name)

	def __generateElements(self, definition):

		num_elements = self.getCardinality()
		num_domains = len(definition)

		temp = []

		for i in range(num_domains):
			temp.append(definition[i].getElements())

		result = []

		for element in itertools.product(*temp):
			result.append(element)

		return result

	def getDomains(self):
		return self.domains


class DomainCartesianControl(DomainCartesian):

	def __init__(self, name, definition, type_):
		DomainCartesian.__init__(self, name, definition, type_)
		self.num = range(len(self.elements))
		self.num.reverse()
		self.val_len = len(self.elements[0])

	def getIndexOfElement(self, value):

		val = None
		if not len(value) == self.val_len:
			return val

		for i in self.num:

			equal = True
			for j in range(self.val_len):

				if not value[j] == self.elements[i][j]:
					equal = False
					break 

			if equal == True:
				return i

		# print "here"
		return None

if __name__ == "__main__":

	definition = [2,3,4,5]
	d = Domain(definition)
	print d.getIndexOfElement(5)