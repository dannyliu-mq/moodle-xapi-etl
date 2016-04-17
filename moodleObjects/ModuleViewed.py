import config
import moodleObjects
import tincan

class ModuleViewed(object):
	# Generic Lists for Viewed
	VIEWED_TYPE_BASE = "http://lrs.learninglocker.net/define/type/moodle/"

	# Removed Object
	REMOVED_TYPE = config.LRS_URI + "/define/type/moodle/removedObject"

	# Possibly inherited stuff
	VERB = ["viewed", "http://id.tincanapi.com/verb/viewed"]
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_module"
	TYPE = None
	TYPE_EN = None
	data = []
	groupings = []
	removedObject = False

	def __init__(self, objecttable, objectid, contextInstanceID):
		# This should NOT be called from a child.
		# Each child should have their own init function specific to that class

		# Just a small safeguard against invalid data
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

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

		if( row is None ):
			self.setRemovedObject(objecttable, objectid, None)
		else:
			self.data = row
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/" + objecttable + "/view.php?id=" + str(contextInstanceID)

	def standardInit(self):
		# This module SHOULD be called by all children
		self.groupings = []

	def hasResult(self):
		return hasattr(self, 'result')

	def setRemovedObject(self, objecttable, objectid, contextInstanceID):
		# Handles when  an object has been deleted but the log reference still exists

		self.TYPE = self.REMOVED_TYPE

		self.data = {
			'type':		self.TYPE_EN,
			'url':		str(config.BASE_URI) + "/mod/" + self.TYPE_EN + "/view.php?id=" + str(contextInstanceID),
			'name':		'Deleted ' + self.TYPE_EN + ' object #' + str(objectid),
			'intro':	'This object has been deleted from the database and could not be properly referenced.'
		}

	def getVerb(self):
		return tincan.Verb(
			id = type(self).VERB[1],
			display = tincan.LanguageMap({
				'en': type(self).VERB[0]
			})
		)

	def getObject(self):
		data = self.data

		# Hack to convert grade from Decimal to float
		if 'grade' in data and data['grade'] is not None: data['grade'] = float(data['grade'])
		if 'sumgrades' in data and data['sumgrades'] is not None: data['sumgrades'] = float(data['sumgrades'])
		if 'gradinggrade' in data and data['gradinggrade'] is not None: data['gradinggrade'] = float(data['gradinggrade'])

		# Create a reference to the child class to pull static information from it
		if(self.TYPE is not None):
			selfRef = self
		else:
			selfRef = type(self)

		# Quick checks on data
		if 'name' not in data: raise moodleObjects.moodleCritical("No Name passed to ModuleViewed with objectID: " + str(data['id']))

		if 'intro' in data:
			# Cap the post information to 1000 chars
			data['intro'] = data['name'][:1000]
			data['intro'] = unicode(data['intro'][:1000], errors='ignore')
			if 'content' in data: data['content'] = unicode(data['content'][:1000], errors='ignore')

			return tincan.Activity(
			id 			= data['url'],
			definition 	= tincan.ActivityDefinition(
				name 		= tincan.LanguageMap({'en': data['name']}),
				description = tincan.LanguageMap({'en': data['intro']}),
				type = selfRef.TYPE,
				extensions 	= { 
					type(self).EXT: data
				}
			)
		)
		else:
			return tincan.Activity(
				id 			= data['url'],
				definition 	= tincan.ActivityDefinition(
					name 		= tincan.LanguageMap({'en': data['name']}),
					type 		= selfRef.TYPE,
					extensions 	= { 
						type(self).EXT: data
					}
				)
			)

	def getBaseGrouping(self):
		# Get the site information once only
		try:
			tmp = ModuleViewed.baseGrouping
		except AttributeError:
			query="""SELECT *
				 FROM %scourse
				 WHERE id = '1';"""%config.MOODLE_PREFIX
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['type'] = 'site'
			row['url'] = str(config.BASE_URI)
			ModuleViewed.baseGrouping = {
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['fullname']} ),
					"type": "http://id.tincanapi.com/activitytype/site",
					"description": tincan.LanguageMap( {'en': row['summary']} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_course": row
					}
				}
			}
		return ModuleViewed.baseGrouping

	def getContext(self, logRow):
		# groupings = []
		groupings = self.groupings

		# Get site information
		groupings.append(self.getBaseGrouping())

		# Get the course info (if applicable. Yes this condition is weird but it is correct.)
		if 'objectid' not in self.data and logRow['courseid'] > 0:
			query="""SELECT *
					 FROM %scourse
					 WHERE id = '%s';"""%(config.MOODLE_PREFIX, logRow['courseid'])
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['type'] = 'course'
			row['url'] = config.BASE_URI + "/course/view.php?id=" + str(row['id'])
			groupings.append({
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['fullname']} ),
					"type":	"http://lrs.learninglocker.net/define/type/moodle/course",
					"description": tincan.LanguageMap( {'en': str(row['summary'])} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_course": row
					}
				}
			})

		# Return the actual context
		return tincan.Context(
			contextActivities={
				"category":	[{
					"objectType":	"Activity",
					"id":			"http://moodle.org",
					"definition": {
						"type":			"http://id.tincanapi.com/activitytype/source",
						"name": tincan.LanguageMap( {'en': "Moodle"} ),
						"description":	tincan.LanguageMap( {'en': "Moodle is a open source learning platform designed to provide educators, administrators and learners with a single robust, secure and integrated system to create personalised learning environments."} )
					}
				}],
				"grouping": groupings
			},
			platform = 	"Moodle",
			language =	"en",
			extensions = {
				"http://lrs.learninglocker.net/define/extensions/moodle_logstore_standard_log": logRow,
				"http://lrs.learninglocker.net/define/extensions/info": {
					"https://github.com/dannyliu-mq/moodle-xapi-etl": config.VERSION
				}
			}
		)

	def getResult(self):
		# Tincan handles no result gracefully
		if self.hasResult():
			return tincan.Result(self.result)



	def __str__(self):
		raise moodleObjects.moodleCritical("__str__ function has not been written yet. ")