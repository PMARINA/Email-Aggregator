from Reminder import Reminder
from Variables import WEEKLY_RECIPIENTS

r = Reminder(event_list=[])
r.html = """
<div><b>Hi Everyone!</b></div>
<div><br></div>
<div>The Stevens ECE Department is hosting the following events. You can add them to your calendar via the attached ics file.</div>
<div style="text-align:center"><img src="https://i.ibb.co/tzCqkZF/thumbnail-27-A300-E049-F041-A0-A167-EEF6-E6283-CC0.png" alt="ECE Event Poster (in quadrants)" border="0"></div>
"""
r.subject = "Interested in Research, Resume Building?"
r.recipients = WEEKLY_RECIPIENTS
r.create_draft()
