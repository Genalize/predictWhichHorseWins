from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import JsonResponse
import os
import pickle
import json

FILE = 'mainDict.txt'

def index(request):
	# with open(os.path.dirname(os.path.realpath(__file__)) + '/'+FILE, 'rb') as handle:
	# 	result = pickle.loads(handle.read())

	# for i,j in list(result.items()):
	# 	if len(result[i]) == 0:
	# 		del result[i]
	return render(request, 'home.html',)