def loadAutomata(url, lazy=False):
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
                    # print(f"add to automata {term} - {id}")
            else:
                A.add_word(row[0].lower(), (id, row[0]))
                # print(f"add to automata {row[0]} - {id}")
    A.make_automaton()
    # print(A.get_stats())
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
    Automata = load_automata(url, lazy=True)
    matches = find_matches(haystack.lower(),Automata)
    print("Matched Lazy Project manager ",matches)
    Automata = load_automata(url,lazy=False)
    matches = find_matches(haystack.lower(),Automata)
    print("Matched Project manager ",matches)
    print ("=====================")
    print ("Test System Operator role")
    haystack="""
    The role of systems engineering (SE) during the operation of a system consists of ensuring that the system maintains key mission and business functions and is operationally effective. The systems engineer is one of the stakeholders who ensures that maintenance actions and other major changes are performed according to the long-term vision of the system. Both the maintenance actions and any implemented changes must meet the evolving needs of owning and operating stakeholders consistent with the documented and approved architecture. SE considerations will also include the eventual decommissioning or disposal of the system so that the disposal occurs according to disposal/retirement plans. Those plans must account for and be compliant with relevant laws and regulations (for additional information on disposal or retirement, please see the Product and Service Life Management knowledge area (KA)). When the system-of-interest (SoI) replaces an existing or legacy system, it may be necessary to manage the migration between systems such that stakeholders do not experience a breakdown in services (INCOSE 2012).
    """
    url = "https://system-operator.s3.eu-west-2.amazonaws.com/term_to_id.csv.gz"
    Automata = load_automata(url,lazy=False)
    matches = find_matches(haystack.lower(),Automata)
    print("Matched System Operator ",matches)