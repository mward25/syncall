#"""Console script for notion_taskwarrior."""
import os
import sys
from typing import List
from pymstodo import Task as MicrosoftTodoTask
import oauthlib
import json

import click
#from bubop import (
#    check_optional_mutually_exclusive,
#    format_dict,
#    log_to_syslog,
#    logger,
#    loguru_tqdm_sink,
#    verbosity_int_to_std_logging_lvl,
#)
#
#from syncall import inform_about_app_extras
#
#try:
#    from syncall import NotionSide, TaskWarriorSide
#except ImportError:
#    inform_about_app_extras(["microsoft_todo", "tw"])
#
#
#from notion_client import Client  # type: ignore
#

#import tw_microsoft_todo_utils

from syncall.tw_microsoft_todo_utils import convert_tw_to_microsoft_todo
from syncall.tw_microsoft_todo_utils import convert_microsoft_todo_to_tw
from syncall import (
    Aggregator,
    __version__,
    cache_or_reuse_cached_combination,
    fetch_app_configuration,
    fetch_from_pass_manager,
    get_resolution_strategy,
    inform_about_combination_name_usage,
    list_named_combinations,
    report_toplevel_exception,
    MicrosoftTodoSide,
    TaskWarriorSide
)
from syncall.cli import (
    opt_combination,
    opt_custom_combination_savename,
    opt_list_combinations,
    opt_resolution_strategy,
    opt_tw_project,
    opt_tw_tags,
)

import pprint

#pp = pprint.PrettyPrinter(indent=4)
##
##
## CLI parsing ---------------------------------------------------------------------------------
#@click.command()
### Notion options ------------------------------------------------------------------------------
##@opt_microsoft_todo_id()
### taskwarrior options -------------------------------------------------------------------------
##@opt_tw_tags()
##@opt_tw_project()
### misc options --------------------------------------------------------------------------------
@opt_resolution_strategy()
##@opt_combination("TW", "Notion")
##@opt_list_combinations("TW", "Notion")
##@opt_custom_combination_savename("TW", "Notion")
@click.command()
@click.option("-v", "--verbose", count=True)
@click.version_option(__version__)
@opt_combination("TW", "Notion")
@opt_list_combinations("TW", "Microsoft Todo")
@opt_custom_combination_savename("TW", "Microsoft Todo")
@click.option("-t", "--token_location")
@click.option("-l", "--list_name")
@click.option("-T", "--tw-tags")
@click.option("-p", "--tw-project")
@opt_resolution_strategy()
#@click.argument('token')
#@opt_resolution_strategy()
    #token_pass_path: str
