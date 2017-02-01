#Import Session and BeautifulSoup for html fetching and formatting
from requests import Session
from bs4 import BeautifulSoup
#Import regex for substitution
import re
#Import os to keep paths os independent
import os
#Import nested for simple file opening using `with`
from contextlib import nested

"""Loops the code to fetch from multiple games of jeopardy based on the game_id
assigned by j-archive.com"""
for i in range(1,31):
  """Fetch raw html from j-archive, store to a file as text"""
  #Create a Session object s to fetch raw html from j-archive
  s = Session()
  #Store the response from j-archive with a game_id of `i`
  response = s.get('http://www.j-archive.com/showgame.php?game_id='+str(i))
  #Open the `html.txt` file, write raw html data from response, close `html.txt`
  with open('html.txt','w') as f:
    f.write(response.text)
    f.close()

  """Fix html stored in `html.txt` with regex subs, write to `clean_html.txt`"""
  #Open `html.txt` and `html_clean.txt` for reading and writing, respectively
  with nested(open('html.txt', 'r'), open('html_clean.txt'))\
  as (f1, f2):
    #TODO: Look into re.findall?
    #Loop through and correct f1 line by line
    for line in f1:
      temp = re.sub('&lt;', '<', line)
      temp = re.sub('&gt;', '>', temp)
      temp = re.sub('&quot;', '"', temp)
      temp = re.sub('&amp;', '\&', temp)
      temp = re.sub('&\#160;', '\ ', temp)
      temp = re.sub('<td class="(wrong|right)">.*</td>', '', temp)
      #TODO: Fix awful, long regex
      temp = re.sub('\'\)" onclick="togglestick\(\'clue_J_[0-9]_.{11}',\
      '', temp)
      #TODO: Fix awful, long regex
      temp = re.sub('\'\)" onmouseout="toggle\(\'clue_J_[0-9]_[0-9]\', .{18}',\
      '', temp)
      #Writes corrected line to f2
      f2.write(temp)
  
  """Prints the fixed html file as text using BeautifulSoup"""
  #Create a BeautifulSoup object `soup` with html_clean.txt and the lxml parser
  soup = BeautifulSoup(open('html_clean.txt'), 'lxml')
  #Create/open a file numbered by the game_id from j-archive
  with open(os.path.join*('Plaintexts', 'html_plaintext'+str(i)+'.txt'), 'w')\
  as f:
    #Convert the html_clean.txt file to text using `soup`
    f.write(soup.get_text())