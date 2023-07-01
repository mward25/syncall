import syncall.taskwarrior as taskwarrior
from syncall.types import TwItem
from pymstodo import Task as MicrosoftTodoTask
from syncall import MicrosoftTodoSide

def convert_tw_to_microsoft_todo(tw_item: TwItem) -> MicrosoftTodoSide:
    returnValue = MicrosoftTodoSide()
    # return title from description
    # return task_status from status
    # return start_date from start
    # return created_date from entry
    # return due_date from due
    # return completed_date from end
    # return last_mod_date from modified
    # return importance from priority
    # add uuid  to body_text under key "uuid"
    pass

def convert_microsoft_todo_to_tw(microsoft_todo_item: MicrosoftTodoTask) -> TwItem:
    pass

# add depends  to body_text under key "depends"
# add wait  to body_text under key "wait"
# add tags  to body_text under key "tags"
# add recur  to body_text under key "recur"
# add project  to body_text under key "project"
# add until  to body_text under key "until"
# ignore categories, isReminderOn, hasAttachments, urgency, imask, parent, id
# add annotations minus reminderDateTime to body_text under key "annotations"
# return reminder_date from annotations[reminderDateTime]





# return completed_date from entry
# return start_date from start
# return task_status from status
# return last_mod_date from modified
# return completed_date from end
# return due_date from due
# return title from description
# return importance from priority
# return reminder_date from annotations[reminderDateTime]
# add annotations minus reminderDateTime to body_text under key "annotations"
# add depends  to body_text under key "depends"
# add uuid  to body_text under key "uuid"
# add wait  to body_text under key "wait"
# add tags  to body_text under key "tags"
# add recur  to body_text under key "recur"
# add project  to body_text under key "project"
# add until  to body_text under key "until"
# ignore categories, isReminderOn, hasAttachments, urgency, imask, parent, id
