import config
import moodleObjects
import tincan

class AssignmentSubmitted(moodleObjects.ModuleViewed):
	VERB = ["completed", "http://adlnet.gov/expapi/verbs/completed"]
	TYPE_EN = "assign"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/assign"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_module"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()
		
		# Get additiona information required for the object
		query="""SELECT a.*
				 FROM %(prefix)sassign_submission s
				 	JOIN %(prefix)sassign a ON s.assignment = a.id
				 WHERE s.id = '%(oid)s';"""%{'prefix': config.MOODLE_PREFIX, 'oid': objectid}
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/assign/view.php?id=" + str(objectid)