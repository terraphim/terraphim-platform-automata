from terraphim_utils import loadAutomata, find_matches
from sample_data.sample_data import *

def test_matcher(url):
    Automata=loadAutomata(url)
    print(f"Testing matcher from {url}")
    print("Sentence ",sentence2)
    print("Matched to ", find_matches(sentence2.lower(), Automata))
    print("Token (cyber)", test_token2)
    print("Matched ", find_matches(test_token2.lower(),Automata))
    print("Sentence (cyber)", sentence_cyber)
    print("Matched ",find_matches(sentence_cyber.lower(),Automata))
    print("Sentence project  ",find_matches(sentence_project.lower(),Automata))


test_matcher("https://s3.eu-west-2.amazonaws.com/assets.thepattern.digital/automata_fresh_semantic.pkl.lzma")
test_matcher("https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_cyberattack.lzma")
test_matcher("https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_cyberattack_tolower.lzma")
test_matcher("https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_project_manager.csv.gz.lzma")
