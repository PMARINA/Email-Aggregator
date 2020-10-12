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
from dns.resolver import query
import dns
import shutil
import zipfile
import re
import multiprocessing

MAX_THREADS = 8
NUM_THREADS = lambda num_tasks: min(MAX_THREADS, num_tasks)
NUM_TASKS_PER_THREAD = lambda num_tasks: num_tasks / NUM_THREADS(num_tasks)
plurality = (
    lambda value, singular_case, plural_case, compare_to=2: singular_case
    if value == compare_to
    else plural_case
)
"""
Given a line that has been rejected, do whatever with it (in this case, add it to a list and log it)
"""


def reject(line: str, failed_list: list):
    failed_list.append(line)
    logger.error(line)


"""
Given a line of text, process out the email
"""

email_regex = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+")
# From https://www.tutorialspoint.com/Extracting-email-addresses-using-regular-expressions-in-Python


def lookup_domain(domain: str):
    dns.resolver.resolve(domain, "MX")


def validate_domain(domain: str, domain_validity: dict, timeout: int = 5):
    # Check domain validity
    assert timeout > 0
    if domain in domain_validity:
        if not domain_validity[domain]:
            return False
    else:
        try:
            # Does the domain have a valid DNS lookup entry?
            proc = multiprocessing.Process(
                target=lookup_domain, args=[domain]
            )
            proc.start()
            proc.join(timeout)
            if proc.is_alive():
                proc.kill()
                logger.error(
                    f"Lookup timed out for `{domain}` killing process after {timeout} seconds"
                )
                return False
        except dns.exception.DNSException:
            logger.error(domain + " not found")
            return False
        domain_validity[domain] = True
    return True


def validate_email(email_address: str, domain_validity: dict):
    if "@" not in email_address:
        return False
    domain = email_address.rsplit("@", 1)[-1]
    if not validate_domain(domain, domain_validity):
        return False
    return True


def process_email(
    line: str, failed_list: list, domain_validity: dict, valid_set: set
):
    line = line.strip()
    # emails need to be at least 5 chars long ie a@b.c, if not, don't bother...
    if len(line) < 5:
        reject(line, failed_list)
    else:
        line = line.lower()
        returned_match = email_regex.findall(line)
        # If the list is empty or None is returned, reject.
        if not returned_match:
            reject(line, failed_list)
        else:
            # User might for some reason include multiple emails in a form response...
            for email in returned_match:
                if validate_email(email, domain_validity):
                    valid_set.add(email)
                else:
                    # This could just not exist, depending on how much manual labor you want...
                    reject(email, failed_list)


def create_and_empty_working_directory(work_dir):
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
    else:
        os.mkdir(work_dir)


def get_num_lines(filepath):
    with open(filepath) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def copy_all_csvs_into_working_directory(counter, wd_path):
    num_lines = 0
    csv_files_in_cwd = glob.glob("*.csv")
    if csv_files_in_cwd:
        logger.debug("About to copy CSV files into working directory")
        if csv_files_in_cwd:
            logger.debug("\t".join(csv_files_in_cwd))
            for csv_file in csv_files_in_cwd:
                newfp = "/".join([wd_path, str(counter) + ".csv"])
                counter += 1
                # Copy the csv file in and rename it to a number to prevent collisions
                # with csv files of the same name, from zip files.
                shutil.copyfile(csv_file, newfp)
                num_lines += get_num_lines(newfp)
        logger.success(
            f"{file_counter-1} CSV files copied into working directory"
        )
    return num_lines, counter


def extract_all_zips_into_working_directory(counter, wd_path):
    zip_files_in_cwd = glob.glob("*.zip")
    if zip_files_in_cwd:
        logger.debug(
            "About to extract all zip files in WD if they contain CSV files"
        )
        num_lines = 0
        for zipfilename in zip_files_in_cwd:
            with zipfile.ZipFile(zipfilename, "r") as zipobj:
                file_name_list = (
                    zipobj.namelist()
                )  # List of files in zip file
                for filename_from_zip in file_name_list:
                    # If any file in the zip (whether it's in another folder, doesn't
                    # matter), ends in csv, pull it
                    if filename_from_zip.endswith(".csv"):
                        newfp = "/".join([wd_path, str(counter) + ".csv"])
                        counter += 1
                        # This will break if there's a file of the same name (numbered csv files in the zip)
                        zipobj.extract(filename_from_zip)
                        os.rename(filename_from_zip, newfp)
                        num_lines += get_num_lines(newfp)
        s = plurality(len(zip_files_in_cwd), "", "s", 1)
        logger.success(
            f"{len(zip_files_in_cwd)} zip file{s} examined & extracted as necessary"
        )
    return num_lines, counter


def read_csv_files_in_cwd():
    plural = plurality(file_counter, "", "s")
    isare = plurality(file_counter, "is", "are")
    line_plurality = plurality(num_lines, "", "s", 1)
    logger.info(
        f"{file_counter-1} csv file{plural} {isare} about to be processed with total {num_lines} line{line_plurality}"
    )
    csv_files_in_work_directory = glob.glob("*.csv")
    files = "\t".join(csv_files_in_work_directory)
    logger.debug(f"Reading: {files}")
    combined_lines = []
    for file in tqdm(csv_files_in_work_directory):
        f = open(file)
        filelines = f.readlines()
        filelines.remove(filelines[0])  # Remove the csv header
        combined_lines.extend(filelines)
        f.close()
    logger.success("Read in all data")
    return combined_lines


def pull_extract_files():
    # Get the path of the file being run without the file at the end of the path (get containing folder)\
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)
    work_dir = "/".join([cwd, "PMARINA_Email_Aggregator"])

    logger.debug(f"Attempting to initialize working directory: {work_dir}")
    create_and_empty_working_directory(work_dir)
    logger.success("Work Directory Initialized")

    file_counter = 1
    num_lines, file_counter = copy_all_csvs_into_working_directory(
        file_counter, work_dir
    )

    (
        number_lines_zip,
        file_counter,
    ) = extract_all_zips_into_working_directory(file_counter, work_dir)
    num_lines += number_lines_zip
    os.chdir(work_dir)
    return num_lines, file_counter


if __name__ == "__main__":
    num_lines, file_counter = pull_extract_files()
    num_lines -= file_counter - 1

    # Create an empty set for emails, as sets don't allow duplicate items
    overall_email_set = set()
    # This is essentially a list of every line that matches the input filetype (all csv files)
    combined_lines_from_input_files = []
    # This is the dictionary of domains against whether or not they're valid (T/F)
    # Mostly to save time (avoid repeated lookups)
    domain_validity = {}
    # A list of lines that failed to be processed and need a human to process them
    failed_list = []
    combined_lines_from_input_files = read_csv_files_in_cwd()
    logger.success("Read in all files")

    logger.debug("Starting to process all ingested data")
    for line in tqdm(combined_lines_from_input_files):
        process_email(
            line, failed_list, domain_validity, overall_email_set
        )
    logger.success("Processed all ingested data")
    if failed_list:
        logger.debug("About to process failed lines")
        for line in tqdm(failed_list):
            print()
            overall_email_set.add(
                input("What email should we add?\n" + line + "\n").lower()
            )
        logger.success("Processed failed lines")

    logger.debug("Starting dump from set to output.txt")
    overall_email_list = list(overall_email_set)
    overall_email_list = sorted(overall_email_list)
    email_output_file = open("output.txt", "w")
    for email_string in tqdm(overall_email_list):
        email_output_file.write(f"{email_string}\n")
    logger.success("Wrote emails out")
    email_output_file.close()
