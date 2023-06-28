from typing import Any, Dict, Optional, Sequence
from syncall.sync_side import SyncSide

import pymstodo
from pymstodo import Task as MicrosoftTodoTask
from pymstodo import ToDoConnection
from item_synchronizer.types import ID

class MicrosoftTodoSide(SyncSide):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            auth_again: bool
    ):
        #super().__init__(**kargs)
        self._client_id = client_id
        self._client_secret = client_secret
        redirect_resp = "https://localhost/login/authorized"
        #if auth_again:
        auth_url = ToDoConnection.get_auth_url(client_id)
        ToDoConnection._scope = "profile email openid Tasks.ReadWrite"
        redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
        token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)
        self._todo_client = pymstodo.ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)
    
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
        return self._todo_client.get_tasks(self._todo_client.get_lists()[0])
        #raise NotImplementedError("Implement in derived")
     
    def get_item(self, item_id: ID, use_cached: bool = False) -> Optional[MicrosoftTodoTask]:
        """Get a single item based on the given UUID.
        :use_cached: False if you want to fetch the latest version of the item. True if a
        cached version would do.
        :returns: None if not found, the item in dict representation otherwise
        """
        raise NotImplementedError("Should be implemented in derived")
     
    def delete_single_item(self, item_id: ID):
        """Delete an item based on the given UUID.
        .. raises:: Keyerror if item is not found.
        """
        raise NotImplementedError("Should be implemented in derived")
     
    def update_item(self, item_id: ID, **changes):
        """Update with the given item.
        :param item_id : ID of item to update
        :param changes: Keyword only parameters that are to change in the item
        .. warning:: The item must already be present
        """
        raise NotImplementedError("Should be implemented in derived")
     
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
