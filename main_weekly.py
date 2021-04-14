from typing import List

from Event import Event
from Weekly_Reminder import Weekly_Reminder

events: List[Event] = Event.import_events()
wk = Weekly_Reminder(events)
wk.create_html()
wk.create_draft()
