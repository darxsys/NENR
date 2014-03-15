import sys

EPSILON = 1e-5

def gamma(x, alpha, beta):

	if x < alpha:
		return 0
	elif x >= beta:
		return 1
	else:
		return (x - alpha) / float(beta - alpha)

def lambdaF(x, alpha, beta, gamma):

	if x < alpha:
		return 0
	elif x >= gamma:
		return 0
	elif x >= alpha and x < beta:
		return (x - alpha) / float(beta - alpha)
	else:
		return (gamma - x) / float(gamma - beta)

def functionL(x, alpha, beta):

	if x < alpha:
		return 1
	elif x >= beta:
		return 0
	else:
		return (beta - x) / float(beta - alpha)

def functionPi(x, alpha, beta, gamma, delta):

	if x < alpha:
		return 0
	elif x >= beta and x < gamma:
		return 1
	elif x >= delta:
		return 0
	elif x >= alpha and x < beta:
		return (x - alpha) / float(beta - alpha)
	else:
		return (delta - x) / float(delta - gamma)

def isInt(s):

    try:
        int(s)
        return True
    except:
        return False


def isSubset(set_, subset):

	if not type(subset) == tuple:
		if subset[0] in set_:
			return True
		return False

	if len(subset) > len(set_):
		return False

	i = 0
	j = 0

	while i < len(set_) and j < len(subset):

		if type(set_[i]) == float:
			if abs(set_[i] - subset[j]) < EPSILON:
				j += 1

		elif set_[i] == subset[j]:
			j += 1

		i += 1

	if j == len(subset):
		return True

	return False