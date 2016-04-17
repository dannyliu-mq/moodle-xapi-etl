import logging

# These will be almost identical however this makes catching the errors
# easier
class moodleCritical(Exception):

	def __init__(self, errString):
		self.err = errString
	def addLogID(self, logID):
		self.logID = logID
	def __str__(self):
		return """{
	"type":			"Critical",
	"logID":		""" + str(self.logID) + """,
	"description": 	""" + repr(self.err) + """
}"""

class moodleError(Exception):

	def __init__(self, errString):
		self.err = errString
	def addLogID(self, logID):
		self.logID = logID
	def __str__(self):
		return """{
	"type":			"Error",
	"logID":		""" + str(self.logID) + """,
	"description": 	""" + repr(self.err) + """
}"""

class moodleWarning(Exception):

	def __init__(self, errString):
		self.err = errString
	def addLogID(self, logID):
		self.logID = logID
	def __str__(self):
		return """{
	"type":			"Warning",
	"logID":		""" + str(self.logID) + """,
	"description": 	""" + repr(self.err) + """
}"""