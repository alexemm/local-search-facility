from util import read_and_parse_text
from local_search import local_search


def test():
    facilities = read_and_parse_text("test_cases/test0.txt")
    #local_search(facilities, frozenset())
    #local_search(facilities, frozenset({'A','B','C','D','E'}))
    local_search(facilities, frozenset({'B','D'}))


test()
