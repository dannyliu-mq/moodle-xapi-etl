import config
import moodleObjects
import tincan

class ConversationViewed(moodleObjects.ModuleViewed):
	# This module should only be used by a module that has a parent.
	VERB = ["viewed", "http://id.tincanapi.com/verb/viewed"]
	TYPE_EN = "ConversationViewed"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/dialogue_conversation"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_conversation"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %sdialogue_conversations c
				 WHERE c.id = '%s'"""%(config.MOODLE_PREFIX, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()

		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/dialogue/conversation.php?id=%s&conversationid=%s"%(str(contextInstanceID), str(objectid))
			self.data['name'] = row['subject']
			self.data['intro'] = "A Moodle Conversation"


			# Build the additional grouping
			query="""SELECT p.*
					 FROM %(prefix)sdialogue_conversations c
					 	JOIN %(prefix)sdialogue p ON c.dialogueid = p.id

					 WHERE c.id = '%(oid)s';"""%{
					 	'prefix':	config.MOODLE_PREFIX,
					 	'oid':		objectid
					 }
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['url'] = config.BASE_URI + "/mod/dialogue/view.php?id=%s"%(str(contextInstanceID))
			row['type'] = self.TYPE
			row['intro'] = "A Moodle Dialogue"

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