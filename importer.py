#!/usr/bin/env python

"""
    This file is part of Macqauarie Open Analytics Toolkit (MOAT).

    MOAT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MOAT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MOAT.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
	Main file for the MOAT project's Moodle xAPI importer

	@author Ed Moore <ed.moore@mq.edu.au>, Danny Liu <danny.liu@mq.edu.au>, James Hamilton <james.hamilton@mq.edu.au>, Yvonne Nemes <yvonne.nemes@mq.edu.au>
	@copyright 2016 Macquarie University
	@license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"""
# import settings
import config
import psycopg2
import psycopg2.extras
import sys
import time
import logging
import moodleObjects
from datetime import date,datetime,timedelta
import json

from pymongo import MongoClient
from bson import ObjectId
from tincan import (RemoteLRS, Agent, Statement)

if config.VERBOSE: logging.getLogger().addHandler(logging.StreamHandler())

ACTIVITY_ROUTES = {
	'\\core\\event\\course_viewed':									moodleObjects.CourseViewed,
	'\\mod_page\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_quiz\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_url\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_folder\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_forum\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	# '\\mod_forum\\event\\discussion_viewed':						moodleObjects.SubModuleViewed,
	'\\mod_forum\\event\\user_report_viewed':						moodleObjects.ModuleViewed,
	'\\mod_book\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_scorm\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_resource\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_choice\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_data\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_feedback\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_lesson\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_lti\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_wiki\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_workshop\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_chat\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_glossary\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_imscp\\event\\course_module_viewed':						moodleObjects.ModuleViewed,
	'\\mod_survey\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	'\\mod_facetoface\\event\\course_module_viewed':				moodleObjects.ModuleViewed,
	'\\mod_quiz\\event\\attempt_abandoned':							moodleObjects.AttemptAbandoned,
	'\\mod_quiz\\event\\attempt_preview_started':					moodleObjects.AttemptStarted,
	'\\core\\event\\user_loggedin':									moodleObjects.UserLoggedIn,
	'\\core\\event\\user_loggedout':								moodleObjects.UserLoggedOut,
	'\\mod_assign\\event\\submission_graded':						moodleObjects.AssignmentGraded,
	'\\mod_assign\\event\\assessable_submitted':					moodleObjects.AssignmentSubmitted,
	'\\core\\event\\user_created':									moodleObjects.UserRegistered,
	# '\\core\\event\\user_enrolment_created':						moodleObjects.EnrolmentCreated,
	'\\mod_scorm\\event\\sco_launched':								moodleObjects.ScormLaunched,
	# '\\mod_quiz\\event\\attempt_reviewed':							moodleObjects.SubModuleViewed,
	# '\\mod_quiz\\event\\attempt_viewed':							moodleObjects.SubModuleViewed,
	# '\\core\\event\\user_graded':									moodleObjects.UserGraded,
	# '\\mod_assign\\event\\feedback_viewed':							moodleObjects.SubModuleViewed,
	# '\\mod_assign\\event\\submission_viewed':						moodleObjects.SubModuleViewed,
	# '\\mod_book\\event\\chapter_viewed':							moodleObjects.SubModuleViewed,
	'\\mod_dialogue\\event\\conversation_viewed':					moodleObjects.ConversationViewed,
	'\\mod_dialogue\\event\\course_module_viewed':					moodleObjects.ModuleViewed,
	# '\\mod_dialogue\\event\\conversation_created':					moodleObjects.ConversationCreated,
	'\\mod_forum\\event\\post_created':								moodleObjects.PostCreated,
	'\\mod_forum\\event\\discussion_created':						moodleObjects.DiscussionCreated,
	'\\mod_lesson\\event\\lesson_started':							moodleObjects.ModuleViewed,
	# '\\mod_lesson\\event\\lesson_ended':							moodleObjects.LessonEnded,
	'\\mod_lti\\event\\course_module_instance_list_viewed':			moodleObjects.ModuleViewed,
	'\\mod_quiz\\event\\attempt_started':							moodleObjects.AttemptStarted,
	'\\mod_quiz\\event\\report_viewed':								moodleObjects.ModuleViewed,
	'\\mod_quiz\\event\\attempt_submitted':							moodleObjects.AttemptSubmitted,
	'\\mod_resource\\event\\course_module_instance_list_viewed':	moodleObjects.ModuleViewed

}

#####################################
#	Nice formatting + Headings		#
#####################################
print "="*43
print " "*3 + " MOAT project's moodle xAPI importer " + " "*9
print "="*43
print ""
# Print settings


