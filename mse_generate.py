import os
import shutil
from PIL import Image
from csv import reader
from typing import List
from card import Card
import subprocess
import requests


def parse_list(file):
	# open file in read mode
	with open(file, 'r', encoding='UTF-8') as read_obj:
		csv_reader = reader(read_obj)
		next(csv_reader)
		next(csv_reader)
		cards = [Card(row) for row in csv_reader]

		sorted_cards = sorted(cards, key= lambda e:e.id)

		return sorted_cards


def generate_mse_set(cards: List[Card], name: str):
	with open('mse_header.txt', 'r', encoding='UTF-8') as read_obj:
		full_text = read_obj.read()

	for card in cards:
		full_text += card.generate_mse_card(len(cards))

		if card.img_url:
			print(card.img_url)
			response = requests.get(card.img_url, stream=True)

			with open(f"build_{name}/{card.img_name}", 'wb') as output:
				for block in response.iter_content(1024):
					if not block:
						break

					output.write(block)
				output.close()

		if card.img_url2:
			print(card.img_url2)
			response = requests.get(card.img_url2, stream=True)

			with open(f"build_{name}/{card.img_name2}", 'wb') as output:
				for block in response.iter_content(1024):
					if not block:
						break
						
					output.write(block)
				output.close()

	with open('mse_footer.txt', 'r', encoding='UTF-8') as read_obj:
		full_text += "\n" + read_obj.read()
	return full_text


def run(name):
	cards = parse_list(f"{name}.csv")

	if not os.path.exists(f"build_{name}"):
		os.makedirs(f"build_{name}")

	output = generate_mse_set(cards, name)

	with open(f"build_{name}/set", 'w', encoding='UTF-8') as file:
		file.write(output)
	
	if os.path.exists(f"{name}.mse-set"):
		os.remove(f"{name}.mse-set")
	shutil.copy('otakube.mse-symbol', f"build_{name}/otakube.mse-symbol")
	shutil.make_archive(name, 'zip', f"build_{name}")
	os.rename(f"{name}.zip", f"{name}.mse-set")

	if os.path.exists('custom.deck'):
		os.remove('custom.deck')

	
	if os.path.exists(f"export_{name}"):
		shutil.rmtree(f"./export_{name}", ignore_errors=True)
		
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.system(f".\MSE\mse  --export {name}.mse-set \"{dir_path}\\export_{name}\\{{card.notes}}.jpg\"")
	with open('custom.deck', 'w', encoding='UTF-8') as file:
		file.write("Custom\n")
		for card in cards:
			file.write(f"1 {card.safe_name}.jpg\n")
	generate_sheets(cards, name)
	
	
def generate_sheets(cards: List[Card], name):
	if os.path.exists(f"sheets_{name}"):
		shutil.rmtree(f"./sheets_{name}", ignore_errors=True)
		
	os.makedirs(f"sheets_{name}")

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
				im = Image.open(f"export_{name}/{card.safe_name}.jpg")
				if card.name2:
					im = im.rotate(90, expand=True)
					im.save(f"export_{name}/{card.safe_name}.jpg")

				new_im.paste(im, (i*card_width,j*card_height))
				index += 1
		new_im.save(f"./sheets_{name}/{name}_{sheet}.jpg")
		sheet += 1



if __name__ == '__main__':
	run('otakube')
	run('otakube_tokens')

	if os.path.exists('upload.py'):
		subprocess.call(["python", "upload.py"])