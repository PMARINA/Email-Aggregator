from __future__ import print_function
import pickle
from email.mime.text import MIMEText
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, "html")
    if type(to) is str:
        message["bcc"] = to
    else:
        message["bcc"] = ";".join(to)
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(
        message.as_string().encode("utf-8")
    )
    return {"raw": raw_message.decode("utf-8")}


def create_draft(service, user_id, message_body):
    try:
        message = {"message": message_body}
        draft = (
            service.users()
            .drafts()
            .create(userId=user_id, body=message)
            .execute()
        )

        print(
            "Draft id: %s\nDraft message: %s"
            % (draft["id"], draft["message"])
        )

        return draft
    except Exception as e:
        print("An error occurred: %s" % e)
        return None


def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (
            service.users()
            .messages()
            .send(userId=user_id, body=message)
            .execute()
        )
        # print 'Message Id: %s' % message['id']
        return message
    except Exception as e:
        print(e)
        print("FAiled")
        # print 'An error occurred: %s' % error


def refresh_import_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service
