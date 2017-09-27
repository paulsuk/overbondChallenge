import bondAnalysis
import pdb
import unittest

'''
Testsuite:
uses testfile: test.csv and invalid_format.csv


'''

class TestProcessInput(unittest.TestCase):
	def testWithFile(self):
		gov, corp = bondAnalysis.processInput('testFiles/test.csv')
		expectedGov = [bondAnalysis.Bond('G1', bondAnalysis.BondType.government, 1.0, 1.0),
			bondAnalysis.Bond('G2', bondAnalysis.BondType.government, 4.0, 4.0),
			bondAnalysis.Bond('G3', bondAnalysis.BondType.government, 5.0, 5.0),
			bondAnalysis.Bond('G4', bondAnalysis.BondType.government, 10.0, 10.0)]

		expectedCorp = [bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 3.0, 5.0),
			bondAnalysis.Bond('C2', bondAnalysis.BondType.corporate, 4.0, 7.0),
			bondAnalysis.Bond('C3', bondAnalysis.BondType.corporate, 7.0, 12.0)]

		self.assertEqual(gov, expectedGov)
		self.assertEqual(corp, expectedCorp)

	def testInvalidFormat(self):
		with self.assertRaises(Exception):
			gov, corp = bondAnalysis.processInput('testFiles/invalid_format.csv')

class TestBondClass(unittest.TestCase):	

	def testInitInvalidArgs(self):
		validName = "C1"
		validType = bondAnalysis.BondType.corporate
		validTerm = 1.0
		validYld = 1.0
		with self.assertRaises(AssertionError):
			bond = bondAnalysis.Bond(1, validType, validTerm, validYld)
		with self.assertRaises(AssertionError):
			bond = bondAnalysis.Bond(validName, "invalid", validTerm, validYld)
		with self.assertRaises(AssertionError):
			bond = bondAnalysis.Bond(validName, validType, "invalid", validYld)
		with self.assertRaises(AssertionError):
			bond = bondAnalysis.Bond(validName, validType, validTerm, "invalid")

	def testEq(self):
		name = "C1"
		term = 1.0
		yld = 1.0
		bondA = bondAnalysis.Bond(name, bondAnalysis.BondType.corporate, term, yld)
		bondB = bondAnalysis.Bond(name, bondAnalysis.BondType.corporate, term, yld)
		bondC = bondAnalysis.Bond(name, bondAnalysis.BondType.government, term, yld)
		bondD = bondAnalysis.Bond("G1", bondAnalysis.BondType.corporate, term, yld)
		bondE = bondAnalysis.Bond(name, bondAnalysis.BondType.corporate, 2.0, yld)
		bondF = bondAnalysis.Bond(name, bondAnalysis.BondType.corporate, term, 2.0)

		self.assertTrue(bondA == bondB)
		self.assertFalse(bondA == bondC)
		self.assertFalse(bondA == bondD)
		self.assertFalse(bondA == bondE)
		self.assertFalse(bondA == bondF)

	def testCompareToBenchmark(self):
		'''
		Uses the example given in:
		https://gist.github.com/kseyon/fdb3ede4fadc2559c74fcdbe32ccf613#file-sample_input-csv
		'''
		gov, corp = bondAnalysis.processInput('testFiles/example1.csv')
		name, spread = corp[0].compareToBenchmark(gov)

		self.assertEqual(name, "G1")
		self.assertEqual(round(spread, 2), 1.60)

	def testSpreadToCurve(self):
		'''
		Uses the example given in:
		https://gist.github.com/kseyon/fdb3ede4fadc2559c74fcdbe32ccf613#file-sample_input-csv
		'''
		gov, corp = bondAnalysis.processInput('testFiles/example2.csv')

		c1 = corp[0]
		c2 = corp[1]

		y1 = round(c1.spreadToCurve(gov), 2)
		y2 = round(c2.spreadToCurve(gov), 2)

		self.assertEqual(y1, 1.22)
		self.assertEqual(y2, 2.98)

	def testFindClosest(self):
		bonds = [bondAnalysis.Bond('G1', bondAnalysis.BondType.government, 1.0, 1.0),
			bondAnalysis.Bond('G2', bondAnalysis.BondType.government, 4.0, 4.0),
			bondAnalysis.Bond('G3', bondAnalysis.BondType.government, 5.0, 5.0),
			bondAnalysis.Bond('G4', bondAnalysis.BondType.government, 10.0, 10.0)]

		#standard case
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 7.0, 8.0)
		expected = bonds[2]
		actual = test._findClosest(bonds)
		self.assertEqual(expected, actual)

		# only a lower neighbour exists
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 11.0, 8.0)
		expected = bonds[3]
		actual = test._findClosest(bonds)
		self.assertEqual(expected, actual)

		# only a higher neighbour exists
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 0.5, 8.0)
		expected = bonds[0]
		actual = test._findClosest(bonds)
		self.assertEqual(expected, actual)

	def testFindClosestNeighbours(self):
		bonds = [bondAnalysis.Bond('G1', bondAnalysis.BondType.government, 1.0, 1.0),
			bondAnalysis.Bond('G2', bondAnalysis.BondType.government, 4.0, 4.0),
			bondAnalysis.Bond('G3', bondAnalysis.BondType.government, 5.0, 5.0),
			bondAnalysis.Bond('G4', bondAnalysis.BondType.government, 10.0, 10.0)]

		#standard case
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 7.0, 8.0)
		expectedLower, expectedHigher = bonds[2], bonds[3]
		actualLower, actualHigher = test._findClosestNeighbours(bonds)
		self.assertEqual(expectedLower, actualLower)
		self.assertEqual(expectedHigher, actualHigher)

		# only a lower neighbour exists
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 11.0, 8.0)
		expectedLower, _ = bonds[3], None
		actualLower, actualHigher = test._findClosestNeighbours(bonds)
		self.assertEqual(expectedLower, actualLower)
		self.assertIsNone(actualHigher)

		# only a higher neighbour exists
		test = bondAnalysis.Bond('C1', bondAnalysis.BondType.corporate, 0.5, 8.0)
		_, expectedHigher = None, bonds[0]
		actualLower, actualHigher = test._findClosestNeighbours(bonds)
		self.assertIsNone(actualLower)
		self.assertEqual(expectedHigher, actualHigher)

	def test_interpolate(self):
		testBond = bondAnalysis.Bond("test", bondAnalysis.BondType.corporate, 2.0, 3.0)

		lowerBond = bondAnalysis.Bond("test", bondAnalysis.BondType.government, 1.0, 1.0)
		upperBond = bondAnalysis.Bond("test", bondAnalysis.BondType.government, 3.0, 3.0)

		expected = 2.0
		actual = testBond._interpolate(lowerBond, upperBond)

		self.assertEqual(expected, actual)

if __name__ == "__main__":
	unittest.main()