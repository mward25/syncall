from typing import Any, Dict, Optional, Sequence
import pymstodo
import json
import ast
from syncall.sync_side import SyncSide
from pymstodo import Task as MicrosoftTodoTask
from pymstodo import ToDoConnection
from item_synchronizer.types import ID
# Taken from https://www.geeksforgeeks.org/how-to-change-a-dictionary-into-a-class/
# Turns a dictionary into a class
class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

def str_to_token(input_str: str) -> dict:
    return json.loads(input_str)

def extract_list_with_name(name_to_get: str, input_list: list):
    for i in input_list:
        if i.displayName == name_to_get:
            return i
    return None
def list_has_key(the_list: Sequence, the_key: str):
    for i in the_list:
        if i == the_key:
            return True
    return False

class MicrosoftTodoSide(SyncSide):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            token: str,
            list_name: str):
        super().__init__(name="MicrosoftTodo", fullname="MicrosoftTodo")
        self._client_id = client_id
        self._client_secret = client_secret
        self._list_name = list_name
        self._token = token
        #super().__init__(**kargs)

    
    def start(self) -> str:
        """Initialization steps.
        Call this manually. Derived classes can take care of setting up data
        structures / connection, authentication requests etc.
        Returns the token
        """
        token = self._token
        client_id = self._client_id
        client_secret = self._client_secret
        list_name = self._list_name
        redirect_resp = "https://localhost/login/authorized"
        ToDoConnection._scope = "profile email openid Tasks.ReadWrite Tasks.ReadWrite.Shared"
        # If the token is empty, it means that we need to authenticate to get a token
        if token == "":
            auth_url = ToDoConnection.get_auth_url(client_id)
            redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
            token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)
            self._token = token
        elif type(token) is str:
            print("was ", type(token))
            token = json.loads(token)
            self._token = token
            print("token is now however ", type(token))
        else:
            print("was not str, but it was", type(token))
            self._token = token
        
        self._todo_client = pymstodo.ToDoConnection(client_id=client_id, client_secret=client_secret, token=self._token)
        
        self._list_id = extract_list_with_name(self._list_name, self._todo_client.get_lists()).list_id
        if type(token) is str:
            return token
        else:
            return json.dumps(token)
     
    def finish(self):
        """Finalization steps.
        Call this manually. Derived classes can take care of closing open connections, flashing
        their cached data, etc.
        """
        pass
     
    def get_all_items(self) -> Sequence[MicrosoftTodoTask]:
        """Query side and return a sequence of items
        :param kargs: Extra options for the call
        :return: A list of items. The type of these items depends on the derived class
        """
        return self._todo_client.get_tasks(list_id=self._list_id)
     
    def get_item(self, item_id: ID, use_cached: bool = False) -> Optional[MicrosoftTodoTask]:
        """Get a single item based on the given UUID.
        :use_cached: False if you want to fetch the latest version of the item. True if a
        cached version would do.
        :returns: None if not found, the item in dict representation otherwise
        """
        return self._todo_client.get_task(task_id=item_id, list_id=self._list_id)
     
    def delete_single_item(self, item_id: ID):
        """Delete an item based on the given UUID.
        .. raises:: Keyerror if item is not found.
        """
        self._todo_client.delete_task(list_id=self._list_id, task_id=item_id)
     
    def update_item(self, item_id: ID, **changes):
        """Update with the given item.
        :param item_id : ID of item to update
        :param changes: Keyword only parameters that are to change in the item
        .. warning:: The item must already be present
        """
        try:
            self._todo_client.update_task(task_id=item_id, list_id=self._list_id, **changes)
        except:
            print("problems in update_item in microsoft_todo_side 🪟 😥 ")
     
    def add_item(self, item: MicrosoftTodoTask) -> MicrosoftTodoTask:
        """Add a new item.
        :returns: The newly added event
        """
        new_task = self._todo_client.create_task(item.title, self._list_id, due_date=item.due_date, body_text=item.body_text)
        return new_task
    def id_key(cls) -> str:
        """
        Key in the dictionary of the added/updated/deleted item that refers to the ID of
        that Item.
        """
        return "task_id"
     
    def summary_key(cls) -> str:
        """Key in the dictionary of the item that refers to its summary."""
        return "title"
    
    def last_modification_key(cls) -> str:
        """Key in the dictionary of the item that refers to its modification date."""
        return "last_mod_date"
     
    def items_are_identical(
        cls, item1: MicrosoftTodoTask, item2: MicrosoftTodoTask, ignore_keys: Sequence[str] = []
    ) -> bool:
        """Determine whether two items are identical.
     
        .. returns:: True if items are identical, False otherwise.
        """
        returnValue = True
        if ( not list_has_key(ignore_keys, "body_text") ) and item1.body_text != item2.body_text:
            returnValue = False
            print("item1.", "body_text", "!= item2.", "body_text") 
        if ( not list_has_key(ignore_keys, "categories") ) and item1.categories != item2.categories:
            returnValue = False
            print("item1.", "categories", "!= item2.", "categories") 
        if ( not list_has_key(ignore_keys, "completedDateTime") ) and item1.completedDateTime != item2.completedDateTime:
            returnValue = False
            print("item1.", "completedDateTime", "!= item2.", "completedDateTime") 
        if ( not list_has_key(ignore_keys, "completed_date") ) and item1.completed_date != item2.completed_date:
            returnValue = False
            print("item1.", "completed_date", "!= item2.", "completed_date") 
        if ( not list_has_key(ignore_keys, "createdDateTime") ) and item1.createdDateTime != item2.createdDateTime:
            returnValue = False
            print("item1.", "createdDateTime", "!= item2.", "createdDateTime") 
        if ( not list_has_key(ignore_keys, "created_date") ) and item1.created_date != item2.created_date:
            returnValue = False
            print("item1.", "created_date", "!= item2.", "created_date") 
        if ( not list_has_key(ignore_keys, "due_date") ) and item1.due_date != item2.due_date:
            returnValue = False
            print("item1.", "due_date", "!= item2.", "due_date") 
        if ( not list_has_key(ignore_keys, "hasAttachments") ) and item1.hasAttachments != item2.hasAttachments:
            returnValue = False
            print("item1.", "hasAttachments", "!= item2.", "hasAttachments") 
        if ( not list_has_key(ignore_keys, "importance") ) and item1.importance != item2.importance:
            returnValue = False
            print("item1.", "importance", "!= item2.", "importance") 
        if ( not list_has_key(ignore_keys, "isReminderOn") ) and item1.isReminderOn != item2.isReminderOn:
            returnValue = False
            print("item1.", "isReminderOn", "!= item2.", "isReminderOn") 
        if ( not list_has_key(ignore_keys, "lastModifiedDateTime") ) and item1.lastModifiedDateTime != item2.lastModifiedDateTime:
            returnValue = False
            print("item1.", "lastModifiedDateTime", "!= item2.", "lastModifiedDateTime") 
        if ( not list_has_key(ignore_keys, "last_mod_date") ) and item1.last_mod_date != item2.last_mod_date:
            returnValue = False
            print("item1.", "last_mod_date", "!= item2.", "last_mod_date") 
        if ( not list_has_key(ignore_keys, "reminderDateTime") ) and item1.reminderDateTime != item2.reminderDateTime:
            returnValue = False
            print("item1.", "reminderDateTime", "!= item2.", "reminderDateTime") 
        if ( not list_has_key(ignore_keys, "reminder_date") ) and item1.reminder_date != item2.reminder_date:
            returnValue = False
            print("item1.", "reminder_date", "!= item2.", "reminder_date") 
        if ( not list_has_key(ignore_keys, "startDateTime") ) and item1.startDateTime != item2.startDateTime:
            returnValue = False
            print("item1.", "startDateTime", "!= item2.", "startDateTime") 
        if ( not list_has_key(ignore_keys, "start_date") ) and item1.start_date != item2.start_date:
            returnValue = False
            print("item1.", "start_date", "!= item2.", "start_date") 
        if ( not list_has_key(ignore_keys, "task_id") ) and item1.task_id != item2.task_id:
            returnValue = False
            print("item1.", "task_id", "!= item2.", "task_id") 
        if ( not list_has_key(ignore_keys, "task_status") ) and item1.task_status != item2.task_status:
            returnValue = False
            print("item1.", "task_status", "!= item2.", "task_status") 
        if ( not list_has_key(ignore_keys, "title") ) and item1.title != item2.title:
            returnValue = False
            print("item1.", "title", "!= item2.", "title") 
        return returnValue

        #return  item1.expires_in == item2.expires_in and item1.expires_at == item2.expires_at

