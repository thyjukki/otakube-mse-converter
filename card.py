def get_sub_type_text(super_types, sub_types):
	element = ""
	if "Land" in super_types:
		element = 'word-list-land'
	elif "Creature" in super_types:
		element = 'word-list-race'
	elif "Enchantment" in super_types:
		element = 'word-list-enchantment'
	elif "Artifact" in super_types:
		element = 'word-list-artifact'
	elif "Instant" in super_types:
		element = 'word-list-spell'
	elif "Sorcery" in super_types:
		element = 'word-list-spell'
	elif "Planeswalker" in super_types:
		element = 'word-list-planeswalker'

	return f"<{element}>{' '.join(sub_types)}</{element}>"


class Card():

	def parse_types(self, raw_type):
		dual_splits = raw_type.split('//')
		splits = dual_splits[0].strip().split('-')
		self.super_types = splits[0].split()

		if len(splits) > 1:
			self.sub_types = splits[1].split()
		else:
			self.sub_types = []
		if len(dual_splits) > 1:
			splits = dual_splits[1].strip().split('-')
			self.super_types2 = splits[0].split()

			if len(splits) > 1:
				self.sub_types2 = splits[1].split()
			else:
				self.sub_types2 = []
		else:
			self.super_types2 = None
			self.sub_types2 = None


	def parse_statline(self, raw_stat):
		if not raw_stat or not raw_stat.strip():
			self.power = ''
			self.toughness = ''
			return
		if "Planeswalker" in self.super_types:
			self.loyalty = int(raw_stat[0].strip())
			self.power = ''
			self.toughness = ''
			return
	
		splits = raw_stat.split('/')
		self.power = splits[0].strip()
		if len(splits) > 1:
			self.toughness = splits[1].strip()
		else:
			print(f"ERROR {raw_stat} statline on {self.name}")
			self.toughness = 'Nil'

	### Parse name, // separates split cards
	def parse_name(self, raw_name):
		splits = raw_name.split('//')
		self.name = splits[0].strip()

		if len(splits) > 1:
			self.name2 = splits[1].strip()
		else:
			self.name2 = None

	def parse_cmc(self, raw_cmc):
		splits = raw_cmc.split('//')
		self.cmc = splits[0].strip()

		if len(splits) > 1:
			self.cmc2 = splits[1].strip()
		else:
			self.cmc2 = None

	def parse_saga(self, raw_rules):
		lines = raw_rules.strip().split('\n')
		line_count = len(lines)
		if line_count == 2:
			self.styling_data = '\n		chapter textboxes: two'
		elif line_count == 3:
			self.styling_data = '\n		chapter textboxes: three'
		elif line_count == 4:
			self.styling_data = '\n		chapter textboxes: four'

		self.level1 = lines[0].split(':')[-1].strip()
		self.level2 = lines[1].split(':')[-1].strip() if line_count > 1 else None
		self.level3 = lines[2].split(':')[-1].strip() if line_count > 2 else None
		self.level4 = lines[3].split(':')[-1].strip() if line_count > 3 else None

	def parse_planeswalker(self, raw_rules):
		lines = raw_rules.strip().split('\n')
		line_count = len(lines)

		self.level1 = lines[0].split(':')[-1].strip()
		self.loyaly1_cost = lines[0].split(':')[0].strip()
		if line_count > 1:
			self.level2 = lines[1].split(':')[-1].strip()
			self.loyaly2_cost = lines[1].split(':')[0].strip()
		if line_count > 2:
			self.level3 = lines[2].split(':')[-1].strip()
			self.loyaly3_cost = lines[2].split(':')[0].strip()
		if line_count > 3:
			self.level4 = lines[3].split(':')[-1].strip()
			self.loyaly4_cost = lines[3].split(':')[0].strip()

	def parse_modal(self,  raw_rules):
		lines = raw_rules.split('\n')
		self.modal_rules = ""
		first = True
		for line in lines[1:]:
			if first:
				first = False
				self.modal_rules += f"\n		<soft-line>{line.strip()}"
			else:
				self.modal_rules += f"\n		{line.strip()}"
		self.modal_rules += '</soft-line>'

			

	def parse_rules(self, raw_rules):
		if "Saga" in self.sub_types:
			self.parse_saga(raw_rules)
			self.rules_text = '<i-auto>(As this Saga enters and after your draw step, add a lore counter. Sacrifice after <nosym>I</nosym><nosym>I</nosym><nosym>I</nosym>.)</i-auto>'
			return

		if "Planeswalker" in self.super_types:
			self.parse_planeswalker(raw_rules)
			self.rules_text = '<i-auto>(As this Saga enters and after your draw step, add a lore counter. Sacrifice after <nosym>I</nosym><nosym>I</nosym><nosym>I</nosym>.)</i-auto>'
			return
		
		first_line = raw_rules.split('\n')[0].strip()
		if first_line.startswith('Choose') and first_line.endswith(':'):
			self.parse_modal(raw_rules)
			self.level1 = first_line
			#return

		splits = raw_rules.split('//')
		lines = splits[0].strip().split('\n')
		self.rules_text = '\n'.join(map(lambda x: f"		{x.strip()}", lines))
		if len(lines) > 1:
			self.rules_text = f"\n{self.rules_text}"

		if len(splits) > 1:
			lines2 = splits[1].strip().split('\n')
			self.rules_text2 = '\n'.join(map(lambda x: f"		{x.strip()}", lines2))
			if len(lines2) > 1:
				self.rules_text2 = f"\n{self.rules_text2}"
		else:
			self.rules_text2 = None

	def parse_flavor(self, raw_flavor):
		splits = raw_flavor.split('//')
		parsed_string = ' '.join(splits[0].strip().split('\n'))
		self.flavor_text = f"<i-flavor>{parsed_string}</i-flavor>"

		if len(splits) > 1:
			parsed_string2 = ' '.join(splits[1].strip().split('\n'))
			self.flavor_text2 = f"<i-flavor>{parsed_string2}</i-flavor>"
		else:
			self.flavor_text2 = None


	def __init__(self, entry):
		self.loyaly1_cost = None
		self.loyaly2_cost = None
		self.loyaly3_cost = None
		self.loyaly4_cost = None
		self.level1 = None
		self.level2 = None
		self.level3 = None
		self.level4 = None
		self.modal_rules = None
		self.rules_text2 = None

		self.id = int(entry[0])
		self.parse_name(entry[1])
		self.revision = entry[2]
		self.parse_types(entry[3])
		self.color = entry[4]
		self.parse_cmc(entry[5])
		self.parse_statline(entry[6])
		self.parse_rules(entry[7])
		self.parse_flavor(entry[9])
		self.rarity = entry[12]
		self.creator = entry[13]

		self.check_errors()

	def check_errors(self):
		if "Land" in self.super_types:
			if self.cmc and self.cmc.strip():
				print(f"WARNING: Land {self} with CMC! ({self.cmc})")


	def get_card_number(self, cards_count):
		id_len = len(str(self.id))
		total_len = len(str(cards_count))
		diff = total_len - id_len

		if diff < 0:
			print(f"ERROR: {self} id exedecs set card count ({cards_count})")
			return f"nil/{cards_count}"
		
		return f"{'0'*diff}{self.id}/{cards_count}"


	def generate_mse_card(self, cards_count):

		text = f"""
card:"""

		if "Planeswalker" in self.super_types:
			text += f"""
	stylesheet: m15-mainframe-planeswalker
	has styling: false"""
		elif "Saga" in self.sub_types:
			text += f"""
	stylesheet: m15-saga
	has styling: true
	styling data: {self.styling_data}
		text box mana symbols: magic-mana-small.mse-symbol-font
		overlay: 
"""
		elif "Enchantment" in self.super_types and "Creature" in self.super_types:
			text += f"""
	stylesheet: m15-altered
	has styling: true
	styling data:
		frames: nyx
		other options: auto nyx crowns
"""
		elif self.modal_rules:
			text += f"""
	stylesheet: m15-altered
	has styling: true
	styling data:
		frames: modal
		text box mana symbols: magic-mana-small.mse-symbol-font
		level mana symbols: magic-mana-large.mse-symbol-font
		overlay: """
		elif self.name2:
			text += f"""
	stylesheet: m15-split-fusable
	has styling: false"""
		else:
			text += f"""
	stylesheet: m15-altered
	has styling: false"""

		text += f"""
	notes: 
	time created: 2019-06-02 01:47:48
	time modified: 2019-06-02 01:50:10
	name: {self.name}
	casting cost: {self.cmc}
	image:
	super type: <word-list-type>{' '.join(self.super_types)}</word-list-type>
	sub type: {get_sub_type_text(self.super_types, self.sub_types)}
	rarity: {self.rarity}
	rule text: {self.rules_text}
	flavor text: {self.flavor_text}"""
	
		if self.loyaly1_cost:
			text += f"""
	loyalty cost 1: {self.loyaly1_cost}"""
		if self.level1:
			text += f"""
	level 1 text: {self.level1}"""
	
		if self.loyaly2_cost:
			text += f"""
	loyalty cost 2: {self.loyaly2_cost}"""
		if self.level2:
			text += f"""
	level 2 text: {self.level2}"""
	
		if self.loyaly3_cost:
			text += f"""
	loyalty cost 3: {self.loyaly3_cost}"""
		if self.level3:
			text += f"""
	level 3 text: {self.level3}"""
	
		if self.loyaly4_cost:
			text += f"""
	loyalty cost 4: {self.loyaly4_cost}"""
		if self.level4:
			text += f"""
	level 4 text: {self.level4}"""

		if self.modal_rules:
			text += f"""
	modal rule text: {self.modal_rules}"""

		if "Planeswalker" in self.super_types:
			text += f"""
	loyalty: {self.loyalty}"""

		text += f"""
	power: {self.power}
	toughness: {self.toughness}"""

		text += f"""
	custom card number: {self.get_card_number(cards_count)}
	card code text:
	illustrator: {self.creator}
	copyright: """

		if self.name2:
			text += f"""
	name 2: {self.name2}"""

		if self.cmc2:
			text += f"""
	casting cost 2: {self.cmc2}"""

		text += f"""
	image 2: """

		if self.super_types2:
			text += f"""
	super type 2: <word-list-type>{' '.join(self.super_types2)}</word-list-type>"""

		if self.sub_types2:
			text += f"""
	sub type 2: {get_sub_type_text(self.super_types2, self.sub_types2)}"""

		if self.rules_text2:
			text += f"""
	rule text 2: {self.rules_text2}"""

		if self.flavor_text2:
			text += f"""
	flavor text 2: {self.flavor_text2}"""

		text += f"""
	copyright 2: 
	copyright 3: 
	mainframe image: 
	mainframe image 2:"""
		return text

	def __repr__(self):
			return f"Card([{self.id, self.name}])"

	def __str__(self):
			return f"id: {self.id} name: {self.name}"