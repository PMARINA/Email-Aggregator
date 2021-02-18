from loguru import logger
from Reminder import Reminder
import inflect
from Event import Event
from typing import Union, List
from Drive import get_recipients
from Variables import (
    ZOOM_LINK,
    ZOOM_LINK_TEXT,
    HOME_PAGE_LINK,
    HOME_PAGE_LINK_TEXT,
    EVENTS_PAGE_LINK,
    EVENTS_PAGE_LINK_TEXT,
    SLACK_LINK,
    SLACK_LINK_TEXT,
    BIG_LOGO_URL,
    SMALL_LOGO_URL,
    INSTA_ATSIGN_URL,
    CTC_INSTA_HANDLE_URL,
    get_event_reminder_subject,
)


class Event_Reminder(Reminder):
    def __init__(self, event=Union[List[Event], Event]):
        if isinstance(event, Event):
            event = [event]
        elif not (isinstance(event, List) and len(event) > 0 and isinstance(event[0], Event)):
            raise TypeError(
                "event provided was of incorrect type. Expected Event or a List of Events"
            )
        super().__init__(event)
        self.subject = get_event_reminder_subject(event[0].name)
        self.recipients = get_recipients(event[0].sign_up_url)

    def create_html(self):
        event = self.events[0]
        body = f"""<div style="text-align:center"><img src="{BIG_LOGO_URL}" alt="CTC Logo" width="398" height="143"><br></div>
                            <div style="text-align:center"><b>Hi Everyone!</b></div>
                            <div style="text-align:center"><br></div>
                """
        body += f"""
                            <div style="text-align:center">This is a reminder that {event.name} will be happening today, {event.get_date_time_strings()[0]} at the following Zoom link.</div>
                            <div style="text-align:center"><a href="{ZOOM_LINK}">{ZOOM_LINK_TEXT}</a></div>
                            </div><div style="text-align:center">Hope to see you there!</div>
                            """
        self.html = body