#[
#    TaskList(list_id='AQMkADAwATM0MDAAMS0yNzRmLWQxZjQtMDACLTAwCgAuAAADUaLGNp8M60W4FQEdV6wGCQEAinlZ3v-HfEKHI4RZNx9RFAAAAgESAAAA', displayName='Tasks', isOwner=True, isShared=False, wellknownListName='defaultList'),
#    TaskList(
#            list_id='AQMkADAwATM0MDAAMS0yNzRmLWQxZjQtMDACLTAwCgAuAAADUaLGNp8M60W4FQEdV6wGCQEAinlZ3v-HfEKHI4RZNx9RFAAC5qnJAQAAAA==',
#            displayName='Test task',
#            isOwner=True,
#            isShared=False,
#            wellknownListName='none'),
#    TaskList(list_id='AQMkADAwATM0MDAAMS0yNzRmLWQxZjQtMDACLTAwCgAuAAADUaLGNp8M60W4FQEdV6wGCQEAinlZ3v-HfEKHI4RZNx9RFAAC4X2KDgAAAA==',
#             displayName='Flagged Emails',
#             isOwner=True,
#             isShared=False,
#             wellknownListName='flaggedEmails'),
#    TaskList(list_id='AQMkADAwATM0MDAAMS0yNzRmLWQxZjQtMDACLTAwCgAuAAADUaLGNp8M60W4FQEdV6wGCQEAinlZ3v-HfEKHI4RZNx9RFAAC5qnJBgAAAA==',
#             displayName='Miles Tasks',
#             isOwner=False,
#             isShared=True,
#             wellknownListName='none')
#]
