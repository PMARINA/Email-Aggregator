from Weekly_Reminder import Weekly_Reminder
from Event import Event
from typing import List

events: List[Event] = Event.import_events()
wk = Weekly_Reminder(events)
wk.create_html()
wk.create_draft()
