'''
Generate a random .csv file of "Pokemon," as well as a very bland file for
testing tiebreaking
'''

import csv
import random
from pokemon_stats import calculate_x_y

def generate_random_data():
	rows = []
	for i in range(1, 41):
		scores = [random.randrange(200) for _ in range(6)]
		rows.append([
			str(i),
			'name_' + str(i),
			'type_a_' + str(i),
			'type_b_' + str(i) if random.choice([False, True]) else '',
			sum(scores)
		] + [str(score) for score in scores] + [
			random.randrange(1, 8),
			random.choice([False, True])
		])


	with open('Random_Test.csv', 'w') as csv_file:
		csv_file.write('#,Name,Type 1,Type 2,Total,HP,Attack,Defense,Sp. Atk,Sp. Def,Speed,Generation,Legendary\n')
		csv.writer(csv_file).writerows(rows)

def generate_tiebreak_data():
	with open('Tiebreak_Test.csv', 'w') as csv_file:
		csv_file.write('#,Name,Type 1,Type 2,Total,HP,Attack,Defense,Sp. Atk,Sp. Def,Speed,Generation,Legendary\n')
		writer = csv.writer(csv_file)
		for i in range(1, 21):
			writer.writerow([
				str(i),
				'name_' + str(i),
				'type_a_' + str(i),
				'type_b_' + str(i),
			] + [0] * 7 + [
				random.randrange(1, 8),
				random.choice([False, True])
			])

if __name__ == '__main__':
	generate_random_data()
	generate_tiebreak_data()
