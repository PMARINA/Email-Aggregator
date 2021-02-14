import os
import traceback
from loguru import logger
from datetime import *
from Event import event
from Reminder import get_email, write_email
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
                while i < len(lines_cleaned) and lines_cleaned[i].strip() != "":
                    occurrences.append(
                        datetime.strptime(lines_cleaned[i].strip(), "%Y.%m.%d %H%M")
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


def get_events_to_remind(events, how_far_ahead):
    ret_dict = {}
    for event in events:
        for occ in event.occurrences:
            date_to_remind = datetime.now() + how_far_ahead
            if occ < date_to_remind:
                ret_dict[occ] = event
    return ret_dict


def main():
    global INPUT_FILE, SEND
    cwd = os.path.dirname(os.path.realpath(__file__))
    logger.debug(cwd)
    INPUT_FILE = os.path.join(cwd, INPUT_FILE)
    parse_csvs()
    os.chdir(cwd)
    events = read_inputs()
    how_far_ahead = timedelta(days=1)
    event_dict = get_events_to_remind(events, how_far_ahead)
    event, occurrence = None, None
    if not event_dict:
        logger.error(f"No events are in the next {how_far_ahead}")
        exit(1)
    elif len(event_dict) > 1:
        logger.info("There are multiple events we need to remind: which one?")
        counter = 1
        for dt, event in event_dict.items():
            print(f"{counter}: {event.name} on {event.get_date_time_strings(dt)}")
            counter += 1
        num = int(input())
        while num < 1 or num > len(event_dict):
            logger.error("Bad input")
            num = int(input())
        dict_item = tuple(list(event_dict.items())[num - 1])
        event = dict_item[1]
        occurrence = dict_item[0]
    elif len(event_dict) == 1:
        dict_item = tuple(list(event_dict.items())[0])
        event = dict_item[1]
        occurrence = dict_item[0]
    else:
        logger.error("We should never have gotten here")
        exit(1)

    mailing_list = read_mailing_list()
    if not SEND:
        write_email(event, occurrence)
        logger.debug("SEND was False. Wrote email to disk... terminating")
    else:
        html_message = get_email(event, occurrence)
        service = Mail.refresh_import_credentials()
        message = Mail.create_message(
            "me",
            mailing_list,
            f"[Stevens CTC] Event Reminder: {event.name}",
            html_message,
        )
        Mail.create_draft(service, "me", message)
        logger.success("Email(s) sent")


if __name__ == "__main__":
    main()
