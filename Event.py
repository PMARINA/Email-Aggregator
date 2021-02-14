import datetime
import os
from loguru import logger
import traceback


class event:
    def __init__(self, name="", description="", sign_up_url="", occurrences=[]):
        self.name = name
        self.description = description
        self.sign_up_url = sign_up_url
        self.occurrences = occurrences

    @staticmethod
    def occurrence_to_string(occ: datetime):
        """
        Given a single datetime object, get a string that represents the
        date and time of the event, to be standardized accross all
        emails...
        """
        logger.critical(f"Got: {occ}")
        # s = occ.strftime("%A, %B %-d (%m/%d/%Y) at %-I:%M %p")
        s = occ.strftime("%A, %B %d (%m/%d/%Y) at %I:%M %p")
        logger.critical(f"Returned: {s}")
        return s

    @staticmethod
    def import_from(input_file: str, comment_character: str = "#"):
        """
        Given a filepath to a text file, import the file into a list of
        events

        Args:
            input_file: a string representing the full path to the input file
            comment_character: will only apply to comments starting at beginning of line.
        """

        def get_lines(input_file: str):
            logger.debug(f"About to read in events from {input_file}")
            lines = None
            with open(input_file) as infile:
                lines = infile.readlines()
            if validate_list(lines):
                logger.success(f"Read in {len(lines)}")
            else:
                logger.error(f"{input_file} was either empty or not found")
            return lines

        def clean_lines(lines: list, comment_character: str):
            """
            Given lines (read in from a file), clean the lines (removing whitespace), and remove commented lines
            """
            logger.debug("About to sanitize event inputs")
            lines_cleaned = []
            for line in lines:
                if not line.startswith(comment_character):
                    lines_cleaned.append(line.strip())
            lines_lost = len(lines) - len(lines_cleaned)
            if validate_list(lines_cleaned):
                logger.success(
                    f"Sanitized event inputs: lost {lines_lost} lines ({lines_lost/len(lines)*100}%)"
                )
            else:
                logger.error(
                    f"Sanitization of event inputs broken: likely no useable lines..."
                )
            return lines_cleaned

        def validate_list(a: list):
            """
            Returns if a list is None or empty
            """
            if not a:
                logger.error(f"{input_file} either empty or readlines returned None")
                return False
            else:
                return True

        def get_events(inputs: list):
            """
            Given a list of lines, this will parse out event objects and
            return a list
            """
            events = []
            i = 0
            try:
                while i < (len(inputs)):
                    event_name = inputs[i]
                    i += 1
                    event_description = inputs[i]
                    i += 1
                    event_url = inputs[i]
                    i += 1
                    occurrences = []
                    while i < len(inputs) and inputs[i] != "":
                        occurrences.append(
                            datetime.datetime.strptime(
                                inputs[i].strip(), "%Y.%m.%d %H%M"
                            )
                        )
                        i += 1
                    i += 1
                    events.append(
                        event(
                            event_name,
                            event_description,
                            event_url,
                            occurrences,
                        )
                    )
            except Exception:
                logger.error("Error attempting to read in sanitized inputs")
                logger.error(traceback.format_exc())
                return None
            return events

        lines = get_lines(input_file)
        lines = clean_lines(lines, comment_character)
        events = get_events(lines)
        if not validate_list(events):
            logger.error("Events returned either empty or None")
        return events

    def get_date_time_strings(self, occurrences=None):
        # By default, use the occurrences belonging to the event
        if not occurrences:
            occurrences = self.occurrences
        # Sometimes, we only want one occurrence...
        if type(occurrences) != list:
            occurrences = [occurrences]
        # Sort, to prevent any weirdness
        occurrences = sorted(occurrences)
        return_list = []
        for occ in occurrences:
            s = event.occurrence_to_string(occ)
            print(s)
            return_list.append(s)
        return return_list