#####################################
#	Construct actual connections	#
#####################################
print "Creating Connections"
sys.stdout.write("\tLRS Connection...")
sys.stdout.flush()
lrs = RemoteLRS(
	version=config.LRS_VERSION,
	endpoint=config.LRS_ENDPOINT,
	username=config.LRS_USERNAME,
	password=config.LRS_PASSWORD
)
print "done"
##
sys.stdout.write("\tMoodle Connection...")
sys.stdout.flush()
try:
	conn=psycopg2.connect(database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
	cur=conn.cursor('cursor_one', cursor_factory=psycopg2.extras.RealDictCursor)
	cur.itersize=config.ITER_SIZE
	cur2=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
except:
	print "failed"
	sys.exit(99)
print "done"
##
# We need to connect to mongo directly to query the most recent statements inserted by us
sys.stdout.write("\tMongoDB Connection...")
sys.stdout.flush()
client = MongoClient()
db = getattr(client, config.LRS_COLLECTION)
try:
	statements=db.statements
	row = statements.find({"statement.authority.account.homePage": config.LRS_URI, "lrs._id": ObjectId(config.LRS_ID)}).sort("timestamp", -1).limit(1)
	if( row.count() > 0):
		startTime=int(row[0]['timestamp'].strftime("%s"))
	else:
		startTime=0
except:
	logging.exception("Failed to connect to MongoDB")
	sys.exit(99)
print "done"

#####################################

# Queries the Site information for Moodle
sys.stdout.write("Querying Moodle information...")
sys.stdout.flush()
cur2.execute("SELECT * FROM " + config.MOODLE_PREFIX + "course WHERE id = 1;")
siteDetails = dict(cur2.fetchone())
siteDetails['type'] = 'site'
siteDetails['url'] = config.BASE_URI
print "done"

# Creates a static object used for a Moodle Reference
sys.stdout.write("Creating Static objects...")
moodleObjects.ModuleViewed.cursor = cur2
sys.stdout.flush()
context_category = [{
	"objectType":		"Activity",
	"id": 				"http://moodle.org",
	"definition": {
		"type": 		"http://id.tincanapi.com/activitytype/source",
		"name": {
			"en": 		"Moodle"
		},
		"description": {
			"en": 		"Moodle is a open source learning platform designed to provide educators, administrators and learners with a single robust, secure and integrated system to create personalised learning environments."
		}
	}	
}]
print "done"

# Count how many statements from Moodle will be imported
# We use a seperate statement call as large queries will not be able to return a result count
sys.stdout.write("Counting entries...")
sys.stdout.flush()
cur2.execute("SELECT COUNT(*) as count FROM " + config.MOODLE_PREFIX + "logstore_standard_log WHERE timecreated > " + str(startTime) + " AND eventname NOT IN ('\\core\\event\\course_module_deleted', '\\core\\event\\calendar_event_created')")
rowCount = int(cur2.fetchone()['count'])
print "done (" + "{:,}".format(rowCount) + " records found)"

# This actually gets the information in a cursor (stored on the database side due to memory overflow on client side)
sys.stdout.write("Querying statements...")
sys.stdout.flush()
cur.execute("SELECT * FROM " + config.MOODLE_PREFIX + "logstore_standard_log  WHERE timecreated > " + str(startTime) + " AND eventname NOT IN ('\\core\\event\\course_module_deleted', '\\core\\event\\calendar_event_created') ORDER BY timecreated ASC")
state = time.time()

# Parse the log cursor and handle each statement
for row in cur:
	try:
		eventname=row['eventname']

		# Check the eventname has a mapping
		if eventname not in ACTIVITY_ROUTES:
			raise moodleObjects.moodleWarning(eventname + " not mapped event.")
			continue

		# Actor is easy to build straight from a log row
		cur2.execute("SELECT Username, Firstname, Lastname FROM " + config.MOODLE_PREFIX + "user WHERE id = '" + str(row['userid']) + "';")
		usrInfo = cur2.fetchone()
		if( usrInfo is None ):
			raise moodleObjects.moodleWarning("Failed to find user information for userID: '%s'"%str(row['userid']))
			
		actor = Agent(
			name = usrInfo['firstname'] + ' ' + usrInfo['lastname'],
			account = {
				'name':			usrInfo['username'],
				'home_page': 	config.BASE_URI
			}
		)

		# Create the object
		# If it's a course view, then we create a simplified course object
		#if eventname == '\\core\\event\\course_viewed':
		#	obj = ACTIVITY_ROUTES[eventname](row['courseid'])
		# If it's a graded assessment, pass a relateduserid
		if eventname == '\\mod_assign\\event\\submission_graded':
			obj = ACTIVITY_ROUTES[eventname](row['objecttable'], row['objectid'], row['relateduserid'])
		# otherwise create a standard object
		else:
			obj = ACTIVITY_ROUTES[eventname](row['objecttable'], row['objectid'], row['contextinstanceid'])

		# Context can be built off the object
		row['object'] = obj.TYPE_EN
		context = obj.getContext(row)

		# Timestamp
		timestamp = datetime.fromtimestamp(row['timecreated']).strftime('%Y-%m-%dT%H:%M:%S') + config.TIMEZONE

		# Create a statement of information
		statement = Statement(
			actor=actor,
			verb=obj.getVerb(),
			result=obj.getResult(),
			object=obj.getObject(),
			context=context,
			timestamp=timestamp
		)

		# Commit the statement
		response = lrs.save_statement(statement)
		if not response.success:
			# TODO : Format proper error here
			responseObject = json.loads(response.data)
			logging.error("Failed to insert statement for logID: '%s' for eventname = '%s'"%(row['id'], row['eventname']))
			print statement.to_json()
			print str(responseObject['message'][0])
			sys.exit(5)

	except moodleObjects.moodleCritical as e:
		# Critical Errors cause the program to die
		e.addLogID(row['id'])
		logging.critical(e)
		# print statement.to_json()
		sys.exit(3)
		
	except moodleObjects.moodleError as e:
		# Errors can cause the program to die
		e.addLogID(row['id'])
		logging.error(e)
		if config.STRICT: sys.exit(2)

	except moodleObjects.moodleWarning as e:
		# The program will live on
		e.addLogID(row['id'])
		logging.warning(e)

	except:
		logging.exception('Critical on logID: ' + str(row['id']))
		sys.exit(4)

print "done"
print "Program Complete"
