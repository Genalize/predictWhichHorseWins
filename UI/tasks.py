from scraper import main
from twitterSentiment import mainAnalysis
import pickle
import datetime
#from celery import task


FILE = 'mainDict.txt'


# Use celery to make it a schedulable task

def loadData():
	eventsAndHorses = main()

	newDict = {}

	for i in eventsAndHorses:

		horseSents = {}
		for j in eventsAndHorses[i]:
			sents = mainAnalysis(j)
			horseSents[j] = sents

		print(horseSents)
		newDict[i] = horseSents

	print(newDict)

	with open(FILE, 'wb') as handle:
		pickle.dump(newDict, handle)

