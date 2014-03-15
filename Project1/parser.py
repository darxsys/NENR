import sys
from domain import *
from fuzzy_set import *
import utils

class Parser(object):

	def __init__(self, filename, domains, sets, operators):

		self.filename = filename
		self.domains = domains
		self.sets = sets
		self.operators = operators
		self.rules = []

	def parse(self):

		file_ = ""
		try:
			file_ = open(self.filename, "r")
		except:
			print ("Error opening file. Exiting.")
			sys.exit(1)

		file_lines = file_.readlines()

		for input_line in file_lines:

			if input_line[0] == "#":
				continue

			# print input_line
			line = input_line.split()
			if len(line) == 0:
				continue

			if line[1] == "domain":
				self.createDomainFromLine(line, self.domains)

			elif line[1] == "fuzzyset" and line[2] == "@":
				# print "ere"
				self.createSetFromLine(line, self.sets, self.domains)

			elif line[0] == "set" and line[1] == "operator":
				self.changeOperatorDefinition(line, self.operators)

			elif line[0] == "write":

				name = line[1][:-1]

				if name in self.sets:
					print (self.sets[name])
				else:
					print ("Write ERROR: Set " + name + " does not exist.")

			elif line[1] == "fuzzyset" and line[2] == "expr":

				name = line[0][:-1]

				formula = "".join(line[3:]).strip()[:-1]
				# try:
				result = self.parseFormula(formula, self.sets, self.operators)
				if result == None:
					print ("Formula " + formula + " is not correctly input.")
				else:
					# print result
					result.setName(name)
					if name.startswith("RULE"):
						# print name
						self.rules.append(result)
					else:
						self.sets[name] = result

				# except:
				# 	print ("Formula " + formula + "is not correctly input.")
			elif line[0].startswith("test"):

				self.checkTest(line, self.sets)

			elif line[1] == "fuzzyset" and line[2] == "project":

				self.checkProjection(line, self.sets, self.domains)

			elif line[1] == "fuzzyset" and line[2] == "cylindrical_extension":

				self.checkCylindrical(line, self.sets, self.domains)

			elif line[1] == "fuzzyset" and line[2] == "composition":

				self.generateSetFromComposition(line, self.sets, self.domains)

	def createDomainFromLine(self, line, domains):

		name = line[0][:-1]
		domain_type = line[2]
		definition = []

		if domain_type == "enumerated":

			definition = self.createEnumList(line[3:])
			d = DomainEnum(name, definition, "enum")
			domains[d.getName()] = d

		elif domain_type == "integer":

			start = int(line[3])
			end = int(line[5])
			definition = []
			step = line[7][:-1]

			if step == "2toi":

				i = 1
				definition.append(0)
				while i <= end:
					definition.append(i)
					i *= 2

				definition.append(i)
				# print definition
			else:
				step = int(step)
				definition = self.createIntList(start, end, step)

			d = DomainInt(name, definition, "integer")
			domains[d.getName()] = d

		elif domain_type == "real":

			start = float(line[3])
			end = float(line[5])
			step = float(line[7][:-1])

			definition = self.createRealList(start, end, step)
			d = DomainReal(name, definition, "real")
			domains[d.getName()] = d

		elif domain_type == "cartesian":

			try:
			# print line
				domain_names = line[3].split(",")
				domain_names[-1] = domain_names[-1][:-1]
				cartesian_domains = []

				for domain in domain_names:
					cartesian_domains.append(domains[domain])

				d = DomainCartesian(name, cartesian_domains, "cartesian")
				domains[d.getName()] = d

			except:
				print ("Error: domain " + name + " is not properly defined")

	def createEnumList(self, list_values):

		result = []
		list_values[0] = list_values[0][1:]

		if len(list_values) > 1:
			list_values[-1] = list_values[-1][:-1]

		for val in list_values:
			result.append(val[:-1])

		return result

	def createRealList(self, start, end, step):

		result = []
		num = int((end - start) / step)

		for i in range(num):
			result.append(start + i * step)
		result.append(end)

		return result

	def createIntList(self, start, end, step):

		result = list(range(start, end + 1, step))
		return result

	def createSetFromLine(self, line, sets, domains):

		name = line[0][:-1]

		domain_name = line[3]

		if name in sets:
			if not domain_name == sets[name].getDomain().getName():
				print ("Cannot redefine set " + name + ". Domains before and after are not the same.")
				return

		memberships = []

		try:
			domain = self.domains[domain_name]
		except:
			print ("ERROR: Set " + name + " is wrongly defined.")
			return

		func = line[5].split("(")[0]
		if func == "gamma":
			memberships = self.generateMembershipsFromGamma(domain, line)

		elif func == "lambda":
			memberships = self.generateMembershipsFromLambda(domain, line)

		elif func == "l":
			memberships = self.generateMembershipsFromL(domain, line)

		elif func == "pi":
			memberships = self.generateMembershipsFromPi(domain, line)

		else:
			memberships = self.generateMembershipsFromLine(domain, line)

		s = FuzzySet(name, domain, memberships)
		sets[s.getName()] = s

	def generateMembershipsFromGamma(self, domain, line):

		parameters = line[5].split("(")[1].split(")")[0].split(",")
		# print parameters
		a = parameters[0]
		b = parameters[1]

		# print a, b

		elements = domain.getElements()
		result = [None] * len(elements)

		if domain.getType() == "enum":

			a = domain.getIndexOfElement(a)
			b = domain.getIndexOfElement(b)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.gamma(index, a, b)

		else:

			a = float(a)
			b = float(b)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.gamma(elem, a, b)

		return result
	
	def generateMembershipsFromLambda(self, domain, line):

		parameters = line[5].split("(")[1].split(")")[0].split(",")
		# print parameters
		a = parameters[0]
		b = parameters[1]
		c = parameters[2]

		elements = domain.getElements()
		result = [None] * len(elements)

		if domain.getType() == "enum":

			a = domain.getIndexOfElement(a)
			b = domain.getIndexOfElement(b)
			c = domain.getIndexOfElement(c)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.lambdaF(index, a, b, c)

		else:

			a = float(a)
			b = float(b)
			c = float(c)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.lambdaF(elem, a, b, c)

		return result

	def generateMembershipsFromL(self, domain, line):

		parameters = line[5].split("(")[1].split(")")[0].split(",")
		# print parameters
		a = parameters[0]
		b = parameters[1]

		# print a, b

		elements = domain.getElements()
		result = [None] * len(elements)

		if domain.getType() == "enum":

			a = domain.getIndexOfElement(a)
			b = domain.getIndexOfElement(b)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.functionL(index, a, b)

		else:

			a = float(a)
			b = float(b)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.functionL(elem, a, b)

		return result

	def generateMembershipsFromPi(self, domain, line):

		parameters = line[5].split("(")[1].split(")")[0].split(",")
		# print parameters
		a = parameters[0]
		b = parameters[1]
		c = parameters[2]
		d = parameters[3]

		elements = domain.getElements()
		result = [None] * len(elements)

		if domain.getType() == "enum":

			a = domain.getIndexOfElement(a)
			b = domain.getIndexOfElement(b)
			c = domain.getIndexOfElement(c)
			d = domain.getIndexOfElement(d)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.functionPi(index, a, b, c, d)

		else:

			a = float(a)
			b = float(b)
			c = float(c)
			d = float(d)

			for elem in elements:

				index = domain.getIndexOfElement(elem)
				result[index] = utils.functionPi(elem, a, b, c, d)

		return result

	def generateMembershipsFromLine(self, domain, line):

		elements = domain.getElements()
		# print elements
		result = []
		for elem in elements:
			result.append(0)

		line[5] = line[5][1:]
		if len(line[5:]) >= 1:
			line[-1] = line[-1][:-2]

		for frac in line[5:]:

			if frac == "+":
				continue

			if frac[-1] == ",":
				frac = frac[:-1]

			mi = float(frac.split("/")[0])
			element = frac.split("/")[1]

			if element[0] == "(":
				element = element[1:-1]

			if domain.getType() == "integer":
				element = int(element)

			elif domain.getType() == "real":
				element = float(element)

			elif domain.getType() == "cartesian":
				el = element.split(",")
				# print el
				element = domain.fromStringRepresentation(el)
				# print element

			index = domain.getIndexOfElement(element)
			# print index
			result[index] = mi

		return result

	def parseFormula(self, formula, sets, operators):

		if not len(formula):
			return None

		formula = formula.strip()

		if formula[0] == "f" and utils.isInt(formula[1:]):
			if formula in sets:
				return sets[formula]
			else:
				return None


		depth = 0
		tree = None
		for i in reversed(xrange(len(formula))):

			if formula[i] == ")":
				depth += 1
			elif formula[i] == "(":
				depth -= 1
			elif depth == 0:

				for operator in ["*", "+", "->"]:

					start = i - len(operator) + 1
					if formula[start:].startswith(operator):

						if tree is not None:
							return None
						
						definition = operators[operator]
						
						left_set = self.parseFormula(formula[0:start], sets, operators)
						right_set = self.parseFormula(formula[i + 1:], sets, operators)

						if left_set == None or right_set == None:
							return None

						s = ""

						if operator == "*":

							if not left_set.getDomain().getName() == right_set.getDomain().getName():
								print ("ERROR: Sets " + left_set.getName() + " and " + right_set.getName() + " dont have same domains.")
								return None

							if definition[0] == "ZadehT":
								s = FuzzySetTimesZadeh("temp", left_set, right_set)
							elif definition[0] == "HammacherT":
								param = definition[1]
								s = FuzzySetTimesHammacher("temp", left_set, right_set, param)

						elif operator == "+":

							if not left_set.getDomain().getName() == right_set.getDomain().getName():
								print ("ERROR: Sets " + left_set.getName() + " and " + right_set.getName() + " dont have same domains.")
								return None

							if definition[0] == "ZadehS":
								s = FuzzySetPlusZadeh("temp", left_set, right_set)
							elif definition[0] == "HammacherS":
								param = definition[1]
								s = FuzzySetPlusHammacher("temp", left_set, right_set, param)							

						elif operator == "->":
							# print definition
							if definition[0] == "'max-min'":
								# print "here"
								s = FuzzySetMamdaniMin("temp", left_set, right_set)
							elif definition[0] == "'max-product'":
								param = definition[1]
								s = FuzzySetMamdaniProduct("temp", left_set, right_set)							

						tree = s
						break

		if tree is not None:
			return tree

		if formula[0] == "!":
			definition = operators[formula[0]]

			s = ""
			if definition[0] == "ZadehNot":
				source = self.parseFormula(formula[1:], sets, operators)
				if source == None:
					return None

				s = FuzzySetComplementZadeh("temp", source)
				return s

		if formula[0] == "(" and formula[-1] == ")":
			return self.parseFormula(formula[1:-1], sets, operators)

		return None

	def changeOperatorDefinition(self, line, operators):

		if line[4].startswith("Zadeh"):
			operators[line[3]] = (line[4][:-1],)

		elif line[4].startswith("Hammacher"):
			# print ("Changing")
			param = float(line[4].split("(")[1].split(")")[0])
			operators[line[3]] = (line[4][:10], param)

			# print operators[line[3]]

	def checkTest(self, line, sets):

		name = line[1][:-1]
		result = False

		if name not in sets:
			print ("ERROR: This set does not exist.")
			return

		if line[0] == "testReflexive":

			sys.stdout.write(name + " is reflexive? ")
			result = sets[name].checkIfReflexive()

		elif line[0] == "testSymmetric":

			sys.stdout.write(name + " is symmetric? ")
			result = sets[name].checkIfSymmetric()

		elif line[0] == "testTransitive" and line[2] == "'max-min';":

			sys.stdout.write(name + " is max-min transitive? ")
			result = sets[name].checkIfMaxMinTransitive()

		elif line[0] == "testTransitive" and line[2] == "'max-product';":

			sys.stdout.write(name + " is max-product transitive? ")
			result = sets[name].checkIfMaxProductTransitive()

		elif line[0] == "testFuzzyEquivalence" and line[2] == "'max-min';":

			sys.stdout.write(name + " is fuzzy max-min-equivalence relation? ")
			result = sets[name].checkIfReflexive() and sets[name].checkIfSymmetric() and sets[name].checkIfMaxMinTransitive()

		elif line[0] == "testFuzzyEquivalence" and line[2] == "'max-product';":

			sys.stdout.write(name + " is fuzzy max-product-equivalence relation? ")
			result = sets[name].checkIfReflexive() and sets[name].checkIfSymmetric() and sets[name].checkIfMaxProductTransitive()
			
		if result == True:
			print ("YES")
		else:
			print ("NO")

	def checkProjection(self, line, sets, domains):

		name = line[0][:-1]
		source = line[3]

		if source not in sets:
			print ("ERROR: Set " + source + " does not exist.")
			return

		source = sets[source]
		domain = line[5][:-1]

		if domain not in domains:
			print ("ERROR: Domain " + domain + " does not exist.")
			return

		domain = domains[domain]
		memberships = source.makeProjection(domain)
		if memberships == None:
			return

		s = FuzzySet(name, domain, memberships)
		sets[name] = s

	def checkCylindrical(self, line, sets, domains):

		name = line[0][:-1]
		source = line[3]

		if source not in sets:
			print ("ERROR: Set " + source + " does not exist.")
			return

		source = sets[source]
		domain = line[5][:-1]

		if domain not in domains:
			print ("ERROR: Domain " + domain + " does not exist.")
			return

		domain = domains[domain]
		memberships = source.makeCylindricalExtension(domain)

		if memberships == None:
			return

		s = FuzzySet(name, domain, memberships)
		sets[name] = s

	def generateSetFromComposition(self, line, sets, domains):

		set1 = line[3][:-1].strip()
		set2 = line[4].strip()
		method = line[6][:-1].strip()
		name = line[0][:-1]

		if set1 not in sets or set2 not in sets:
			print ("ERROR: Sets " + set1 + " and " + set2 + " do not exist.")
			return

		set1 = sets[set1]
		set2 = sets[set2]

		domain_left = set1.getDomain()
		domain_right = set2.getDomain()
		subdomain_left = set1.getDomain().getDomains()
		subdomain_right = set2.getDomain().getDomains()
		# binary relations
		if len(subdomain_left) == 2 and len(subdomain_right) == 2:

			status = self.checkBinaryRelationCompatibility(subdomain_left, subdomain_right)
			if status == False:
				print ("ERROR. Domains " + str(domain_left) + " and " + str(domain_right) + "are not compatible for composition.")
				return

			self.generateBinaryRelationFromBinary(name, method, set1, set2, subdomain_left, subdomain_right, sets)

		# general case	
		else:

			self.generateRelation(name, method, set1, set2, domain_left, domain_right, subdomain_left, subdomain_right, sets)

	def checkBinaryRelationCompatibility(self, domain_left, domain_right):

		if not domain_left[1] == domain_right[1]:
			return False

		return True

	def generateBinaryRelationFromBinary(self, name, method, set_left, set_right, subdomain_left, subdomain_right, sets):

		common_domain = subdomain_left[1]
		left = subdomain_left[0]
		right = subdomain_right[1]

		definition = []
		definition.append(left)
		definition.append(right)
		new_domain = DomainCartesian("temp", definition, "cartesian")

		memberships = [None] * new_domain.getCardinality()

		for x in left.getElements():
			for z in right.getElements():

				max_ = 0
				for y in common_domain.getElements():

					min_ = 0 
					if method == "'max-min'":
						min_ = min(set_left.getMembershipFor((x,y)), set_right.getMembershipFor((y, z)))
					elif method == "'max-product'":
						min_ = set_left.getMembershipFor((x,y)) * set_right.getMembershipFor((y, z))

					if min_ > max_:
						max_ = min_

				memberships[new_domain.getIndexOfElement((x, z))] = max_

		s = FuzzySet(name, new_domain, memberships)
		sets[name] = s


	def generateRelation(self, name, method, set_left, set_right, domain_left, domain_right, subdomain_left, subdomain_right, sets):

		common_domain = []
		left = []
		right = []

		self.findIntersectionOfDomains(subdomain_left, subdomain_right, left, common_domain, right)

		if len(common_domain) == 0:
			print ("ERROR. Domains " + str(domain_left) + " " + str(domain_right) + " are not compatible.")
			return

		# print "here"
		# first case
		if len(left) == 0:

			self.createRelationDefinedOnRight(name, method, set_left, set_right, right, common_domain, sets)

		elif len(right) == 0:

			self.createRelationDefinedOnLeft(name, method, set_left, set_right, left, common_domain, sets)


		else:

			self.createGeneralRelation(name, method, set_left, set_right, left, right, common_domain, sets)


	def findIntersectionOfDomains(self, left, right, left_out, intersection_out, right_out):

		i = 0
		j = 0

		while i < len(left) and j < len(right):

			if left[i] == right[j]:

				intersection_out.append(left[i])
				i += 1
				j += 1

			else:

				left_out.append(left[i])
				i += 1

		while j < len(right):
			right_out.append(right[j])
			j += 1

	def createGeneralRelation(self, name, method, set_left, set_right, left, right, common_domain, sets):

		leftDomain = DomainCartesian("temp", left, "cartesian")
		rightDomain = DomainCartesian("temp", right, "cartesian")
		commonDomain = DomainCartesian("temp", common_domain, "cartesian")

		new_definition = left + right
		newDomain = DomainCartesian("temp", new_definition, "cartesian")

		memberships = [None] * newDomain.getCardinality()

		for x in leftDomain.getElements():
			for z in rightDomain.getElements():
				max_ = 0

				for y in commonDomain.getElements():

					min_ = 0
					if method == "'max-min'":
						min_ = min(set_left.getMembershipFor(x + y), set_right.getMembershipFor(y + z))

					elif method == "'max-product'":
						min_ = set_left.getMembershipFor(x + y) * set_right.getMembershipFor(y + z)

					if min_ > max_:
						max_ = min_

				memberships[newDomain.getIndexOfElement(x + z)] = max_

		# print name
		s = FuzzySet(name, newDomain, memberships)
		sets[name] = s

	def createRelationDefinedOnRight(self, name, method, set_left, set_right, right, common_domain, sets):

		rightDomain = DomainCartesian("temp", right, "cartesian")
		commonDomain = DomainCartesian("temp", common_domain, "cartesian")

		new_definition = right
		newDomain = DomainCartesian("temp", new_definition, "cartesian")

		memberships = [None] * newDomain.getCardinality()

		for z in rightDomain.getElements():
			max_ = 0

			for y in commonDomain.getElements():

				min_ = 0
				if method == "'max-min'":
					min_ = min(set_left.getMembershipFor(y), set_right.getMembershipFor(y + z))

				elif method == "'max-product'":
					min_ = set_left.getMembershipFor(y) * set_right.getMembershipFor(y + z)

				if min_ > max_:
					max_ = min_

			memberships[newDomain.getIndexOfElement(z)] = max_

		# print name
		s = FuzzySet(name, newDomain, memberships)
		sets[name] = s

	def createRelationDefinedOnLeft(self, name, method, set_left, set_right, left, common_domain, sets):

		leftDomain = DomainCartesian("temp", left, "cartesian")
		commonDomain = DomainCartesian("temp", common_domain, "cartesian")

		new_definition = left
		newDomain = DomainCartesian("temp", new_definition, "cartesian")

		memberships = [None] * newDomain.getCardinality()

		for x in leftDomain.getElements():

			max_ = 0
			for y in commonDomain.getElements():

				min_ = 0
				if method == "'max-min'":
					min_ = min(set_left.getMembershipFor(x + y), set_right.getMembershipFor(y))

				elif method == "'max-product'":
					min_ = set_left.getMembershipFor(x + y) * set_right.getMembershipFor(y)

				if min_ > max_:
					max_ = min_

			memberships[newDomain.getIndexOfElement(x)] = max_

		s = FuzzySet(name, newDomain, memberships)
		sets[name] = s
