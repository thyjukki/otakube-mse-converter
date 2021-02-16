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

	def __repr__(self):
			return f"Card([{self.id, self.name}])"

	def __str__(self):
			return f"id: {self.id} name: {self.name}"

	def generate_mse_card(self):

		text = f"""
card:
	has styling: false
	notes: 
	time created: 2019-06-02 01:47:48
	time modified: 2019-06-02 01:50:10
	name: {self.name}
	casting cost: {self.cost}
	image:
	super type: <word-list-type>{' '.join(self.super_types)}</word-list-type>
	sub type: <word-list-race>{' '.join(self.sub_types)}</word-list-race>
	rarity: {self.rarity}
	rule text:
		{self.rules_text}		
	flavor text: <i-flavor>{self.flavor_text}</i-flavor>"""
		if self.power and self.toughness:
			text += f"""
	power: {self.power}
	toughness: {self.toughness}"""

		text += f"""
	card code text: 
	illustrator:
		{self.creator}
	copyright: 
	image 2: 
	copyright 2: 
	copyright 3: 
	mainframe image: 
	mainframe image 2:"""
		return text