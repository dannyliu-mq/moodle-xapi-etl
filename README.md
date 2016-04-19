#Macquarie Open Analytics Toolkit - Moodle xAPI importer

This tool reads from the Moodle database and ETLs (extracts, transforms, and loads) the data into xAPI-compliant statements, stored in a Learning Record Store.

This tool is part of the larger Macquarie Open Analytics Toolkit (MOAT) project at Macquarie University in Sydney, Australia. The MOAT project seeks to address learning analytics holistically, bringing together data from the learning management system and beyond, combining visualisations and data modelling techniques with pedagogical insight and a customisable intervention engine to help staff improve the learning experience for students.

##Technical details

The importer reads events from the Moodle logstore_standard_log table (Moodle version 2.7+), translates the information into a standard format and passes it to a LRS for validation and storage.

#Requirements

* LearningLocker
* Moodle (postgres database)
* MonogDB

#Installation
##Installation for Ubuntu
1. For good practice, `apt-get update`
2. `apt-get upgrade`
3. Clone the repo: `git clone https://github.com/dannyliu-mq/moodle-xapi-etl`
4. Install psycopg2: `apt-get install python-psycopg2`
5. Install easy_install: `apt-get install python-setuptools python-dev build-essential`
6. Install pytz: `easy_install --upgrade pytz`
7. Install aniso8601: `easy_install --upgrade aniso8601`
8. Install pymongo: `easy_install --upgrade pymongo`

#Usage

To run the importer, you will need to setup a config file.
There is an example config file included with the repository.
Create a copy of the file `cp config.dist.py config.py`
Edit the file to suit your systems, more assistance is in the file.
Finally to run the program, `./importer.py` will run the program however as it may take many hours (or days) to run, depending on the amount of records, we suggest installing screen program to allow users to leave a ssh session while running it in a resumable screen.

#Related projects

Macquarie Open Analytics Toolkit - https://github.com/dannyliu-mq/moat

#References

This importer is structurally based on the moodle-logstore_xapi (https://github.com/jlowe64/moodle-logstore_xapi) Moodle plugin developed by Learning Locker (https://learninglocker.net/blog/say-hello-to-our-little-plugin/)

Experience API (xAPI) specification: https://github.com/adlnet/xAPI-Spec/blob/master/xAPI.md

#Credits

* Code: Ed Moore (ed.moore@mq.edu.au) and Yvonne-Noemi Nemes (yvonne.nemes@mq.edu.au)
* Concept: Danny Liu (danny.liu@mq.edu.au) and James Hamilton
* Funding: Macquarie University
