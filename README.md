# PMARINA Email Aggregator

## What does it do

- Given CSV and/or ZIP files, it extracts all CSVs and all unique, valid email addresses from them.

## Should I use this in a production environment

- Probably not: I wrote this to work on a small scale (<1000 emails) from a few google forms. Here are some of the main issues with doing so:
  - Efficiency: I didn't try to make this a parallelized operation, so that's a big drop in speed.
  - Memory: I load all of the files into memory before trying to process them, rather than one at a time. Why? Because otherwise I either need to find the total number of lines in all the files combined, or tqdm doesn't look as nice (the purpose of this was to figure out tqdm/logger).
  - Robustness? - I wrote this to parse out a few forms for a university club. The regex provided by email.utils probably wasn't designed to be used the way I'm using it, and there's a good chance my way of doing this will break if your form accepts info/generates CSVs in a different way. You should definitely look through the output to make sure it works as expected before acting on it.

## Who should use this

- People doing email aggregation on small scales, but who can carefully look through the output to make sure nothing strange appears.

## How do I use it

- Get Python 3+
- `pip install --upgrade tqdm loguru dnspython google-api-python-client google-auth-oauthlib`
  - Do I really need these?
    - Yes, for email-sending & drive file access, Google APIs are important. TQDM & Loguru are necessary for clean outputs. dnspython helps with email validation.
- Put all important events in a new file `input.txt` inside the top level of this repository. 
  - The format is as follows: (note that `#` is used as the comment character, but only if it is the first (non-whitespace) character in the line)
    1. Title Line
    2. Description Line
    3. Event Sign-up link (heavily recommend dynamic URLs)
    4. Date & Time: (yyyy.mm.dd hhmm) eg "2021.12.31 2359"
- Run the applicable file (`python main_weekly.py` or `python main_reminder.py`)
