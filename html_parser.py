#Import Session and BeautifulSoup for html fetching and formatting
from requests import Session
from bs4 import BeautifulSoup
#Import regex for substitution
import re

"""Loops the code to fetch from multiple games of jeopardy based on the game_id
assigned by j-archive.com"""
for i in range(1,31):
  """Fetch raw html from j-archive, store to a file as text"""
  #Create a Session object s to fetch raw html from j-archive
  s = Session()
  #Store the response from j-archive with a game_id of `i`
  response = s.get('http://www.j-archive.com/showgame.php?game_id='+str(i))
  #Open the `html.txt` file, write raw html data from response, close `html.txt`
  file = open('html.txt','w')
  file.write(response.text)
  file.close()

  """Fix html stored in `html.txt` with regex subs, write to `clean_html.txt`"""
  
  file = open('html.txt', 'r')
  file2 = open('html_clean.txt', 'w')
  for line in file:
    temp = re.sub('&lt;', '<', line)
    temp = re.sub('&gt;', '>', temp)
    temp = re.sub('&quot;', '"', temp)
    temp = re.sub('&amp;', '\&', temp)
    temp = re.sub('&\#160;', '\ ', temp)
    temp = re.sub('<td class="(wrong|right)">.*</td>', '', temp)
    temp = re.sub('\'\)" onclick="togglestick\(\'clue_J_[0-9]_[0-9]_stuck\'\)">',\
    '', temp)
    temp = re.sub(\
    '\'\)" onmouseout="toggle\(\'clue_J_[0-9]_[0-9]\', \'clue_J_[0-9]_.{8}',\
    '', temp)
    file2.write(temp)
  file.close()
  file2.close()
  soup = BeautifulSoup(open('html_clean.txt'), 'lxml')

  file3 = open('Plaintexts\\html_plaintext'+str(i)+'.txt', 'w')
  file3.write(soup.get_text())
  file3.close()
