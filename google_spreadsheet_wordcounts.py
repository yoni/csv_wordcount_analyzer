__author__ = 'yoni.bmesh@gmail.com (Yoni Ben-Meshulam)'

from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string

class SimpleCRUD:

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheet Linguistic Analysis'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.list_feed = None
    
  def _PrintFeed(self, feed):
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        print '%s %s %s' % (i, entry.title.text, entry.content.text)
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print 'Contents:'
        for key in entry.custom:  
          print '  %s: %s' % (key, entry.custom[key].text) 
        print '\n',
      else:
        print '%s %s\n' % (i, entry.title.text)
        
  def get_rows(self):
    feed = self.get_worksheet_feed()
    rows = []
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        row = {}
        for key in entry.custom:  
          row[key] = entry.custom[key].text

        rows.append(row)
    return rows

  def _InvalidCommandError(self, input):
    print 'Invalid input: %s\n' % (input)
    
  def get_worksheet_feed(self):
    """The current worksheet's content"""
    return self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)

  def spreadsheets(self):
    """Get the list of spreadsheets"""
    # Get the list of spreadsheets
    feed = self.gd_client.GetSpreadsheetsFeed()
    self._PrintFeed(feed)
    return feed

  def set_spreadsheet(self, input):
    """Select the spreadsheet to use"""
    feed = self.gd_client.GetSpreadsheetsFeed()
    id_parts = feed.entry[int(input)].id.text.split('/')
    self.curr_key = id_parts[len(id_parts) - 1]
  
  def worksheets(self):
    """Get the list of worksheets"""
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    self._PrintFeed(feed)
    
  def set_worksheet(self, input):
    """Select the worksheet to use"""
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    id_parts = feed.entry[int(input)].id.text.split('/')
    self.curr_wksht_id = id_parts[len(id_parts) - 1]

