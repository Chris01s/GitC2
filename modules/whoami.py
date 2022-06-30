import os

def run():
	return os.popen("whoami").read()
