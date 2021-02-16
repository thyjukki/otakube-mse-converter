import os
import shutil
from csv import reader
from typing import List
from card import Card


def parse_list(file):
	# open file in read mode
	with open(file, 'r', encoding='UTF-8') as read_obj:
		csv_reader = reader(read_obj)
		next(csv_reader)
		next(csv_reader)
		cards = [Card(row) for row in csv_reader]

		sorted_cards = sorted(cards, key= lambda e:e.id)

		return sorted_cards


def generate_mse_set(cards: List[Card]):
	with open('mse_header.txt', 'r', encoding='UTF-8') as read_obj:
		full_text = read_obj.read()

	for card in cards:
		full_text += card.generate_mse_card()
	return full_text


def run():
	cards = parse_list('otakube.csv')

	output = generate_mse_set(cards)
	if not os.path.exists('build'):
		os.makedirs('build')
	with open('build/set', 'w', encoding='UTF-8') as file:
		file.write(output)
	
	os.remove('otakube.mse-set')
	shutil.make_archive('otakube', 'zip', 'build')
	os.rename('otakube.zip', 'otakube.mse-set')

if __name__ == '__main__':
	run()