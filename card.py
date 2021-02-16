class Card():

    def __init__(self, entry):
      self.id = int(entry[0])
      self.name = entry[1]
      self.revision = entry[2]
      self.type = entry[3]
      self.subtypes = entry[3]
      self.color = entry[4]
      self.cost = entry[5]
      self.power = None
      self.toughness = None
      self.rules_text  = entry[7]
      self.flavor_text  = entry[9]
      self.rarity  = entry[12]
      self.creator  = entry[13]

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
	super type: <word-list-type>{self.type}</word-list-type>
	sub type: <word-list-race></word-list-race>
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