def main(verbose: int,
    combination_name: str,
    do_list_combinations: bool,
    custom_combination_savename: str,
    token_location: str,
    list_name: str,
    tw_tags: str,
    tw_project: str,
    resolution_strategy: str):
    #print("test", verbose, "token: ", token_location)
    token_file = open(token_location, "r")
    token_str = token_file.read()
    #print("token_str: ", token_str)
    client_id = token_str.split("\n")[0]
    client_secret = token_str.split("\n")[1]
    token_json = ""
    if len(token_str) >= 3:
        token_json = token_str.split("\n")[2]
    # initialize taskwarrior ------------------------------------------------------------------
    tw_side = TaskWarriorSide(tags=tw_tags, project=tw_project)

    # initialize microsoft_todo ----------------------------------------------------------------
    microsoft_todo_side = None
    try:
        write_token = False
        if token_json == "":
            write_token = True
        microsoft_todo_side = MicrosoftTodoSide(client_id=client_id, client_secret=client_secret, token=token_json, list_name=list_name)
        token_json = microsoft_todo_side.start()
        if write_token:
            token_file.close()
            token_file = open(token_location, "w")
            token_file.write(client_id + "\n" + client_secret + "\n" + token_json)
            token_file.close()
            # Re-open as read only, just in case other parts of the script want to read from the file
            token_file = open(token_location, "r")
    except oauthlib.oauth2.rfc6749.errors.InvalidClientIdError:
        #token_str = client_id + "\n" + client_secret + "\n" 
        #client_id = token_str.split("\n")[0]
        #client_secret = token_str.split("\n")[1]
        token_json = ""
        
        microsoft_todo_side = MicrosoftTodoSide(client_id=client_id, client_secret=client_secret, token=token_json, list_name=list_name)
        token_json = microsoft_todo_side.start()
        token_file.close()
        token_file = open(token_location, "w")
        token_str = client_id + "\n" + client_secret + "\n" + json.dumps(token_json)
        token_file.write(token_str)
        token_file.close()
        # Re-open as read only, just in case other parts of the script want to read from the file
        token_file = open(token_location, "r")
    # sync ------------------------------------------------------------------------------------
    # ignore categories, isReminderOn, hasAttachments, urgency, imask, parent, id, depends, wait, tags, recur, project, until  
    try:
        with Aggregator(
            side_A=microsoft_todo_side,
            side_B=tw_side,
            converter_B_to_A=convert_tw_to_microsoft_todo,
            converter_A_to_B=convert_microsoft_todo_to_tw,
            resolution_strategy=get_resolution_strategy(
                resolution_strategy, side_A_type=type(microsoft_todo_side), side_B_type=type(tw_side)
            ),
            config_fname=combination_name,
            ignore_keys=(
                ('task_id', 'categories', 'isReminderOn', 'hasAttachments'),
                ('urgency', 'imask', 'parent', 'id', 'depends', 'wait', 'tags', 'recur', 'project', 'until'),
            ),
        ) as aggregator:
            aggregator.sync()
    except KeyboardInterrupt:
        logger.error("Exiting...")
        return 1
    except:
        report_toplevel_exception(is_verbose=verbose >= 1)
        return 1

    #if inform_about_config:
    #    inform_about_combination_name_usage(combination_name)


    # Old tests: 
    """
    all_items = microsoft_todo_side.get_all_items()
    print("Get All items: ", all_items, "\n\n")
    print("Getting one item: ", microsoft_todo_side.get_item(item_id=all_items[1].task_id), "\n\n")
    print("Deleting one item: ", microsoft_todo_side.get_item(item_id=all_items[1].task_id), "\n\n")
    microsoft_todo_side.delete_single_item(item_id=all_items[1].task_id)

    # Update our all_items variable so we don't have the deleted value any more
    all_items = microsoft_todo_side.get_all_items()
    print("Updating task: ", all_items[1])
    microsoft_todo_side.update_item(item_id=all_items[1].task_id, title="NEW_TITLE_THAT_IS_SUPER_COOL")
    new_item1 = microsoft_todo_side.add_item(item=MicrosoftTodoTask(title="test_title"))
    print("added task test_title")

    # Update our all_items variable so we don't have the deleted value any more
    all_items = microsoft_todo_side.get_all_items()

    print("Testing items_are_identical, Items should be identical")

    new_item2 = microsoft_todo_side.add_item(item=MicrosoftTodoTask(title="test_title"))

    if microsoft_todo_side.items_are_identical(item1=new_item1, item2=new_item2, ignore_keys=["task_id", "created_date", "createdDateTime", "last_mod_date", "lastModifiedDateTime"]):
        print("items where identical :)")
    else:
        print("items where not identical :(")
    print("Testing items_are_identical, Items should NOT be identical")

    if microsoft_todo_side.items_are_identical(item1=new_item1, item2=new_item2, ignore_keys=["task_id"]):
        print("items where identical :(")
    else:
        print("items where not identical :)")
    """

    

    token_file.close()
