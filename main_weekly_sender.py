import os
import traceback
from loguru import logger
from datetime import datetime
from Event import event
from Weekly_Reminder import get_email, write_email
import Mail
from main import main as parse_csvs

INPUT_FILE = "input.txt"
COMMENT_CHARACTER = "#"
SEND = True


def read_inputs():
    global SEND
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
                lines_cleaned.append(line)
        i = 0
        try:
            while i < (len(lines_cleaned)):
                event_name = lines_cleaned[i].strip()
                i += 1
                event_description = lines_cleaned[i].strip()
                i += 1
                event_url = lines_cleaned[i].strip()
                i += 1
                occurrences = []
                while (
                    i < len(lines_cleaned)
                    and lines_cleaned[i].strip() != ""
                ):
                    occurrences.append(
                        datetime.strptime(
                            lines_cleaned[i].strip(), "%Y.%m.%d %H%M"
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
            logger.error(f"Something went wrong reading in {INPUT_FILE}")
            logger.error(traceback.format_exc())
            SEND = False
        return events


def read_mailing_list(infile="output.txt"):
    ret = None
    with open(infile) as f:
        ret = f.readlines()
        for s in range(len(ret)):
            ret[s] = ret[s].strip()
    return ret


def main():
    global INPUT_FILE, SEND
    cwd = os.path.dirname(os.path.realpath(__file__))
    INPUT_FILE = os.path.join(cwd, INPUT_FILE)
    parse_csvs()
    events = read_inputs()
    mailing_list = read_mailing_list()
    if not SEND:
        write_email(events)
    else:
        html_message = get_email(events)
        service = Mail.refresh_import_credentials()
        message = Mail.create_message(
            "me",
            mailing_list,
            "[Stevens CTC] This Week's Events",
            html_message,
        )
        Mail.send_message(service, "me", message)


if __name__ == "__main__":
    main()
