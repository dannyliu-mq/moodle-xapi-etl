class MoodleObject():	
	def getStringLine(oneKey, oneVal):
		if isinstance(oneVal, (list, tuple)):
			return '"' + str(oneKey) + '": {\n' + getStringLine(oneVal) + '\n}'
		else:
			return '"' + str(oneKey) + '": "' + str(oneVal) + "\",\n"

	def __str__(self):
		for oneKey, oneVal in enumerate(self.object):
			return getStringLine(oneKey, oneVal)