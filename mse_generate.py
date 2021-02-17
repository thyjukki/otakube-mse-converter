import os
import shutil
from PIL import Image
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
		full_text += card.generate_mse_card(len(cards))
	with open('mse_footer.txt', 'r', encoding='UTF-8') as read_obj:
		full_text += "\n" + read_obj.read()
	return full_text


def run():
	cards = parse_list('otakube.csv')

	output = generate_mse_set(cards)
	if not os.path.exists('build'):
		os.makedirs('build')
	with open('build/set', 'w', encoding='UTF-8') as file:
		file.write(output)
	
	if os.path.exists('otakube.mse-set'):
		os.remove('otakube.mse-set')
	shutil.make_archive('otakube', 'zip', 'build')
	os.rename('otakube.zip', 'otakube.mse-set')

	if os.path.exists('custom.deck'):
		os.remove('custom.deck')

	
	if os.path.exists('export'):
		shutil.rmtree('./export', ignore_errors=True)
		
	#os.makedirs('export')
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.system(f".\MSE\mse  --export otakube.mse-set \"{dir_path}\\export\\{{card.notes}}.jpg\"")
	with open('custom.deck', 'w', encoding='UTF-8') as file:
		file.write("Custom\n")
		for card in cards:
			file.write(f"1 {card.safe_name}.jpg\n")
	generate_sheets(cards)
	
	
def generate_sheets(cards: List[Card]):
	if os.path.exists('sheets'):
		shutil.rmtree('./sheets', ignore_errors=True)
		
	os.makedirs('sheets')

	card_width = 375
	card_height = 523
	index = 0
	sheet = 0
	while index < len(cards):
		new_im = Image.new('RGB', (card_width*10,card_height*7))
		for j in range (7):
			if index >= len(cards):
				break
			for i in range (10):
				if index >= len(cards):# or (i== 9 and j == 6):
					break

				card = cards[index]
				im = Image.open(f"export/{card.safe_name}.jpg")
				if card.name2:
					im = im.rotate(90, expand=True)
					im.save(f"export/{card.safe_name}.jpg")

				new_im.paste(im, (i*card_width,j*card_height))
				index += 1
		new_im.save(f"./sheets/otakube_{sheet}.jpg")
		sheet += 1
		

if __name__ == '__main__':
	run()