import os
import shutil
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread
from gspread import Worksheet
from typing import List
from card import Card
import subprocess
import requests
import argparse
import csv
from PIL import Image, ImageFont, ImageDraw

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '11U38EPYmtDRnwzh8r9bb0rHfFL3dBzYSA-WNP0Lgxdo'
SPREADSHEET_SHEET = 'Alpha 1.2'
SPREADSHEET_SHEET_TOKEN = 'A1.0.e EXTRA TOKENS'


def parse_list_gs(sheet: Worksheet):
	cards = []
	for row in sheet.get_all_values():
		if row[0] and row[0] != 'ID' and row[2]:
			cards.append(Card(row))

	sorted_cards = sorted(cards, key=lambda e: e.id)
	return sorted_cards


def parse_list_csv(file):
	cards = []
	csvreader = csv.reader(file)
	for row in csvreader:
		if row[0] and row[0] != 'ID' and row[2]:
			cards.append(Card(row))

	sorted_cards = sorted(cards, key=lambda e: e.id)
	return sorted_cards


def build_cred():
	cred = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			cred = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			cred = flow.run_local_server(port=0, success_message='test')
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(cred, token)
	return cred


def generate_mse_set(cards: List[Card], name: str):
	with open('mse_header.txt', 'r', encoding='UTF-8') as read_obj:
		full_text = read_obj.read()

	for card in cards:
		full_text += card.generate_mse_card(len(cards))

		if card.img_url:
			get_img(card.img_url, card.img_name, name)
		elif not os.path.isfile(f"build_{name}/{card.id}_{card.safe_name}_tmp.jpg"):
			name_split = card.name.split()[0].replace(',', '').replace('-', '')
			get_img(f"https://loremflickr.com/311/228/{name_split}", f"{card.id}_{card.safe_name}_tmp", name)
			img = Image.open(f"build_{name}/{card.id}_{card.safe_name}_tmp")
			font = ImageFont.truetype("BebasNeue-Bold.ttf", 40, encoding="unic")
			image_editable = ImageDraw.Draw(img)
			w_img, h_img = (311, 228)
			w, h = font.getsize("PLACEHOLDER")
			image_editable.text(((w_img-w)/2, (h_img-h)/2), "PLACEHOLDER", (245, 66, 66, 155), font)
			img.save(f"build_{name}/{card.id}_{card.safe_name}_tmp.jpg")

		if card.img_url2:
			get_img(card.img_url2, card.img_name2, name)

	with open('mse_footer.txt', 'r', encoding='UTF-8') as read_obj:
		full_text += "\n" + read_obj.read()
	return full_text


def get_img(img_url, img_name, name):
	print(img_url)
	response = requests.get(img_url, stream=True, allow_redirects=True)
	with open(f"build_{name}/{img_name}", 'wb') as output:
		for block in response.iter_content(1024):
			if not block:
				break

			output.write(block)
		output.close()


def run(name, cards: List[Card], printable: bool):
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

	if os.path.exists(f"export_{name}"):
		shutil.rmtree(f"./export_{name}", ignore_errors=True)

	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.system(f".\\MSE\\mse  --export {name}.mse-set \"{dir_path}\\export_{name}\\{{card.notes}}.jpg\"")

	if printable:
		generate_a4_sheets(cards, name)
	else:
		generate_tts_sheets(cards, name)


def generate_tts_sheets(cards: List[Card], name):
	if os.path.exists(f"sheets_{name}"):
		shutil.rmtree(f"./sheets_{name}", ignore_errors=True)

	os.makedirs(f"sheets_{name}")

	card_width = 375
	card_height = 523
	index = 0
	sheet = 0
	while index < len(cards):
		new_im = Image.new('RGB', (card_width * 10, card_height * 7))
		for j in range(7):
			if index >= len(cards):
				break
			for i in range(10):
				if index >= len(cards):  # or (i== 9 and j == 6):
					break

				card = cards[index]
				im = Image.open(f"export_{name}/{card.safe_name}.jpg")
				if card.name2:
					im = im.rotate(90, expand=True)
					im.save(f"export_{name}/{card.safe_name}.jpg")

				new_im.paste(im, (i * card_width, j * card_height))
				index += 1
		new_im.save(f"./sheets_{name}/{name}_{sheet}.jpg")
		sheet += 1


def generate_a4_sheets(cards: List[Card], name):
	if os.path.exists(f"sheets_{name}"):
		shutil.rmtree(f"./sheets_{name}", ignore_errors=True)

	os.makedirs(f"sheets_{name}")

	card_width = 375
	card_height = 523
	index = 0
	sheet = 0
	while index < len(cards):
		new_im = Image.new('RGB', (card_width * 3, card_height * 3))
		for j in range(3):
			if index >= len(cards):
				break
			for i in range(3):
				if index >= len(cards):  # or (i== 9 and j == 6):
					break

				card = cards[index]
				im = Image.open(f"export_{name}/{card.safe_name}.jpg")
				if card.name2:
					im = im.rotate(90, expand=True)
					im.save(f"export_{name}/{card.safe_name}.jpg")

				new_im.paste(im, (i * card_width, j * card_height))
				index += 1
		new_im.save(f"./sheets_{name}/{name}_{sheet}.jpg")
		sheet += 1


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-P", "--print", help="A4 printable sheet", action="store_true")
	parser.add_argument("-T", "--tokens", help="Generate token sheet", action="store_true")
	parser.add_argument("-U", "--upload", help="Upload using upload.py", action="store_true")
	parser.add_argument("-CF", "--csv_file", help="Path to csv file", type=str)

	# Read arguments from the command line
	args = parser.parse_args()

	cards = None
	token_cards = None
	if args.csv_file:
		with open(args.csv_file, 'r', encoding='utf-8') as file:
			cards = parse_list_csv(file)
	else:
		if not os.path.exists('credentials.json'):
			raise Exception(
				"credentials.json not found, guide for generating : https://developers.google.com/sheets/api/quickstart/python")
		gc = gspread.authorize(build_cred())
		sh = gc.open_by_key(SPREADSHEET_ID)
		card_sheet = sh.worksheet(SPREADSHEET_SHEET)
		cards = parse_list_gs(card_sheet)
		if args.tokens:
			token_sheet = sh.worksheet(SPREADSHEET_SHEET_TOKEN)
			token_cards = parse_list_gs(card_sheet)

	run('otakube', cards, args.print)
	if args.tokens:
		run('otakube_tokens', token_cards, args.print)

	if args.upload and os.path.exists('upload.py') and not args.print:
		subprocess.call(["python", "upload.py"])
