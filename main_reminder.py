from Event_Reminder import Event_Reminder
from Event import Event
from typing import List

events: List[Event] = Event.import_events()
wk = Event_Reminder(events)
wk.create_html()
wk.create_draft()
