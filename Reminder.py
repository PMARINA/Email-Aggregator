from typing import List
from typing import Optional
from Event import Event
from loguru import logger
import Mail


class Reminder:
    event_list = None

    def __init__(self, event_list: List[Event]):
        self.events = event_list
        self.html = ""
        self.subject = ""
        self.recipients = ""

    @staticmethod
    def read_inputs():
        lines = None
        with open(INPUT_FILE) as infile:
            lines = infile.readlines()
        if not lines:
            logger.error(f"{INPUT_FILE} not found. exiting")
            exit(1)
        else:
            events = []
            lines_cleaned = []
            for line in lines:
                if not line.startswith(COMMENT_CHARACTER):
                    lines_cleaned.append(line.strip())
            i = 0
            while i < (len(lines_cleaned)):
                event_name = lines_cleaned[i]
                i += 1
                event_description = lines_cleaned[i]
                i += 1
                event_url = lines_cleaned[i]
                i += 1
                occurrences = []
                while i < len(lines_cleaned) and lines_cleaned[i] != "":
                    occurrences.append(datetime.strptime(lines_cleaned[i].strip(), "%Y.%m.%d %H%M"))
                    i += 1
                i += 1
                events.append(Event(event_name, event_description, event_url, occurrences))
            return events

    def create_html(self):
        logger.critical(
            "create_html is not implemented. Reminder.py is a base class and not intended to be functional"
        )
        raise NotImplementedError()

    def create_draft(self):
        if not self.html:
            raise RuntimeError("html is not yet created. Please run create_html() first.")
        if not self.subject:
            raise RuntimeError("You are likely calling this method on the abstract base class")
        Mail.create_draft(self.subject, self.html, bcc_to=self.recipients)

    def send_email(self):
        if not self.html:
            raise RuntimeError("html is not yet created. Please run create_html() first.")
        if not self.subject:
            raise RuntimeError("You are likely calling this method on the abstract base class")
        Mail.send_message(self.subject, self.html, bcc_to=self.recipients)
