class Card():

	def parse_types(self, raw_type):
		splits = raw_type.split('-')
		self.super_types = splits[0].split()

		if len(splits) > 1:
			self.sub_types = splits[1].split()
		else:
			self.sub_types = []

	def parse_statline(self, raw_stat):
		if not raw_stat and not raw_stat.strip():
			self.power = None
			self.toughness = None
			return
		if "Planeswalker" in self.super_types:
			self.loyalty = int(raw_stat[0].strip())
			self.power = None
			self.toughness = None
			return
	
		splits = raw_stat.split('/')
		self.power = splits[0].strip()
		if len(splits) > 1:
			self.toughness = splits[1].strip()
		else:
			print(f"ERROR {raw_stat} statline on {self.name}")
			self.toughness = 'Nil'
		
	def __init__(self, entry):
		self.id = int(entry[0])
		self.name = entry[1]
		self.revision = entry[2]
		self.parse_types(entry[3])
		self.color = entry[4]
		self.cost = entry[5]
		self.parse_statline(entry[6])
		self.rules_text = entry[7]
		self.flavor_text = entry[9]
		self.rarity = entry[12]
		self.creator = entry[13]

		self.check_errors()

	def check_errors(self):
		if "Land" in self.super_types:
			if self.cost and self.cost.strip():
				print(f"WARNING: Land {self} with CMC! ({self.cost})")


	def get_sub_type_text(self):
		element = ""
		if "Land" in self.super_types:
			element = 'word-list-land'
		elif "Creature" in self.super_types:
			element = 'word-list-race'
		elif "Enchantment" in self.super_types:
			element = 'word-list-race'
		elif "Artifact" in self.super_types:
			element = 'word-list-artifact'
		elif "Instant" in self.super_types:
			element = 'word-list-spell'
		elif "Sorcery" in self.super_types:
			element = 'word-list-spell'
		elif "Planeswalker" in self.super_types:
			element = 'word-list-planeswalker'

		return f"<{element}>{' '.join(self.sub_types)}</{element}>"


	def get_card_number(self, cards_count):
		id_len = len(str(self.id))
		total_len = len(str(cards_count))
		diff = total_len - id_len

		if diff < 0:
			print(f"ERROR: {self} id exedecs set card count ({cards_count})")
			return f"nil/{cards_count}"
		
		return f"{'0'*diff}{self.id}/{cards_count}"

	
	def get_flavor_text(self):
		parsed_string = ' '.join(self.flavor_text.split('\n'))
		return f"<i-flavor>{parsed_string}</i-flavor>"


	def generate_mse_card(self, cards_count):

		text = f"""
card:"""

		if "Planeswalker" in self.super_types:
			text += f"""
	stylesheet: m15-mainframe-planeswalker"""
		elif "Saga" in self.sub_types:
			text += f"""
	stylesheet: m15-saga"""

		text += f"""
	has styling: false
	notes: 
	time created: 2019-06-02 01:47:48
	time modified: 2019-06-02 01:50:10
	name: {self.name}
	casting cost: {self.cost}
	image:
	super type: <word-list-type>{' '.join(self.super_types)}</word-list-type>
	sub type: {self.get_sub_type_text()}
	rarity: {self.rarity}
	rule text:\n"""

		for line in self.rules_text.split('\n'):
			text += f"		{line.strip()}\n"
		text += f"""	flavor text: {self.get_flavor_text()}"""

		if self.power is not None and self.toughness is not None:
			text += f"""
	power: {self.power}
	toughness: {self.toughness}"""

		if "Planeswalker" in self.super_types:
			text += f"""
	loyalty: {self.loyalty}"""

		text += f"""
	custom card number: {self.get_card_number(cards_count)}
	card code text:
	illustrator: {self.creator}
	copyright: 
	image 2: 
	copyright 2: 
	copyright 3: 
	mainframe image: 
	mainframe image 2:"""
		return text

	def __repr__(self):
			return f"Card([{self.id, self.name}])"

	def __str__(self):
			return f"id: {self.id} name: {self.name}"