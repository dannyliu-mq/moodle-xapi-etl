#
# This is the main Moodle xAPI etl configuration file. It contains the
# configuration that gives the client its instructions.
#
# You will need to fill out almost all of this configuration file for
# the program to work properly.



# Verbose
# Controls how much output the importer will push to screen.
VERBOSE			= False

# Testing
# Toggles a testing flag to push testing data.
# This should not be used
TESTING			= False

# Strict
# Whether to stop on WARNING level errors.
STRICT			= True

# BASE_URI
# The url to the Moodle instance. This should NOT include the
# trailing forward slash.
BASE_URI		= ""

# LRS_URI
# The url to the LRS instance. This should NOT include the trailing
# forward slash
LRS_URI			= ""

# DB_HOST
# Hostname for the MongoDB
DB_HOST			= ""

# DB_USER
# The username for the MongoDB
DB_USER			= ""

# DB_PASS
# The password for the MongoDB
DB_PASS			= ""

# DB_NAME
# The database name for the MongoDB
DB_NAME 		= ""

# MOODLE_PREFIX
# The prefix of the moodle tables in the database
MOODLE_PREFIX 	= "mdl_"

# TIMEZONE
# Timezone string showing the offset from +0:00
TIMEZONE 		= "+10:00"

# ITER_SIZE
# How many records to pull from the MongoDB
ITER_SIZE 		= 10000

# LRS_COLLECTION
# The collection inside the mongoDB
LRS_COLLECTION 	= "learninglocker"

# LRS_ENDPOINT
# Endpoint of the LRS service
LRS_ENDPOINT 	= ""

# LRS_VERSION
# Version of the statement, must be one of
# 1.0.1 | 1.0.0 | 0.95 | 0.9
LRS_VERSION 	= "1.0.0"

# LRS_ID
# ID of the LRS, this is used to resume an importing process in the
# case of a critical error
LRS_ID			= ""

# LRS_USERNAME
# Client username from LearningLocker
LRS_USERNAME	= ""

# LRS_PASSWORD
# Client password from LearningLocker
LRS_PASSWORD	= ""


# Logging settings
# These settings are based off the python logging module. The main
# option that you might want to change here is the logging level.
logging.basicConfig(
	filename='logs/' + str(int(time.time())) + '.log'
	,format='%(asctime)s %(levelname)s: %(message)s'
	,datefmt='%Y-%m-%d %H:%M:%S'
	,filemod='w'
	,level=logging.ERROR,
)

# VERSION
# Version of the importing tool
VERSION = "0.6.2"


