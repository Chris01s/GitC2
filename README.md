# GitC2

Github Command and Control idea adapted from BlackHat Python 2nd Ed. This version has used cryptography for PAT token, encrypting it with RSA.
Token is encrypted in the trojan build but RSA key is hosted locally. Request is sent to obtain the RSA key to decrypt the token for access to github API.

Extra modules have been added to harvest passwords, screenshots, and gather systeminfo.

This is built purely for educational puproses, I am not responsible for it's use or misuse; please use this responsibly and ethically. To that end, few places in the code need to be modified for operational purposes: if you do not know what/how to change in the code, then you probably shouldn't be using
this! 
