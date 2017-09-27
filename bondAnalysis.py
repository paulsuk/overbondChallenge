from enum import Enum
import sys
import pdb

class BondType(Enum):
	'''
	Enum used for distinguishing types of bonds
	'''
	government = 1
	corporate = 2

class Bond(object):
	'''
	Properties:
	name: String, identifier for bond, e.g 'C1'
	bondType: value of enum: BondType that classifies the type of bond
	term: double that indicates the length of the term
	yld: double that indicates the percent yield of the bond

	Methods:
	__init__(): initializes the object, using the inputs from stdin
	'''

	def __init__(self, name, bondType, term, yld):
		'''
		Initializes bond object:
		param - name: String, identifier for bond, e.g 'C1'
		param - bondType: value of enum: BondType that classifies the type of bond
		param - term: double that indicates the length of the term
		param - yld: double that indicates the percent yield of the bond
		'''
		self.name = name
		self.type = bondType
		self.term = term
		self.yld = yld

	def compareToBenchmark(self, bonds):
		'''
		Finds the closest benchmark bond (by term length) and retruns the spread to benchmark

		param - bonds: array of Bond() objects that we are comparing to

		Returns:
		benchmark, spread_to_benchmark
			benchmark: String that is the name of the benchmark bond
			spread_to_benchmark: float that represents the spread to benchmark bond
		'''

		benchmark = self._findClosest(bonds)
		spread = self.yld - benchmark.yld

		return benchmark.name, spread

	def spreadToCurve(self, bonds):
		'''
		Calculates the spread to a bond curve, given a list of bonds to compare to.
			Uses linear interpolation to determine the spread to the curve

		param - bonds: list of Bond objects used to calculate the yield curve to compare to

		Returns: spreadToCurve, a float that represents the spread to the yield curve
		'''

		closestLower, closestUpper = self._findClosestNeighbours(bonds)

		#Error checking to see if lower and upper bounds exist for current bond
		#	In the problem statement, says we can assume that it exists, but put in 
		#	just in case

		if (closestLower is None or closestUpper is None):
			raise Exception("Cannot calculate spread to curve, no benchmark that is lower/higher term than bond")

		yldAtCurve = self._interpolate(closestLower, closestUpper)
		return self.yld - yldAtCurve

	def _findClosest(self, bonds):
		'''
		Finds the closest bond (in term) from a list of bonds, calls _findClosestNeighbours()

		param - bonds: array of Bond() objects that we are comparing to

		Returns:
		Bond() object that is the closest bond (in term) from the list to the bond
		'''
		closestLower, closestUpper = self._findClosestNeighbours(bonds)

		# edge cases if the current bond is the longest or shortest term bond
		if closestUpper is None:
			return closestLower
		if closestLower is None:
			return closestUpper

		if closestUpper.term - self.term > self.term - closestLower.term:
			return closestLower
		else:
			return closestUpper


	def _findClosestNeighbours(self, bonds):
		'''
		Finds the bonds from a list that is the closest neighbours for term length,

		param - bonds: array of Bond() objects

		Returns:
		closestLower, closestUpper: Bond objects that are the closest upper and lower bounds from the 
			input list
		'''

		# sort keys
		bonds.sort(key=lambda x: x.term)

		closestLower = None
		closestUpper = None

		for bond in bonds:
			if self.term > bond.term:
				closestLower = bond
			# stop when reaching first bond that is longer in term
			else:
				closestUpper = bond
				break

		return closestLower, closestUpper

	def _interpolate(self, lower, upper):
		'''
		Uses linear interpolation to determine the yield on the curve at 
			the term of the current bond

		Solving the equation (y2-y1)/(t2-t1) = (yd - y1)/(td_t1)
			where y2,y1 are yields of upper,lower
			t2,t1 are terms of upper,lower
			td is term of current bond
			yd is the yield at current term on the curve

		param - lower, upper: Bond() objects that are used as the lower and upper 
			limits to determine the curve

		Returns: 
			yield_at_curve: float that is the interpolated yield at curve
		'''

		y2 = upper.yld
		y1 = lower.yld
		t2 = upper.term
		t1 = lower.term
		td = self.term

		return ((y2 - y1) * (td - t1) / (t2 - t1)) + y1

def processInput(filename):
	'''
	Parses input file and outputs two arrays, one containing all of the 
		government bonds and one containing all of the corporate bonds
	
	param - filename: String of the filename for input file
	Note: we expect the data to be in csv format, with the attributes in order
	bond,type,term,yield 

	Returns gov, corp
	gov: array of Bond objects
	corp: array of Bond objects
	'''

	INPUT_FORMAT = ['bond', 'type', 'term', 'yield']
	gov = []
	corp = []

	with open(filename, 'r') as file:
		# validate the format of the data is what we expect
		line = file.readline().strip().split(',')
		if line != INPUT_FORMAT:
			raise Exception("Unexpected Input Format")

		for line in file:
			#Parse the line of the input file
			line = line.strip().split(',')
			name = line[0]
			bondType = BondType[line[1]]
			#term is in format of 'x years'
			term = float(line[2].split()[0])
			#yield is in format of 'x%'
			yld = float(line[3].strip('%'))

			#instantiate Bond object
			bond = Bond(name, bondType, term, yld)

			if(bond.type == BondType.government):
				gov.append(bond)
			else:
				corp.append(bond)

	return gov, corp

def challenge1(inputFile):
	'''
	Method that calculates the spread to benchmark for all corporate bonds in 
		a given inputFile

	param - inputFile: String, filename of the desired inputFile, expected to be a csv

	Prints the result to console
	'''

	gov, corp = processInput(inputFile)
	print("bond,benchmark,spread_to_benchmark")
	for bond in corp:
		benchmark, spread = bond.compareToBenchmark(gov)
		print("{},{},{:.2f}%".format(bond.name, benchmark, spread))

def challenge2(inputFile):
	'''
	Method that calculates the spread to curve for all corporate bonds in 
		a given inputFile

	param - inputFile: String, filename of the desired inputFile, expected to be a csv

	Prints the result to console
	'''

	gov, corp = processInput(inputFile)
	print("bond,spread_to_curve")
	for bond in corp:
		spread = bond.spreadToCurve(gov)
		print("{},{:.2f}%".format(bond.name, spread))

if __name__ == "__main__":
	assert sys.version_info >= (3,4), "Please run this program with a Python version of 3.4 or more recent. You are using {}".format(sys.version)
	try: 
		if len(sys.argv) < 3:
			raise InputError("Please indicate an input file name, and challenge number (1 or 2)\n" + 
				"e.g python3 inputfilename.csv 2")
		elif len(sys.argv) >3:
			raise InputError("too many arguments\n" + 
				"e.g python3 inputfilename.csv 2")
		else:
			filename = sys.argv[1]
			try:
				challengeNum = int(sys.argv[2])
				if challengeNum == 1:
					print("Solving challenge 1: spread to benchmark")
					challenge1(filename)
				elif challengeNum == 2:
					print("Solving challenge 2: spread to curve")
					challenge2(filename)
				else:
					raise ValueError("Challenge number should be 1 or 2")

			except ValueError as e:
				print(e)
				print("Please enter a valid number for the challenge number")
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
