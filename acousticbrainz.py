import requests

def retrieve_highlevel_features(mbid):
	try:
		response = requests.get('https://acousticbrainz.org/api/v1/' + mbid + '/high-level?n=0')
		data = response.json()
		if len(data) <= 1:
			return {}
		return data
	except:
		return {}

def retrieve_lowlevel_features(mbid):
	try:
		response = requests.get('https://acousticbrainz.org/api/v1/' + mbid + '/low-level?n=0')
		data = response.json()
		if len(data) <= 1:
			return {}
		return data
	except:
		return {}