import sys
from datetime import datetime
from pathlib import Path


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def quote_string(v):
    """
    RedisGraph strings must be quoted,
    quote_string wraps given v with quotes incase
    v is a string.
    """

    if isinstance(v, bytes):
        v = v.decode()
    elif not isinstance(v, str):
        return v
    if len(v) == 0:
        return '""'

    if v[0] != '"':
        v = '"' + v

    if v[-1] != '"':
        v = v + '"'

    return v

def loadAutomata(url):
    from urllib.request import urlopen
    from urllib.parse import urlparse, unquote

    import ahocorasick 
    import joblib
    from pathlib import Path
    url_parsed = urlparse(url)
    file_path = Path("/tmp/") / unquote(Path(url_parsed.path).name)
    try:
        Automata=joblib.load(file_path)
    except:
        automata_file=urlopen(url)
        
        with open(file_path, 'wb') as f:
            f.write(automata_file.read())
        Automata=joblib.load(file_path)    
    return Automata

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



# https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_cyberattack.lzma cyber
# "https://s3.eu-west-2.amazonaws.com/assets.thepattern.digital/automata_fresh_semantic.pkl.lzma" medical