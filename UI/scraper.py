import time
from bs4 import BeautifulSoup
import requests


class Scraper():
	"""Scraper class to scrape the horse racing
	site, extracts events and the competitors in 
	the events
	"""
	def __init__(self, url):
		self.url = 'http://www.attheraces.com/racecards/tomorrow'
		self.root = 'http://www.attheraces.com'



	def getAllEvents(self,):
		self.data = requests.get(self.url, timeout=8)
		self.soup = BeautifulSoup(self.data.content, 'html.parser')
		
		meetings = self.soup.find_all('a', {'class':'meeting'}, href=True)

		allEvents = {}
		
		for i in meetings:
			span = i.find_all('span',{'itemprop':'name'})
			if not len(span) == 0:
				event = span[0].text
				allEvents[i['href']] = event
			

		return allEvents


	def getAllHorses(self,url):
		horseData = requests.get(url)
		horseSoup = BeautifulSoup(horseData.content, 'html.parser')
	
		allHorseDivs = horseSoup.find_all('div',{'class':'horse'}) or horseSoup.find_all('td',{'class':'horse'})

		allHorses = []
		for i in allHorseDivs:
			if i.find('a') is not None:
				allHorses.append(i.find('a').text)
		allHorses = list(set(allHorses))

		return allHorses


	def getHorseDetails(self, horse):
		pass

		

def main():
	#creater a scraper object
	url = 'http://www.attheraces.com/racecards/tomorrow'

	scraper = Scraper(url)

	allEvents = scraper.getAllEvents()

	finalDict = {}

	for i in allEvents:
		finalDict[i] = scraper.getAllHorses(scraper.root + i)
		print(i, finalDict[i])

	print(finalDict)

	return finalDict













