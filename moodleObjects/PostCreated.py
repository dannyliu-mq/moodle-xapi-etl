import config
import moodleObjects
import tincan

class PostCreated(moodleObjects.ModuleViewed):
	VERB = ["created", "http://activitystrea.ms/schema/1.0/create"]
	TYPE_EN = "forum_post"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/forum_post"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_post"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %sforum_posts c
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
			self.data['name'] = row['subject']
			self.data['intro'] = row['message']


			# Build the additional grouping
			query="""SELECT d.*
					 FROM %sforum_discussions d
					 WHERE d.id = '%s';"""%(config.MOODLE_PREFIX, self.data['discussion'])
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['url'] = config.BASE_URI + "/mod/forum/discuss.php?id=" + str(contextInstanceID)
			row['type'] = 'forum_discussion'
			row['intro'] = "A Moodle Discussion"

			self.groupings.append({
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['name']} ),
					"type": "http://lrs.learninglocker.net/define/type/moodle/forum_discussion",
					"description": tincan.LanguageMap( {'en': row['intro']} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_module": row
					}
				}
			})

			query="""SELECT f.*
					 FROM %sforum f
					 WHERE f.id = '%s';"""%(config.MOODLE_PREFIX, row['forum'])
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