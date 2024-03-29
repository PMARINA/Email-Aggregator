import base64
import pickle
from email.mime.text import MIMEText
from os.path import exists as file_exists
from typing import Iterable, List, Union, Dict

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from loguru import logger

from Variables import BCC_TO, FROM, G_CLOUD_SECRETS_FILE, TO

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def create_message(
    subject: str,
    html: str,
    sender: str,
    bcc_to: Union[str, Iterable] = "",
    to: Union[str, Iterable] = "",
) -> Dict[str, str]:
    """Create a json object representing a message.

    Args:
        subject (str): The subject of the email
        html (str): The HTML string representing the body of the email
        sender (str): From whom is the email being sent?
        bcc_to (Union[str, Iterable]): The BCC-to field (can be blank, just submit `""`)
        to (Union[str, Iterable]): The To field (can be blank, just submit `""`)

    Returns:
        Dict[str, str]: [description]
    """
    message = MIMEText(html, "html")
    if type(bcc_to) is str:
        message["bcc"] = bcc_to
    elif hasattr(to, "__iter__"):
        message["bcc"] = "; ".join(bcc_to)
    else:
        pass

    if type(to) is str:
        message["to"] = to
    elif hasattr(to, "__iter__"):
        message["to"] = "; ".join(to)
    else:
        pass

    message["from"] = sender
    message["subject"] = subject

    if not message["bcc"] and not message["to"]:
        logger.warning("No BCC or TO recipient specified.")

    raw_message: bytes = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {"raw": raw_message.decode("utf-8")}


def create_draft(subject, html, sender=FROM, bcc_to=BCC_TO, to=TO, user_id="me"):
    message = {"message": create_message(subject, html, sender, bcc_to, to)}
    _ = get_service().users().drafts().create(userId=user_id, body=message).execute()


def send_message(subject, html, sender=FROM, bcc_to=BCC_TO, to=TO, user_id="me"):
    get_service().users().messages().send(
        userId=user_id, body=create_message(subject, html, sender, bcc_to, to)
    ).execute()


def get_service() -> Resource:
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if file_exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(G_CLOUD_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service: Resource = build("gmail", "v1", credentials=creds)
    return service
