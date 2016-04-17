import config
import moodleObjects
import tincan

class UserLoggedOut(moodleObjects.ModuleViewed):
	VERB = ["logged out to", "http://brindlewaye.com/xAPITerms/verbs/loggedout/"]
	TYPE_EN = "course"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/course"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_course"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()
		
		# Get additional information required for this
		query="""SELECT *
				 FROM %scourse
				 WHERE id = '1';"""%config.MOODLE_PREFIX
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			row['type'] = self.TYPE_EN
			row['url'] = str(config.BASE_URI)
			row['name'] = row['fullname']
			row['intro'] = row['summary']

			self.data = row