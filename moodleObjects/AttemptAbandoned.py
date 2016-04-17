import config
import moodleObjects
import tincan

class AttemptAbandoned(moodleObjects.ModuleViewed):
	VERB = ["abandoned", "https://w3id.org/xapi/adl/verbs/abandoned"]
	TYPE_EN = "quiz_attempts"
	TYPE = "http://lrs.learninglocker.net/define/type/moodle/quiz_attempts"
	EXT = "http://lrs.learninglocker.net/define/extensions/moodle_attempt"

	def __init__(self, objecttable, objectid, contextInstanceID):
		if type(objectid) is not long: raise moodleObjects.moodleWarning("Invalid ObjectID provided")

		self.standardInit()

		# Get additional information required for this
		query="""SELECT  *
				 FROM %squiz_attempts qa
				 WHERE qa.id = '%s'"""%(config.MOODLE_PREFIX, objectid)
		self.cursor.execute(query)
		row = self.cursor.fetchone()
		
		if( row is None ):
			self.setRemovedObject(objecttable, objectid, contextInstanceID)
		else:
			self.data = row
			self.data['name'] = 'Attempt ' + str(objectid)
			self.data['type'] = self.TYPE_EN
			self.data['url'] = config.BASE_URI + "/mod/quiz/attempt.php?id=" + str(objectid)
			self.data['questions'] = {}

			# Add additional information to the object
			query="""SELECT qa.*
					 FROM %squestion_attempts qa
					 WHERE qa.questionusageid = '%s';"""%(config.MOODLE_PREFIX, row['uniqueid'])
			self.cursor.execute(query)
			questionAttempts = self.cursor.fetchall()		# Yes this is bad. So is creating 3 connections to a db.
			for questionAttempt in questionAttempts:
				# Clean questionAttempt information
				questionAttempt['maxmark'] = int(questionAttempt['maxmark'])
				questionAttempt['maxfraction'] = int(questionAttempt['maxfraction'])
				questionAttempt['minfraction'] = int(questionAttempt['minfraction'])
				questionAttempt['steps'] = {}

				# Query the steps
				query="""SELECT *
						 FROM %squestion_attempt_steps
						 WHERE questionattemptid = '%s';"""%(config.MOODLE_PREFIX, questionAttempt['id'])
				self.cursor.execute(query)
				attemptSteps = self.cursor.fetchall()		# Yes this is bad. So is creating 4 connections to a db.

				for step in attemptSteps:
					if 'fraction' in step and step['fraction'] is not None: step['fraction'] = int(step['fraction'])
					# Query the data
					query="""SELECT *
							 FROM %squestion_attempt_step_data
							 WHERE attemptstepid = '%s';"""%(config.MOODLE_PREFIX, step['id'])
					self.cursor.execute(query)
					stepData = self.cursor.fetchone()
					step['data'] = stepData
					questionAttempt['steps'][step['id']] = step


				self.data['questions'][questionAttempt['id']] =  questionAttempt

			# Build the additional grouping
			query="""SELECT q.*
					 FROM %squiz q
					 WHERE q.id = '%s';"""%(config.MOODLE_PREFIX, self.data['quiz'])
			self.cursor.execute(query)
			row = self.cursor.fetchone()
			row['url'] = config.BASE_URI + "/mod/quiz/view.php?id=" + str(contextInstanceID)
			row['type'] = 'quiz'
			row['grade'] = float(row['grade'])
			row['sumgrades'] = float(row['sumgrades'])

			self.groupings.append({
				"id":		row['url'],
				"definition": {
					"name": tincan.LanguageMap( {'en': row['name']} ),
					"type": "http://lrs.learninglocker.net/define/type/moodle/quiz",
					"description": tincan.LanguageMap( {'en': row['intro']} ),
					"extensions": {
						"http://lrs.learninglocker.net/define/extensions/moodle_module": row
					}
				}
			})