#def main(
#    microsoft_todo_id: str,
#    tw_tags: List[str],
#    tw_project: str,
#    token_pass_path: str,
#    resolution_strategy: str,
#    verbose: int,
#    combination_name: str,
#    custom_combination_savename: str,
#    do_list_combinations: bool,
#):
#    """Synchronise filters of TW tasks with the to_do items of Notion pages
#
#    The list of TW tasks is determined by a combination of TW tags and TW project while the
#    microsoft_todo tasks should be provided by their URLs.
#    """
#    # setup logger ----------------------------------------------------------------------------
#    loguru_tqdm_sink(verbosity=verbose)
#    log_to_syslog(name="tw_notion_sync")
#    logger.debug("Initialising...")
#    inform_about_config = False
#
#    if do_list_combinations:
#        list_named_combinations(config_fname="tw_notion_configs")
#        return 0
#
#    # cli validation --------------------------------------------------------------------------
#    check_optional_mutually_exclusive(combination_name, custom_combination_savename)
#    combination_of_tw_project_tags_and_notion_page = any(
#        [
#            tw_project,
#            tw_tags,
#            microsoft_todo_id,
#        ]
#    )
#    check_optional_mutually_exclusive(
#        combination_name, combination_of_tw_project_tags_and_notion_page
#    )
#
#    # existing combination name is provided ---------------------------------------------------
#    if combination_name is not None:
#        app_config = fetch_app_configuration(
#            config_fname="tw_notion_configs", combination=combination_name
#        )
#        tw_tags = app_config["tw_tags"]
#        tw_project = app_config["tw_project"]
#        microsoft_todo_id = app_config["microsoft_todo_id"]
#
#    # combination manually specified ----------------------------------------------------------
#    else:
#        inform_about_config = True
#        combination_name = cache_or_reuse_cached_combination(
#            config_args={
#                "microsoft_todo_id": microsoft_todo_id,
#                "tw_project": tw_project,
#                "tw_tags": tw_tags,
#            },
#            config_fname="tw_notion_configs",
#            custom_combination_savename=custom_combination_savename,
#        )
#
#    # at least one of tw_tags, tw_project should be set ---------------------------------------
#    if not tw_tags and not tw_project:
#        raise RuntimeError(
#            "You have to provide at least one valid tag or a valid project ID to use for"
#            " the synchronization"
#        )
#
#    # more checks -----------------------------------------------------------------------------
#    if microsoft_todo_id is None:
#        logger.error(
#            "You have to provide the page ID of the Notion page for synchronization. You can"
#            " do so either via CLI arguments or by specifying an existing saved combination"
#        )
#        sys.exit(1)
#
#    # announce configuration ------------------------------------------------------------------
#    logger.info(
#        format_dict(
#            header="Configuration",
#            items={
#                "TW Tags": tw_tags,
#                "TW Project": tw_project,
#                "Notion Page ID": microsoft_todo_id,
#            },
#            prefix="\n\n",
#            suffix="\n",
#        )
#    )
#
#    # find token to connect to notion ---------------------------------------------------------
#    api_key_env_var = "NOTION_API_KEY"
#    token_v2 = os.environ.get(api_key_env_var)
#    if token_v2 is not None:
#        logger.debug("Reading the Notion API key from environment variable...")
#    else:
#        if token_pass_path is None:
#            logger.error(
#                "You have to provide the Notion API key, either via the"
#                f" {api_key_env_var} environment variable or via the UNIX Passowrdr Manager"
#                ' and the "--token-pass-path" CLI parameter'
#            )
#            sys.exit(1)
#        token_v2 = fetch_from_pass_manager(token_pass_path)
#
#    assert token_v2
#
#    # initialize taskwarrior ------------------------------------------------------------------
#    tw_side = TaskWarriorSide(tags=tw_tags, project=tw_project)
#
#    # initialize notion -----------------------------------------------------------------------
#    # client is a bit too verbose by default.
#    client_verbosity = max(verbose - 1, 0)
#    client = Client(
#        auth=token_v2, log_level=verbosity_int_to_std_logging_lvl(client_verbosity)
#    )
#    notion_side = NotionSide(client=client, page_id=microsoft_todo_id)
#    microsoft_todo_side = MicrosoftTodoSide(client=client, page_id=microsoft_todo_side)
#    print(microsoft_todo_side.get_all_items())
#
#
#    return 0


if __name__ == "__main__":
    sys.exit(main())
