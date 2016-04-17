import config
import moodleObjects
import tincan

class DiscussionCreated(moodleObjects.ModuleViewed):
	VERB = ["created", "http://activitystrea.ms/schema/1.0/create"]
	TYPE_EN = "forum_discussion"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/forum_discussion"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_discussion"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %sforum_discussions c
				 WHERE c.id = '%s'"""%(config.MOODLE_PREFIX, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		# if 'name' not in row: raise moodleObjects.moodleWarning("Failed to match record from " + objecttable + " with objectid " + str(objectid))

		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/forum/discuss.php?id=" + str(objectid)
			self.data['intro'] = "A Moodle discussion."


			# Build the additional grouping
			query="""SELECT f.*
					 FROM %sforum f
					 WHERE f.id = '%s';"""%(config.MOODLE_PREFIX, self.data['forum'])
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['url'] = config.BASE_URI + "/mod/forum/view.php?id=" + str(contextInstanceID)
			row['type'] = 'forum'

			self.groupings.append({
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['name']} ),
					"type": "http://lrs.learninglocker.net/define/type/moodle/forum",
					"description": tincan.LanguageMap( {'en': row['intro']} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_module": row
					}
				}
			})