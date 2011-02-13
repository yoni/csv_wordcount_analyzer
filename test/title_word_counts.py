import sys
sys.path.append("/Users/yoni/opower/csv_wordcount_analyzer")

def assert_equals(expected, actual):
  '''Asserts equality of two values. TODO: use a proper unit testing library'''
  if(not expected == actual):
    raise "Expected: " + str(expected) + ", but got " + str(actual)

print "Running tests"
expected = [
    ('day', 3),
    ('red', 2),
    ('the', 2),
    ('big', 1),
    ('bueller', 1),
    ('earth', 1),
    ('ferris', 1),
    ('fiction', 1),
    ('grit', 1),
    ('hood', 1),
    ('hunt', 1),
    ('little', 1),
    ('october', 1),
    ('off', 1),
    ('pulp', 1),
    ('riding', 1),
    ('still', 1),
    ('stood', 1),
    ('thei', 1),
    ('true', 1)
]

# Test word counts for movie titles. NOTE: Any changes to the titles.csv file will break this test
from csv_wordcount_analyzer import Analyzer
a = Analyzer('data/titles.csv')
freq = a.word_freq('title')
assert_equals(expected, freq.items())

print "Finished running tests"
