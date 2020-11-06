__author__ = 'cs540-testers'
__credits__ = ['Harrison Clark', 'Stephen Jasina', 'Saurabh Kulkarni',
		'Alex Moon']
version = 'v0.1'

import unittest
import numpy as np
import scipy.cluster.hierarchy
from pokemon_stats import load_data, calculate_x_y, hac

tiebreak_csv_file = 'Tiebreak_Test.csv'
random_csv_file = 'Random_Test.csv'

class TestLoadData(unittest.TestCase):
	def test_load(self):
		pokemon = load_data(random_csv_file)

		# We should have a list
		self.assertIsInstance(pokemon, list)

		# The elements of the list should be dictionaries
		for element in pokemon:
			self.assertIsInstance(element, dict)

		# We should load exactly 20 pokemon
		self.assertEqual(len(pokemon), 20)

		# Check row 13 to make sure it contains what we expect
		row = pokemon[13]
		expected_row = {
			'#': 14,
			'Name': 'name_14',
			'Type 1': 'type_a_14',
			'Type 2': '',
			'Total': 687,
			'HP': 191,
			'Attack': 2,
			'Defense': 181,
			'Sp. Atk': 12,
			'Sp. Def': 108,
			'Speed': 193
		}

		# Check that expected_row is contained in row
		for k, v in expected_row.items():
			self.assertIn(k, row)
			self.assertIsInstance(row[k], type(v))
			self.assertEqual(row[k], v)

		# Check that row contains no extra keys
		for k in row:
			self.assertIn(k, expected_row)

def get_x_y_pairs(csv_file):
	'''
	Take in a csv file name and return a list of (x, y) pairs corresponding to
	the csv file's pokemon
	'''
	return [calculate_x_y(stats) for stats in load_data(csv_file)]

class TestCalculateXY(unittest.TestCase):
	def test_calculate_xy(self):
		x_y_pairs = get_x_y_pairs(random_csv_file)
		expected_x_y_pairs = [(318, 172), (197, 165), (256, 276), (243, 300),
				(272, 256), (125, 403), (280, 362), (374, 85), (326, 554),
				(296, 115), (334, 380), (336, 436), (270, 425), (207, 480),
				(347, 401), (186, 305), (267, 304), (396, 184), (469, 518),
				(414, 223)] # I'm sorry this is ugly
		for x_y_pair, expected_x_y_pair in zip(x_y_pairs, expected_x_y_pairs):
			self.assertEqual(x_y_pair, expected_x_y_pair)


class TestHAC(unittest.TestCase):
	def test_randomized(self):
		x_y_pairs = get_x_y_pairs(random_csv_file)

		computed = hac(x_y_pairs)

		# hac should return an numpy array of the right shape
		self.assertIsInstance(computed, np.ndarray)
		self.assertEqual(np.shape(computed), (19, 4))

		# The third column should be increasing
		for i in range(18):
			self.assertGreaterEqual(computed[i + 1, 2], computed[i, 2])

		# Verify hac operates exactly as linkage does
		expected = scipy.cluster.hierarchy.linkage(x_y_pairs)
		self.assertTrue(np.all(np.isclose(computed, expected)))

	def test_tiebreak(self):
		x_y_pairs = get_x_y_pairs(tiebreak_csv_file)
		computed = hac(x_y_pairs)
		expected_cluster_sizes \
				= [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 8, 8, 12, 20]
		for i, row in enumerate(computed):
			self.assertEqual(row[0], 2 * i)
			self.assertEqual(row[1], 2 * i + 1)
			self.assertEqual(row[2], 0)
			self.assertEqual(row[3], expected_cluster_sizes[i])


if __name__ == '__main__':
	print('Homework 7 Tester Version', version)

	unittest.main()
