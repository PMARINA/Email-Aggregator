from typing import List

from Event import Event
from Event_Reminder import Event_Reminder

events: List[Event] = Event.import_events()
wk = Event_Reminder(events)
wk.create_html()
wk.create_draft()
