from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas
import os

def download_vid_by_titles(los):
	ids = []
	# query video that corresponds with data in csv file
	for index, item in enumerate(los):
		vid_id = query_vid_id(item)
		ids += [vid_id]
	print("Downloading songs")
	download_vid_by_ids(ids)


def download_vid_by_ids(lov):
	SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
	# to pass by
	try:
		os.makedirs(SAVE_PATH)
	except:
		print("folder exists")
	ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
		'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download(lov)

def query_vid_id(query):
	print ("Getting video id for: ", query)
	BASIC="http://www.youtube.com/results?search_query="
	URL = (BASIC + query)
	URL.replace(" ", "+")
	page = requests.get(URL)
	session = HTMLSession()
	response = session.get(URL)
	response.html.render(sleep=1)
	soup = BeautifulSoup(response.html.html, "html.parser")

	results = soup.find('a', id="video-title")
	return results['href'].split('/watch?v=')[1]

def __main__():

	data = pandas.read_csv('songs.csv')
	data = data['colummn'].tolist()
	print("Found ", len(data), " songs")
	download_vid_by_titles(data[0:1])
__main__()
