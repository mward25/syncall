import syncall.taskwarrior as taskwarrior
from syncall.types import TwItem
from pymstodo import Task as MicrosoftTodoTask
from syncall import MicrosoftTodoSide
def priority_to_importance(importance):
    if importance == 'H':
        return 'high'
    elif importance == 'M':
        return 'normal'
    elif importance == 'L':
        return 'low'
    elif importance == '':
        return 'normal'

def importance_to_priority(priority):
    if priority == 'high':
        return 'H'
    elif priority == 'normal':
        return 'M'
    elif priority == 'low':
        return 'L'
    elif priority == None:
        return 'L'

def ms_todo_status_to_tw_status(ms_todo_status):
    if ms_todo_status == 'notStarted':
        return 'pending'
    elif ms_todo_status == 'inProgress':
        return 'pending'
    elif ms_todo_status == 'completed':
        return 'return completed'
    elif ms_todo_status == 'waitingOnOthers':
        return 'waiting'
    elif ms_todo_status == 'deferred':
        return 'deleted'
    else:
        # Other wise return pending, as this is the option that is least likely to make a users task disappear, which would be very bad for the user
        return 'pending'
def tw_status_to_ms_todo_status(tw_status):
    if tw_status ==  'pending':
        return 'inProgress'
    elif tw_status == 'completed':
        return 'completed'
    elif tw_status == 'deleted':
        return 'deferred'
    elif tw_status == 'waiting':
        return 'waiting' 
    else:
        # Other wise return inProgress, as this is the option that is least likely to make a users task disappear, which would be very bad for the user
        return 'inProgress'

# ignore categories, isReminderOn, hasAttachments, urgency, imask, parent, id, depends, wait, tags, recur, project, until  
def convert_tw_to_microsoft_todo(tw_item: TwItem) -> MicrosoftTodoSide:
    return_value = MicrosoftTodoSide()
    # return title from description
    return_value.title = tw_item['description']
    # return task_status from status
    return_value.task_status = tw_status_to_ms_todo_status(tw_item['status'])
    # return start_date from start
    return_value.start_date = tw_item['start']
    # return created_date from entry
    return_value.created_date = tw_item['entry']
    # return due_date from due
    return_value.due_date = tw_item['due']
    # return completed_date from end
    return_value.completed_date = tw_item['completed_date']
    # return last_mod_date from modified
    return_value.last_mod_date = tw_item['last_mod_date']
    # return importance from priority
    return_value.importance = priority_to_importance(tw_item['priority'])
    # add uuid  to body_text under key "uuid"
    return_value.body_text = "uuid: " + tw_item['uuid']
    return return_value

def convert_microsoft_todo_to_tw(microsoft_todo_item: MicrosoftTodoTask) -> TwItem:
    return_value = dict()
    # return title from description
    return_value['description'] = microsoft_todo_item.title
    # return task_status from status
    return_value['status'] = ms_todo_status_to_tw_status(microsoft_todo_item.task_status)
    # return start_date from start
    return_value['start'] = microsoft_todo_item.start_date
    # return created_date from entry
    return_value['entry'] = microsoft_todo_item.created_date
    # return due_date from due
    return_value['due'] = microsoft_todo_item.due_date
    # return completed_date from end
    return_value['end'] = microsoft_todo_item.completed_date
    # return last_mod_date from modified
    return_value['modified'] = microsoft_todo_item.last_mod_date
    # return importance from priority
    return_value['priority'] = importance_to_priority(microsoft_todo_item.importance)
    # add uuid  to body_text under key "uuid"
    body_text_split_tmp = microsoft_todo_item.body_text.split('uuid:')
    print('body_text_split_tmp: ', body_text_split_tmp)
    if len(body_text_split_tmp) >= 2:
        body_text_split_tmp = body_text_split_tmp[1]
        body_text_split_tmp = body_text_split_tmp.split('\n')
        return_value['uuid'] = body_text_split_tmp[0]
    return return_value

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
