import csv
import gzip
import os
import tempfile
import requests
import ahocorasick_rs


def load_automata(url):
    from urllib.request import urlopen
    from urllib.parse import urlparse, unquote
    data = {}
    patterns = list()
    # Extract the filename from the URL
    url_parsed = urlparse(url)
    from pathlib import Path
    # Check if the file already exists in the temp folder
    temp_dir = tempfile.gettempdir()
    filename = Path(temp_dir) / unquote(Path(url_parsed.path).name)
    file_path = os.path.join(temp_dir, filename)
    if os.path.exists(file_path):
        # Open the existing file and read the rows
        pass
    else:
        # Download the gzipped CSV file from the URL
        response = requests.get(url)
        content = response.content

        # Save the file to the temp folder with the specified filename
        with open(file_path, 'wb') as f:
            f.write(content)

    # Open the gzipped CSV file and read the rows
    with gzip.open(file_path, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            term = row[0]
            patterns.append(term)
            id = row[1]
            parent_id = row[2]
            data[term] = {'id': id, 'parent_id': parent_id}
    return data , patterns

def find_matches(haystack: str, data:dict, patterns:list) -> list:
    #  Find matches in the haystack string always return a list of tuples (id, term, start, end)
    matched_terms = list()
    ac = ahocorasick_rs.AhoCorasick(patterns, matchkind=ahocorasick_rs.MatchKind.LeftmostLongest)
    matches=ac.find_matches_as_indexes(haystack)
    print(f"{matches}")
    for match in matches:
        id = data[patterns[match[0]]]['id']
        term = patterns[match[0]]
        matched_terms.append((id,term,match[1],match[2]))
    return matched_terms

if __name__ == "__main__":
    haystack = "I am a text with the word Organization strategic plan and bar and project calendar"
    print(haystack)
    url = "https://terraphim-automata.s3.eu-west-2.amazonaws.com/project_manager.csv.gz"
    data, patterns = load_automata(url)
    matches = find_matches(haystack, data, patterns)
    print(matches)