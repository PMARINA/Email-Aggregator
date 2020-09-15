# Instructions:
# pip install loguru tqdm
# Place all csv files and/or zip files containing csv files in the same directory as this file.
# Run this script
# If/when prompted, add the correct email.
# Check PMARINA_Email_Aggregator/output.txt for the final list of emails

# Future Improvements: Use telnet to verify that the email addresses are valid with the domain.
# Why don't we do this right now?
# It looks like many ISPs block port 25 (telnet)
# Apparently there's a python library for this? Need to test

import glob
import os
from loguru import logger
from tqdm import tqdm
# This is a terrible regex replacement, in future, just make your own regex \/
from email.utils import parseaddr
from dns.resolver import query
import dns
import shutil
import zipfile


'''
Given a line that has been rejected, do whatever with it (in this case, add it to a list and log it)
'''


def reject(line: str, failed_list: list):
    failed_list.append(line)
    logger.error(line)


'''
Given a line of text, process out the email
'''


def process_email(line: str, failed_list: list, domain_validity: dict):
    line = line.strip().lower()
    if "@" not in line:
        reject(line, failed_list)  # Emails need to have an @
    else:
        returned_match = parseaddr(line)[1]
        # Email address cannot possibly be shorter than 5 characters long
        while "@" not in returned_match and len(line) >= 5:
            # Sometimes the email regex matches stuff in the line before the actual email
            # When it does so, keep going until you have an 'email' with an @ in it
            line = line[len(returned_match)-1:]
            returned_match = parseaddr(line)[1]
        if "@" in returned_match:  # If the loop didn't break because of >=5 condition
            # Sometimes the filter doesn't get rid of stuff before the start of email...
            while "\"" in returned_match:
                returned_match = returned_match[returned_match.index(
                    "\"")+1:]
                # Remove the start of the line up to and including "
            # Get the domain from the email
            domain = returned_match.rsplit('@', 1)[-1]
            domain_is_valid = False
            if domain in domain_validity:
                domain_is_valid = domain_validity[domain]
            else:
                try:
                    # Does the domain have a valid DNS lookup entry?
                    domain_is_valid = bool(dns.resolver.resolve(domain, 'MX'))
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


def create_and_empty_working_directory(workdir):
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
    else:
        os.mkdir(work_dir)


def copy_all_csvs_into_working_directory(counter, wd_path):
    csv_files_in_cwd = glob.glob("*.csv")
    logger.debug(csv_files_in_cwd)
    for csv_file in csv_files_in_cwd:
        newfp = '/'.join([wd_path, str(counter) + ".csv"])
        counter += 1
        # Copy the csv file in and rename it to a number to prevent collisions
        # with csv files of the same name, from zip files.
        shutil.copyfile(csv_file, newfp)
    return counter


def extract_all_zips_into_working_directory(counter, wd_path):
    zip_files_in_cwd = glob.glob("*.zip")
    for zipfilename in zip_files_in_cwd:
        with zipfile.ZipFile(zipfilename, 'r') as zipobj:
            file_name_list = zipobj.namelist()  # List of files in zip file
            for filename_from_zip in file_name_list:
                # If any file in the zip (whether it's in another folder, doesn't
                # matter), ends in csv, pull it
                if filename_from_zip.endswith(".csv"):
                    newfp = '/'.join([wd_path, str(counter) + ".csv"])
                    counter += 1
                    # This will break if there's a file of the same name (numbered csv files in the zip)
                    zipobj.extract(filename_from_zip)
                    os.rename(filename_from_zip, newfp)
    return counter


def read_csv_files_in_cwd():
    csv_files_in_work_directory = glob.glob("*.csv")
    logger.debug(csv_files_in_work_directory)
    combined_lines = []
    for file in tqdm(csv_files_in_work_directory):
        f = open(file)
        filelines = f.readlines()
        filelines.remove(filelines[0])  # Remove the csv header
        combined_lines.extend(filelines)
        f.close()
    return combined_lines


if __name__ == "__main__":
    # Get the path of the file being run without the file at the end of the path (get containing folder)\
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)
    work_dir = '/'.join([cwd, "PMARINA_Email_Aggregator"])

    logger.debug("Attempting to initialize working directory: " + work_dir)
    create_and_empty_working_directory(work_dir)
    logger.success("Created Work Directory")

    file_counter = 1
    logger.debug("About to copy CSV files into working directory")
    file_counter = copy_all_csvs_into_working_directory(file_counter, work_dir)
    logger.success("All CSV files copied into working directory")

    logger.debug(
        "About to extract all zip files in WD if they contain CSV files")
    file_counter = extract_all_zips_into_working_directory(
        file_counter, work_dir)
    logger.success("All zip files extracted accordingly")

    email_output_file = open("output.txt", 'w')
    # Create an empty set for emails, as sets don't allow duplicate items
    overall_email_set = set()
    # This is essentially a list of every line that matches the input filetype (all csv files)
    combined_lines_from_input_files = []
    # This is the dictionary of domains against whether or not they're valid (T/F)
    # Mostly to save time (avoid repeated lookups)
    domain_validity = {}
    # A list of lines that failed to be processed and need a human to process them
    failed_list = []

    os.chdir(work_dir)
    logger.debug("Reading in all files")
    combined_lines_from_input_files = read_csv_files_in_cwd()
    logger.success("Read in all files")

    logger.debug("Starting to process all ingested data")
    for line in tqdm(combined_lines_from_input_files):
        email = process_email(line, failed_list, domain_validity)
        if email is not None:
            overall_email_set.add(email)
    logger.success("Processed all ingested data")

    logger.debug("About to process failed lines")
    for line in tqdm(failed_list):
        print()
        overall_email_set.add(
            input("What email should we add?\n" + line + "\n").lower())
    logger.success("Processed failed lines")

    logger.debug("Starting dump from set to output.txt")
    overall_email_list = list(overall_email_set)
    overall_email_list = sorted(overall_email_list)
    for email_string in tqdm(overall_email_list):
        email_output_file.write(email_string + "\n")
    logger.success("Wrote emails out")
    email_output_file.close()
