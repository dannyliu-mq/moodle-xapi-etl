import config
import moodleObjects
import tincan
import sys
import re

class AssignmentGraded(moodleObjects.ModuleViewed):
	VERB = ["recieved grade for", "http://adlnet.gov/expapi/verbs/scored"]
	TYPE_EN = "assign"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/assign"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_module"

	def __init__(self, objecttable, objectid, relatedUserID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %sassign c
				 WHERE c.id = '%s'"""%(config.MOODLE_PREFIX, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		# if 'name' not in row: raise moodleObjects.moodleWarning("Failed to match record from " + objecttable + " with objectid " + str(objectid))

		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, None)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/assign/view.php?id=" + str(objectid)

			self.groupings.append({
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['name']} ),
					"type": self.TYPE,
					"description": tincan.LanguageMap( {'en': row['intro']} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_module": row
					}
				}
			})

		# Get the result
		query="""SELECT (gg.rawgrade/gg.rawgrademax) as scaled, gg.rawgrade as raw, gg.rawgrademax as max, true as completion, gg.feedback as response
				 FROM %(prefix)sassign_grades ag
				 	JOIN %(prefix)sgrade_items gi ON gi.iteminstance = ag.assignment
				 	JOIN %(prefix)sgrade_grades gg ON gg.itemid = gi.id
				 WHERE gi.itemmodule = 'assign'
				 AND ag.id = '%(oid)s'
				 AND gg.userid = '%(ruid)s'"""%{'prefix': config.MOODLE_PREFIX, 'oid': objectid, 'ruid': relatedUserID}
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		# Quick fix for a empty response (regex criticals)
		if row['response'] is None: row['response'] = ''
		for key in ['scaled', 'raw', 'max']:
			if row[key] is not None: row[key] = int(row[key])


		self.result = {
			"score": {
				"scaled":	row['scaled'],
				"raw":	 	row['raw'],
				"max":		row['max']
			},
			"completion":	row['completion'],
			"response":		re.sub(r'[^\x00-\x7F]+',' ', row['response'])	# Non-unicode characters, cannot be serialized so this replaces them with a space
		}