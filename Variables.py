INPUT_FILE = "input.txt"

BCC_TO = """
        "CTC Mailing List" <stevens_ctc_events@lists.stevens.edu>
        """

WEEKLY_SUBJECT = "This Week's Events"
WEEKLY_RECIPIENTS = """
        "CTC Mailing List" <stevens_ctc_events@lists.stevens.edu>
        """.strip()

get_event_reminder_subject = lambda event_title: f"[Stevens CTC] Event Reminder: {event_title}"

DATETIME_INPUT_FORMAT = "%Y.%m.%d %H%M"
DATETIME_OUTPUT_FORMAT = "%A, %B %d (%m/%d/%Y) at %I:%M %p"
COMMENT_CHARACTER = "#"
ZOOM_LINK = "https://stevensctc.page.link/zoom"
EVENTS_PAGE_LINK = "https://stevensctc.page.link/events"
HOME_PAGE_LINK = "https://stevensctc.page.link/home"
SLACK_LINK = "https://stevensctc.page.link/slack"
BIG_LOGO_URL = "https://i.postimg.cc/sx8hCztQ/big-logo.png"
SMALL_LOGO_URL = "https://i.postimg.cc/25pVx2DY/logo.png"
INSTA_ATSIGN_URL = "https://i.postimg.cc/435sh54B/atsign.png"
CTC_INSTA_HANDLE_URL = "https://i.postimg.cc/tgwQ6MQd/ctc-insta-handle.png"

G_CLOUD_SECRETS_FILE = "credentials.json"

# Do not change this, always send the email to ourselves and bcc anyone else
TO = """
            "CTC Mailing List" <ctc.stevens@gmail.com>
        """.strip()

FROM = """
            "Stevens CTC" <ctc.stevens@gmail.com>
""".strip()

# Begin lambdas
remove_https = lambda s: s.strip()[len("https://") :]  # chop off the `https://`

# Begin computed constants
ZOOM_LINK_TEXT = remove_https(ZOOM_LINK)
EVENTS_PAGE_LINK_TEXT = remove_https(EVENTS_PAGE_LINK)
HOME_PAGE_LINK_TEXT = remove_https(HOME_PAGE_LINK)
SLACK_LINK_TEXT = remove_https(SLACK_LINK)

temp = BCC_TO.split("\n")
temp_out = []
for e in temp:
    t = e.strip()
    if t == "":
        continue
    temp_out.append(t)
BCC_TO = "; ".join(temp_out)
