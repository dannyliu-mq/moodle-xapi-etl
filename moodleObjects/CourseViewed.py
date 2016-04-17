import config
import moodleObjects

class CourseViewed(moodleObjects.ModuleViewed):
	VERB = ["viewed", "http://id.tincanapi.com/verb/viewed"]
	TYPE_EN = "course"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/course"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_course"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %scourse c
				 WHERE c.id = '%s'"""%(config.MOODLE_PREFIX, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()
		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/course/view.php?id=" + str(objectid)
			self.data['name'] = row['fullname']
			self.data['intro'] = row['summary']