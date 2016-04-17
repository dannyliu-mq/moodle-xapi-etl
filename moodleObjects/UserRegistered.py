import config
import moodleObjects
import tincan

class UserRegistered(moodleObjects.ModuleViewed):
	VERB = ["registered to", "http://adlnet.gov/expapi/verbs/registered"]
	TYPE_EN = "site"
	TYPE = "http://id.tincanapi.com/activitytype/site"
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