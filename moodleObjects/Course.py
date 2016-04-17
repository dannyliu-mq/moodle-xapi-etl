import config
import moodleObjects

class Course(moodleObjects.ModuleViewed):
	def __init__(self, courseID):
		if type(courseID) is not long: raise moodleObjects.moodleWarning("Invalid CourseID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT *
				 FROM %scourse
				 WHERE id = '%s';"""%(config.MOODLE_PREFIX, str(courseID))
		self.cursor.execute(query)
		row = self.cursor.fetchone()