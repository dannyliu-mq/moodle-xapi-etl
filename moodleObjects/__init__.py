"""
Custom object library for Moodle objects before passing them into
the LRS (Learning Record Store).
"""

from ModuleViewed import ModuleViewed
# from SubModuleViewed import SubModuleViewed
from Course import Course
from AssignmentGraded import AssignmentGraded
from AssignmentSubmitted import AssignmentSubmitted
from AttemptSubmitted import AttemptSubmitted
from AttemptAbandoned import AttemptAbandoned
# from AttemptReviewed import AttemptReviewed
from AttemptStarted import AttemptStarted
from CourseViewed import CourseViewed
from DiscussionCreated import DiscussionCreated
from DiscussionViewed import DiscussionViewed
from PostCreated import PostCreated
# from EnrolmentCreated import EnrolmentCreated
# from QuestionSubmitted import QuestionSubmitted
from ScormLaunched import ScormLaunched
from UserLoggedIn import UserLoggedIn
from UserLoggedOut import UserLoggedOut
from UserRegistered import UserRegistered
from moodleErrors import moodleCritical
from moodleErrors import moodleError
from moodleErrors import moodleWarning

from ConversationViewed import ConversationViewed