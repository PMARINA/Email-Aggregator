import glob
import os
import re
import shutil
import zipfile

import dns

# https://stackoverflow.com/a/21642297 for installing pydns...
from dns.resolver import query
from loguru import logger
from tqdm import tqdm


def reject(line: str, failed_list: list):
    """
    Given a line that has been rejected, do whatever with it (in this case, add it to a list and log it)
    """
    failed_list.append(line)
    logger.error(line)


email_regex = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
# From https://www.tutorialspoint.com/Extracting-email-addresses-using-regular-expressions-in-Python


def process_email(line: str, failed_list: list, domain_validity: dict):
    """
    Given a line of text, process out the email
    """
    line = line.strip().lower()
    if "@" not in line:
        reject(line, failed_list)  # Emails need to have an @
    else:
        possible_emails = email_regex.findall(line)
        if len(possible_emails) < 1:
            reject(line, failed_list)
            return
        returned_match = possible_emails[0]
        # Email address cannot possibly be shorter than 5 characters long
        while "@" not in returned_match and len(line) >= 5:
            # Sometimes the email regex matches stuff in the line before the actual email
            # When it does so, keep going until you have an 'email' with an @ in it
            line = line[len(returned_match) - 1 :]
            possible_emails = email_regex.findall(line)
            if len(possible_emails) < 1:
                reject(line, failed_list)
                return
            returned_match = possible_emails[0]
        if "@" in returned_match:  # If the loop didn't break because of >=5 condition
            # Sometimes the filter doesn't get rid of stuff before the start of email...
            while '"' in returned_match:
                returned_match = returned_match[returned_match.index('"') + 1 :]
                # Remove the start of the line up to and including "
            # Get the domain from the email
            domain = returned_match.rsplit("@", 1)[-1]
            domain_is_valid = False
            if domain in domain_validity:
                domain_is_valid = domain_validity[domain]
            else:
                try:
                    # Does the domain have a valid DNS lookup entry?
                    domain_is_valid = bool(dns.resolver.resolve(domain, "MX"))
                except dns.exception.DNSException:
                    logger.error(domain + " not valid")
                    domain_is_valid = False
                    # Don't do reject here, instead, do it in the else condition based on domain_is_valid
                domain_validity[domain] = domain_is_valid
            if domain_is_valid:
                return returned_match
            else:
                reject(line, failed_list)
        else:
            reject(line, failed_list)


def extract_emails(filename):
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()[1:]
    overall_email_set = set()
    # This is the dictionary of domains against whether or not they're valid (T/F)
    # Mostly to save time (avoid repeated lookups)
    domain_validity = {}
    # A list of lines that failed to be processed and need a human to process them
    failed_list = []

    for line in lines:
        email = process_email(line, failed_list, domain_validity)
        if email is not None:
            overall_email_set.add(email)
    for line in failed_list:
        print()
        overall_email_set.add(input("What email should we add?\n" + line + "\n").lower())
    overall_email_list = list(overall_email_set)
    overall_email_list = sorted(overall_email_list)
    return overall_email_list
