#import datetime
#
#from typing import Any, Mapping, Optional
#
#"""
#            "@odata.etag": "W/\"inlZ3v/HfEKHI4RZNx9RFAAC5qiZOQ==\"",
#            "importance": "normal",
#            "isReminderOn": false,
#            "status": "notStarted",
#            "title": "Mount 2 drives to be searched by Josh",
#            "createdDateTime": "2023-06-25T16:53:28.0283733Z",
#            "lastModifiedDateTime": "2023-06-26T15:02:17.4230543Z",
#            "hasAttachments": false,
#            "categories": [],
#            "id": "AQMkADAwATM0MDAAMS0yNzRmLWQxZjQtMDACLTAwCgBGAAADUaLGNp8M60W4FQEdV6wGCQcAinlZ3v-HfEKHI4RZNx9RFAAC5qnJBgAAAIp5Wd7-x3xChyOEWTcfURQAAuaqKMwAAAA=",
#            "body": {
#                "content": "",
#                "contentType": "text"
#            },
#            "dueDateTime": {
#                "dateTime": "2023-06-27T00:00:00.0000000",
#                "timeZone": "UTC"
#            },
#            "recurrence": {
#                "pattern": {
#                    "type": "daily",
#                    "interval": 3,
#                    "month": 0,
#                    "dayOfMonth": 0,
#                    "daysOfWeek": [],
#                    "firstDayOfWeek": "sunday",
#                    "index": "first"
#                },
#                "range": {
#                    "type": "noEnd",
#                    "startDate": "2023-06-29",
#                    "endDate": "0001-01-01",
#                    "recurrenceTimeZone": "UTC",
#                    "numberOfOccurrences": 0
#                }
#"""
#
#class MicrosoftTodoTaskRecurrence(Mapping):
#    pattern_type: str
#    interval: int
#    month: int
#    day_of_month: int
#    days_of_week: list
#    first_day_of_week: str
#    index: str
#
#    range_type: str
#    start_date: datetime.datetime
#    endDate: datetime.datetime
#    numberOfOccurrences: int
#
#
#class  MicrosoftTodoTask(Mapping):
#    list_id: str
#    importance: str
#    is_reminder_on: bool
#    status: str
#    title: str
#    created_date_time: datetime.datetime
#    lastModifiedDateTime: datetime.datetime
#    has_attachments: bool
#    categories: dict
#    unique_id: str
#    body: dict
#    due_date_time: datetime.datetime
#    recurrence: MicrosoftTodoTaskRecurrence
    

