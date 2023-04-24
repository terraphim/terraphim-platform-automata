from terraphim_utils import loadAutomata, find_matches
from sample_data.sample_data import *

def test_matcher(url):
    Automata=loadAutomata(url)
    print(f"Testing matcher from {url}")
    print(find_matches(sentence2, Automata))
    print(find_matches(test_token2,Automata))


test_matcher("https://s3.eu-west-2.amazonaws.com/assets.thepattern.digital/automata_fresh_semantic.pkl.lzma")
test_matcher("https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_cyberattack.lzma")