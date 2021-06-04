import requests
from bs4 import BeautifulSoup
import re

def get_website_text(url):
	res = requests.get(url)
	html_page = res.content

	soup = BeautifulSoup(html_page, 'html.parser')
	text = soup.find_all(text=True)

	output = ''
	blacklist = [
		'[document]',
		'noscript',
		'header',
		'html',
		'meta',
		'head', 
		'input',
		'script',
		'style',
	]

	for t in text:
		if t.parent.name not in blacklist:
			output += '{} '.format(t)

	return output

file_urls = input("Enter url list filename (or nothing for default 'urls.txt': ")
if file_urls == '':
	file_urls = "urls.txt"
file_words = "words.txt"

try:
	urls = open(file_urls, 'r').readlines()
except:
	print('error: could not open URL list file: ', file_urls)
	exit()

try:
	words = open(file_words, 'r').readlines()
except:
	print('error: could not open word list file: ', file_words)
	exit()

print('Results for URL list', file_urls, ":\n")

for url in urls:
	article = get_website_text(url.rstrip('\n'))
	#print(url.rstrip('\n'))
	found_test = 0
	temp_words = {}
	for word in words:
		regex_string = r'\b' + word.rstrip('\n') + r'\b'
		found = re.findall(regex_string, article, flags=re.IGNORECASE)
		if len(found) > 0:
			#print(word.rstrip('\n'), len(found))
			temp_words[word.rstrip('\n')] = len(found)
			found_test = 1
	if found_test > 0:
		print(url.rstrip('\n') + ',', temp_words)
	else:
		print(url.rstrip('\n') + ',', '+++ CLEAN - NONE FOUND +++')

print("Done, goodbye")