import os
import sys


def run():
	if sys.platform.lower()=="linux":
		return os.popen("hostnamectl").read()
	elif os.name=="nt":
		return os.popen("systeminfo").read()
	else:
		return None
