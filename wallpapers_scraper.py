#!/usr/bin/env python3

import sys
import re
import shutil
import tempfile
import subprocess

import requests

from bs4 import BeautifulSoup

URL_REGEX = re.compile(r"^https://boards\.4chan\.org/wg/thread/\d+$")
FILETEXT_REGEX = re.compile(r"^<div class=\"fileText\" id=\".*\">File: <a href=\"(?P<UID>.*)\" target=\".*\">.*</a> \(.*, (?P<width>\d+)x(?P<height>\d+)\)</div>$")
FILENAME_REGEX = re.compile(r"//i\.4cdn\.org/wg/(?P<id>.*)$")

# adapted from https://stackoverflow.com/a/16696317
def download_file(url, filepath):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
    with open(filepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def main():
    # Checking the correctness of the arguments
    for arg in sys.argv[1:]:
        if URL_REGEX.match(arg) is None:
            # Raise Error
            print("Argument invalid")
            sys.exit(1)

    tmp_dir = tempfile.TemporaryDirectory()
    found_a_file = False

    # Downloading loop
    for index, url in enumerate(sys.argv[1:]):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            for line in soup.find_all(attrs={"class":"fileText"}):
                result = FILETEXT_REGEX.search(str(line))
                if result is not None:
                    width = int(result.group('width'))
                    height = int(result.group('height'))
                    if height > width:
                        continue
                    file_url = 'https:'+result.group('UID')
                    filename = FILENAME_REGEX.search(result.group('UID')).group(1)
                    download_file(file_url, tmp_dir.name+'/'+filename)
                    found_a_file = True
        except requests.exceptions.SSLError:
            print("Couldn't process:")
            for remaining_args in sys.argv[index:]:
                print(remaining_args)
            break
    # end DL loop

    if not found_a_file:
        sys.exit()

    # Selection Loop
    cmd = subprocess.run(['/usr/bin/sxiv', '-o', tmp_dir.name],
                         capture_output=True, text=True, check=True)
    for f in cmd.stdout.strip().split('\n'):
        shutil.copy(f, '/home/hugo/WP')

    tmp_dir.cleanup() # Deletes the dir and erases the files inside of it
    # END OF MAIN()

main()
