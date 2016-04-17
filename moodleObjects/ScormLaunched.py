import config
import moodleObjects
import tincan

class ScormLaunched(moodleObjects.ModuleViewed):
	VERB = ["launched", "http://adlnet.gov/expapi/verbs/launched"]
	TYPE_EN = "scorm"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/scorm"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_module"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT *
				 FROM %(prefix)sscorm_scoes ss
				 	JOIN %(prefix)sscorm s ON s.id = ss.scorm
				 WHERE ss.id = '%(oid)s';"""%{'prefix': config.MOODLE_PREFIX, 'oid': objectid}
		self.cursor.execute(query)
		row = self.cursor.fetchone()
		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			row['type'] = self.TYPE_EN
			row['url'] = str(config.BASE_URI) + "/mod/scorm/view.php?id=" + str(contextInstanceID)

			self.data = row