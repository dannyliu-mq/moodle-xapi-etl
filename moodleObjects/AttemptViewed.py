import config
import moodleObjects
import tincan

class ModuleViewed(object):
	VERB = ["viewed", "http://id.tincanapi.com/verb/viewed"]
	TYPE_EN = "quiz_attempts"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/course"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_course"

	def __init__(self, objecttable, objectid, contextInstanceID):
		# This should NOT be called from a child.
		# Each child should have their own init function specific to that class


		self.standardInit()

		# Just a small safeguard against invalid data
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		# Setup the types that are normally const
		self.TYPE = self.VIEWED_TYPE_BASE + objecttable
		self.TYPE_EN = objecttable

		# Query the data
		# This may cause an error for a non-standard storage method
		query="""SELECT  *
				 FROM %s%s
				 WHERE id = '%s'"""%(config.MOODLE_PREFIX, objecttable, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		if (row is None or len(row) == 0):
			raise moodleObjects.moodleError("Failed to query information from " + config.MOODLE_PREFIX + objecttable)


		self.data = row
		self.data['type'] = self.TYPE_EN
		self.data['url'] = config.BASE_URI + "/mod/" + objecttable + "/view.php?id=" + str(contextInstanceID)
