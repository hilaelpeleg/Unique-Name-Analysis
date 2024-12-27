import unittest
from uniqueNameCounter import countUniqueNames

class TestNameFunctions(unittest.TestCase):
    def test_empty_input(self):
        with self.assertRaises(ValueError) as context:
            countUniqueNames("", "Egli", "Deborah", "Egli", "Deborah Egli")
        self.assertEqual(str(context.exception), "All inputs must be non-empty strings.")

    def test_identical_names(self):
        result = countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_levenshteinDistance(self):
        result = countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_names_with_similar_last_name(self):
        result = countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_different_names(self):
        result = countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli")
        self.assertEqual(result, 2)  # Expected result is 2

    def test_names_with_surname_variation(self):
        result = countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_hamming_distance(self):
        result = countUniqueNames("Deborph", "Eglo", "Deborah", "Egli", "Deborah Egli")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_last_name_length_2(self):
        result = countUniqueNames("hila", "El peleg", "hila", "el peleg", "hila el deleg")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_last_name_length_3(self):
        result = countUniqueNames("hila", "El peleg ex", "hila", "el peleg ex", "hila el deleg ex")
        self.assertEqual(result, 1)  # Expected result is 1

    def test_last_name_length_1(self):
        result = countUniqueNames("hila", "peleg", "hila", "peleg", "hila deleg")
        self.assertEqual(result, 1)  # Expected result is 1

if __name__ == '__main__':
    unittest.main()