import glob
import io
import pickle
import re
import shutil
import zipfile
from os import remove, rename
from os.path import exists

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import EmailParser

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


def get_recipients(url):
    # logger.debug(f"Attempting to find final url for {url}")
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    form_name = ""
    form_id = ""
    try:
        element = WebDriverWait(driver, 10).until(EC.url_contains("docs.google.com/forms/"))
    finally:
        form_name = driver.title
        # logger.debug(f"Form Name: {form_name}")
        driver.quit()
    # We have the form name...
    svc = get_service()
    response = (
        svc.files()
        .list(
            q="mimeType='application/vnd.google-apps.form'",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=None,
        )
        .execute()
    )
    for file in response.get("files", []):
        if file.get("name") == form_name:
            form_id = file.get("id")
    if not form_id:
        raise RuntimeError(
            "Form ID not found given name... is the form in the drive and shared with this account?"
        )
    # We have form id
    fh = io.BytesIO()
    request = svc.files().export_media(fileId=form_id, mimeType="application/zip")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    zipname = "form.zip"
    csvname = "form.csv"
    workdir = "temp"
    with open(zipname, "wb") as f:
        f.write(fh.getbuffer())
    with zipfile.ZipFile(zipname, "r") as zipobj:
        file_name_list = zipobj.namelist()  # List of files in zip file
        for filename_from_zip in file_name_list:
            # If any file in the zip (whether it's in another folder, doesn't
            # matter), ends in csv, pull it
            if filename_from_zip.endswith(".csv"):
                zipobj.extract(filename_from_zip, workdir)
    fname = glob.glob(f"{workdir}/*.csv")[0]
    rename(fname, f"{workdir}/{csvname}")
    emails = EmailParser.extract_emails(f"{workdir}/{csvname}")
    emails_str = "\n".join(emails)
    logger.info(f"{len(emails)} emails were extracted:\n{emails_str}")
    for d in [zipname, "geckodriver.log"]:
        try:
            remove(d)
        except Exception:
            print("Failed to remove file: " + str(d))
    for d in [workdir]:
        try:
            shutil.rmtree(d)
        except:
            print("Failed to remove folder: " + str(d))

    return emails


def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if exists("token.pickle"):
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
    return service
