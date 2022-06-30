import os

def getProfiles():
	show_profiles = os.popen("netsh wlan show profiles").readlines()
	profiles = []
	for line in profiles:
		if "Profile" in line:
			profile = line.split("Profile")[-1].replace(":", "").strip()
			profiles.append(profile)
	return profiles


def getWiFiPasswrd(profile):
	profile_content = os.popen(f"netsh wlan show profile {profile} key=clear").read()
	key_content = re.findall("(?:Key Content.*:)(.*)", profile_content)
	if key_content:
		return key_content[0].strip()
	return None


def run():
	results = []
	if os.name == 'nt':
		wlan_profiles = getProfiles()
		for profile in wlan_profiles:
			pwd = getWiFiPasswrd(profile)
			if pwd:
				results += [f"Profile: {profile}\tPassword: {pwd}"]
		return '\n'.join(results)
	else:
		return None
