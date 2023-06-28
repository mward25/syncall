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

def str_to_token(input_str: str):
    return ast.literal_eval(input_str)

def extract_list_with_name(name_to_get: str, input_list: list):
    for i in input_list:
        if i.displayName == name_to_get:
            return i
    return None

class MicrosoftTodoSide(SyncSide):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            token: str,
            list_name: str
    ):
        #super().__init__(**kargs)
        self._client_id = client_id
        self._client_secret = client_secret
        self._list_name = list_name
        redirect_resp = "https://localhost/login/authorized"
        ToDoConnection._scope = "profile email openid Tasks.ReadWrite Tasks.ReadWrite.Shared"
        # If the token is empty, it means that we need to authenticate to get a token
        if token == "":
            auth_url = ToDoConnection.get_auth_url(client_id)
            redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
            token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)
            print("Please put this token on the third line of your config file: ", token)
        self._token = str_to_token(token)
        self._todo_client = pymstodo.ToDoConnection(client_id=client_id, client_secret=client_secret, token=self._token)
        
        self._list_id = extract_list_with_name(self._list_name, self._todo_client.get_lists()).list_id
    
    def start(self):
        """Initialization steps.
        Call this manually. Derived classes can take care of setting up data
        structures / connection, authentication requests etc.
        """
        pass
     
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
        self._todo_client.update_task(task_id=item_id, list_id=self._list_id, **changes)
     
    def add_item(self, item: MicrosoftTodoTask) -> MicrosoftTodoTask:
        """Add a new item.
        :returns: The newly added event
        """
        raise NotImplementedError("Implement in derived")
     
    def id_key(cls) -> str:
        """
        Key in the dictionary of the added/updated/deleted item that refers to the ID of
        that Item.
        """
        raise NotImplementedError("Implement in derived")
     
    def summary_key(cls) -> str:
        """Key in the dictionary of the item that refers to its summary."""
        raise NotImplementedError("Implement in derived")
    
    def last_modification_key(cls) -> str:
        """Key in the dictionary of the item that refers to its modification date."""
        raise NotImplementedError("Implement in derived")
     
    def items_are_identical(
        cls, item1: MicrosoftTodoTask, item2: MicrosoftTodoTask, ignore_keys: Sequence[str] = []
    ) -> bool:
        """Determine whether two items are identical.
     
        .. returns:: True if items are identical, False otherwise.
        """
        raise NotImplementedError("Implement in derived")


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
