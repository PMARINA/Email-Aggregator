from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.form'",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            )
            .execute()
        )
        count = 1
        for file in response.get("files", []):
            # Process change
            print("Found file: %s (%s)" % (file.get("name"), file.get("id")))
            if True:  # "java" in file.get("name").lower():
                file_id = file.get("id")
                request = service.files().export_media(
                    fileId=file_id, mimeType="application/zip"
                )
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
                with open(
                    str(count) + "_" + make_safe_filename(file.get("name")) + ".zip",
                    "wb",
                ) as f:
                    f.write(fh.getbuffer())
                count += 1

        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    # Call the Drive v3 API
    # results = (
    #     service.files()
    #     .list(pageSize=10, fields="nextPageToken, files(id, name)")
    #     .execute()
    # )
    # items = results.get("files", [])

    # if not items:
    #     print("No files found.")
    # else:
    #     print("Files:")
    #     for item in items:
    #         print(u"{0} ({1})".format(item["name"], item["id"]))


if __name__ == "__main__":
    main()
