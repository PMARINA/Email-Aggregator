import inflect
from loguru import logger

import Event
from Reminder import Reminder
from Mail import create_message
from Variables import (
    BIG_LOGO_URL,
    CTC_INSTA_HANDLE_URL,
    EVENTS_PAGE_LINK,
    EVENTS_PAGE_LINK_TEXT,
    HOME_PAGE_LINK,
    HOME_PAGE_LINK_TEXT,
    INSTA_ATSIGN_URL,
    SLACK_LINK,
    SLACK_LINK_TEXT,
    SMALL_LOGO_URL,
    TO,
    WEEKLY_RECIPIENTS,
    WEEKLY_SUBJECT,
    ZOOM_LINK,
    ZOOM_LINK_TEXT,
)

p = inflect.engine()


class Weekly_Reminder(Reminder):
    def __init__(self, events):
        super().__init__(events)
        self.subject = WEEKLY_SUBJECT
        self.recipients = WEEKLY_RECIPIENTS

    def create_html(self):
        event_list = self.events
        message = f"""
                        <div style="text-align:center"><img src="{BIG_LOGO_URL}" alt="CTC Logo" width="398" height="143"><br></div>
                        <div style="text-align:center"><b>Hi Everyone!</b></div>
                    """
        # Sort the event list chronologically by the first occurrence of each event.
        event_list = sorted(event_list, key=lambda e: e.occurrences[0])
        for event_number in range(len(event_list)):
            event = event_list[event_number]
            if len(event_list) > 1:
                message += f"""<div style="text-align:center"><br></div><div style="text-align:center"><b>Our {p.number_to_words(p.ordinal(event_number+1))} event this week is {event.name}</b></div>"""
            else:
                message += f"""<div style="text-align:center"><br></div><div style="text-align:center"><b>This week's event is {event.name}</b></div>"""

            message += f"""<div style="text-align:center">{event.description}</div>"""
            for occ_str in event.get_date_time_strings():
                message += f"""
                                <div style="text-align:center">{occ_str} - <a href="{ZOOM_LINK}">{ZOOM_LINK_TEXT}</a></div>
                            """
            message += f"""
                        <div style="text-align:center"><a href="{event.sign_up_url}">Sign Up!</a></div>
                        """
        # The footer of the email
        message += f"""
                        <div style="text-align:center">Hope to see you there!</div>
                        <div style="text-align:center"><br></div>
                        <div style="text-align:center">If you have any questions please feel free to reach out to us at this email and follow us on Instagram to stay up to date with announcements and future events.</div>
                        <div style="text-align:center">
                        <div><img src="{SMALL_LOGO_URL}" alt="Small Logo" width="35" height="35">
                        <img src="{INSTA_ATSIGN_URL}" alt="Instagram Atsign" width="30" height="36">
                        <img src="{CTC_INSTA_HANDLE_URL}" alt="CTC Insta Handle" width="140" height="36">
                        <img src="{SMALL_LOGO_URL}" alt="Small Logo" width="35" height="35">
                        </div>
                        <div><br></div>
                        <div>Join our slack for important announcements about events, to ask questions about previous events, and access instructors directly </div>
                            <div><a href="{SLACK_LINK}">{SLACK_LINK_TEXT}</a></div>
                            <div><br></div>
                            <div>Want to know more? Check out our website for info on who we are, all event sign-ups, contact information, and to meet your instructors! </div>
                            <div><a href="{HOME_PAGE_LINK}" >{HOME_PAGE_LINK_TEXT}</a><br></div>
                        </div>
                        <div style="text-align:center"><br></div>
                        <div style="text-align:center">Please use our website to sign up for upcoming events here: <a href="{EVENTS_PAGE_LINK}" >Sign Up!</a></div>
                        </div>
                    """
        self.html = message

    def create_draft(self):
        if not self.html:
            raise RuntimeError("html is not yet created. Please run create_html() first.")
        if not self.subject:
            raise RuntimeError("You are likely calling this method on the abstract base class")
        message = {
            "message": create_message(
                self.subject, self.html, sender, bcc_to=TO, to=WEEKLY_RECIPIENTS
            )
        }
        draft = get_service().users().drafts().create(userId=user_id, body=message).execute()

    def send_email(self):
        if not self.html:
            raise RuntimeError("html is not yet created. Please run create_html() first.")
        if not self.subject:
            raise RuntimeError("You are likely calling this method on the abstract base class")
        message = {
            "message": create_message(
                self.subject, self.html, sender, bcc_to=TO, to=WEEKLY_RECIPIENTS
            )
        }
        get_service().users().messages().send(userId=user_id, body=message).execute()
