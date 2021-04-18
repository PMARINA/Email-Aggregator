from __future__ import annotations

from datetime import datetime
from os.path import abspath
from os.path import exists as file_exists

# Regular Expressions
from re import IGNORECASE as RE_IGNORECASE
from re import compile as re_compile
from re import match as re_match
from typing import Any, List, Optional

from Exceptions import *
from Variables import COMMENT_CHARACTER, DATETIME_INPUT_FORMAT, DATETIME_OUTPUT_FORMAT, INPUT_FILE

# Source: https://stackoverflow.com/a/7160778
url_validator = re_compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    RE_IGNORECASE,
)

is_empty_str = lambda s: len(s) == 0


class Event:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        sign_up_url: str = "",
        occurrences: List[datetime] = [],
    ):
        if not isinstance(name, str):
            raise TypeError(f"Name is of type {type(name)}, expected str")

        if not isinstance(description, str):
            raise TypeError(f"Description is of type {type(description)}, expected str")

        if not isinstance(sign_up_url, str):
            raise TypeError(f"Sign_up_url is of type {type(sign_up_url)}, expected str")
        if not re_match(url_validator, sign_up_url):
            raise URLError(f"URL does not appear to be valid")

        if not isinstance(occurrences, List):
            raise TypeError(
                f"Occurrences is of type {type(occurrences)}, expected list of datetimes"
            )
        self.name = name
        self.description = description
        self.sign_up_url = sign_up_url
        self.occurrences = occurrences

    @staticmethod
    def occurrence_to_string(occ: datetime) -> str:
        """
        Given a single datetime object, get a string that represents the
        date and time of the event, to be standardized accross all
        emails...

        Args:
            occ: a datetime object representing the when the event will occur
        """
        # s = occ.strftime("%A, %B %-d (%m/%d/%Y) at %-I:%M %p")
        # This was the linux version that is not compatible with everything.
        # See more at https://docs.python.org/3/library/datetime.html (near bottom)
        if not isinstance(occ, datetime):
            raise TypeError(f"Expected a datetime object, received: {type(occ)}")

        formatted_datetime: str = occ.strftime(DATETIME_OUTPUT_FORMAT)

        return formatted_datetime

    def get_date_time_strings(self) -> List[str]:
        """
        Transform all datetime objects for this event into a list of printable strings
        """
        return_list: List[str] = []
        for occ in self.occurrences:
            s: str = Event.occurrence_to_string(occ)
            return_list.append(s)
        return return_list

    @staticmethod
    def import_events(
        input_file: str = INPUT_FILE, comment_character: str = COMMENT_CHARACTER
    ) -> List[Event]:
        """
        Given a filepath to a text file, import the list of events

        Args:
            input_file: a string representing the full path to the input file
            comment_character: will only apply to comments starting at beginning of line.
        """

        if not isinstance(input_file, str):
            raise TypeError(f"Input_file is of type {type(input_file)}, expected str")

        if not (isinstance(comment_character, str) or (comment_character == None)):
            raise TypeError(
                f"Comment_character is of type {type(comment_character)}, expected str or None"
            )

        def get_lines(input_file: str) -> List[str]:
            """
            Given a filename, read it into memory.

            Args:
                input_file: Filepath to the input file
            """
            input_filepath: str = abspath(input_file)
            if not file_exists(input_filepath):
                raise InputError(f"File not found: {input_filepath}")

            lines: Optional[List[str]] = None
            with open(input_filepath) as f:
                lines = f.readlines()

            if not validate_list(lines):
                raise InputError(f"{input_filepath} was empty")

            return lines

        def clean_lines(lines: List[str], comment_character: str = "") -> List[str]:
            """
            Given a list of lines, return a copy having removed:
                1) leading/trailing whitespace
                2) Excessive newlines
                3) Comments

            Args:
                lines: the list of lines to parse
                comment_character: the character to use to decide if a line should be ignored

            """
            if not isinstance(lines, List):
                raise TypeError(f"Lines is of type {type(lines)}, expected List of str")

            output_lines: List[str] = []

            # Prevents having too many empty lines...
            last_line_empty: bool = True

            for line in lines:
                cleaned_line: str = line.strip()

                if last_line_empty and is_empty_str(cleaned_line):
                    # last_line_empty = True # This is implicit since it's already true...
                    continue
                elif comment_character != "" and cleaned_line.startswith(comment_character):
                    last_line_empty = True
                    continue
                elif is_empty_str(cleaned_line):
                    last_line_empty = True
                    output_lines.append(cleaned_line)
                else:
                    last_line_empty = False
                    output_lines.append(cleaned_line)

            if is_empty_str(output_lines[-1]):
                output_lines = output_lines[:-1]

            if not validate_list(output_lines):
                raise InputError(
                    f"Sanitization of event inputs yielded no lines. Is everything commented out or just whitespace?"
                )
            return output_lines

        def validate_list(a: List[Any]) -> bool:
            """
            Returns if a list is None or empty -- originally used for logging purposes
            """
            if not isinstance(a, List):
                raise TypeError(f"A is of type {type(a)}, expected List")
            if not a:
                return False
            else:
                return True

        def get_events(inputs: List[str]) -> list[Event]:
            """
            Given a list of lines, this will parse out event objects
            """
            if not isinstance(inputs, List):
                raise TypeError(f"inputs is of type {type(inputs)}, expected List[str]")
            events: List[Event] = []
            i: int = 0
            try:
                while i < (len(inputs)):
                    event_name: str = inputs[i]
                    i += 1
                    event_description: str = inputs[i]
                    i += 1
                    event_url: str = inputs[i]
                    i += 1
                    occurrences: List[datetime] = []
                    while i < len(inputs) and not is_empty_str(inputs[i]):
                        occurrences.append(datetime.strptime(inputs[i], DATETIME_INPUT_FORMAT))
                        i += 1
                    i += 1
                    events.append(
                        Event(event_name, event_description, event_url, sorted(occurrences))
                    )
            except Exception as e:
                print("Failed while parsing cleaned lines.")
                raise e
            return events

        lines: List[str] = get_lines(input_file)
        cleaned_lines: List[str] = clean_lines(lines, comment_character)
        events: List[Event] = get_events(cleaned_lines)
        if not validate_list(events):
            raise InputError("No events to return")
        return events
