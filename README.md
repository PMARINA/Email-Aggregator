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
- `pip install tqdm loguru`
  - Do I really need these?
    - Unless you change my code, yes. Do they do anything important? Not really. I just wanted to learn to use them.
- Put [main.py](main.py) in a folder (or if you cloned this repository, skip this step)
- Copy all CSVs, ZIP files containing CSVs into the same folder as [main.py](main.py)
- Run [main.py](main.py)
  - If the script cannot extract a line, it will wait until it extracts everything and then ask you for the correct email from each line.
  - If you ctrl+c at this point, you won't have any emails extracted... You can just comment out the lines between `logger.debug("about to process failed lines")` and the `logger.success...` right after it.
- [PMARINA_Email_Aggregator/output.txt](PMARINA_Email_Aggregator/output.txt) will have your emails, separated by newlines.

