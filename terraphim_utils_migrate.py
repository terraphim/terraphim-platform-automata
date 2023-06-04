def load_csv_to_automata(url, lazy=True):
    from urllib.request import urlopen
    from urllib.parse import urlparse, unquote
    import csv
    import gzip
    import os
    import tempfile
    import ahocorasick
    A = ahocorasick.Automaton()
    data = {}
    patterns = list()
    # Extract the filename from the URL
    url_parsed = urlparse(url)
    from pathlib import Path
    # Check if the file already exists in the temp folder
    temp_dir = tempfile.gettempdir()
    parsed_filename = unquote(Path(url_parsed.path).name)
    filename = Path(temp_dir) / parsed_filename
    file_path = os.path.join(temp_dir, filename)
    if os.path.exists(file_path):
        # Open the existing file and read the rows
        pass
    else:
        # Download the gzipped CSV file from the URL
        response = urlopen(url)

        # Save the file to the temp folder with the specified filename
        with open(file_path, 'wb') as f:
            f.write(response.read())
    if lazy:        
        parsed_filename="lazy_"+parsed_filename

    # Open the gzipped CSV file and read the rows
    with gzip.open(file_path, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            id = row[1].replace("\"", "")
            parent_id = row[2]
            if lazy:
                terms = row[0].lower().split(" ")
                for term in terms:
                    A.add_word(term, (id, term))
                    print(f"add to automata {term} - {id}")
            else:
                A.add_word(row[0].lower(), (id, row[0]))
                print(f"add to automata {row[0]} - {id}")
    A.make_automaton()
    print(A.get_stats())
    save_file=f"./automata/automata_{parsed_filename}.lzma"
    print(f"save automata to {save_file}")
    import joblib
    joblib.dump(A,save_file)

    return A

def find_matches(sent_text, A):
    matched_ents = []
    for char_end, (eid, ent_text) in A.iter_long(sent_text):
        char_start = char_end - len(ent_text)
        matched_ents.append((eid, ent_text, char_start, char_end))
    # remove shorter subsumed matches
    longest_matched_ents = []
    for matched_ent in sorted(matched_ents, key=lambda x: len(x[1]), reverse=True):
        longest_match_exists = False
        char_start, char_end = matched_ent[2], matched_ent[3]
        for _, _, ref_start, ref_end in longest_matched_ents:
            if ref_start <= char_start and ref_end >= char_end:
                longest_match_exists = True
                break
        if not longest_match_exists:
            # print("adding match to longest")
            longest_matched_ents.append(matched_ent)
    return [t for t in longest_matched_ents if len(t[1])>3] 

if __name__ == "__main__":
    haystack = "I am a text with the word Organization strategic plan and bar and project calendar"
    print(haystack)
    url = "https://terraphim-automata.s3.eu-west-2.amazonaws.com/project_manager.csv.gz"
    Automata = load_csv_to_automata(url)
    matches = find_matches(haystack.lower(),Automata)
    print(matches)
    Automata = load_csv_to_automata(url,lazy=False)
    matches = find_matches(haystack.lower(),Automata)
    print(matches)