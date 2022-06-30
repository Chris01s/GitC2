import requests

def run():
	return requests.get("http://icanhazip.com").text
