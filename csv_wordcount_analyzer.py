import sys
import nltk
from nltk import FreqDist
import os
import re
import csv
import string

class Analyzer:
  """
  Analyzes word counts across a given CSV file's columns. A word will count only once
  per cell of a column. Counds reflect the prevalence of that word across all cells
  in that column.

  The results are NLTK's standard FreqDist object.

  For example, to get the word frequencies for the "Innovation Ideas" column in the
  file data/ideas.csv:

    import csv_wordcount_analyzer
    from csv_wordcount_analyzer import Analyzer
    a = Analyzer('data/ideas.csv')
    freq = a.word_freq('Innovation Ideas')
    freq.items()

  Known issues: Calling word_freq is somehow destructive, so it can only be called once.
  The workaround is to create a new Analyzer each time you want to call word_freq or top_words
  """
  
  def __init__(self, csv_file_name):
    """Create a new analyzer with all of the rows in the CSV file"""
    if not csv_file_name:
      raise "Expected a file_name determining which CSV file to open."
    self.rows = csv.DictReader(open(csv_file_name))

  def full_text(self, column):
    """Retrieves the full text for the given column."""
    column_text = ''
    for row in self.rows:
      column_text = column_text + " " + row[column].lower()
    return column_text 

  def get_values(self, row, fields):
    """Gets an array of all of the values for the given fields from the given row"""
    values = []
    for field in fields:
      if(row[field]):
        values.append(row[field])
    return values

  def word_freq(self, column):
    """Retrieves the word frequencies for the given column"""
    words = []

    for row in self.rows:
      pattern = r"\w+"
      tokens = nltk.tokenize.regexp_tokenize(row[column], pattern)
      stopwords = nltk.corpus.stopwords.words('english')
      row_words = [w for w in tokens if w not in stopwords]
      row_words = set(row_words) # Remove duplicates within a given row
      for word in row_words:
        words.append(word)

    freq = FreqDist(word.lower() for word in words)
    return freq 

  def top_words(self, column, n):
    """
    Retrieves the N top words from the given column, along with the count of
    each word in CSV format.
    """
    freq = self.word_freq(column)
    result = 'word,count\n'
    words = freq.items()
    for i in range(n):
      if i >= len(words):
        break
      f = words[i]
      result = result + f[0] + "," + str(f[1]) + '\n'

    return result

  def fields(self):
    """Retrieves all of the fields in the CSV"""
    return self.rows.next().keys()

