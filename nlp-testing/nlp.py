#!/usr/bin/env python3
import sys
import os
import speech_recognition as sr
import spacy
from credentials import *

nlp = spacy.load('en')

r = sr.Recognizer()
with sr.Microphone() as source:
	print("Say something!")
	audio = r.listen(source)
  
# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "guardbot-200023",
  "private_key_id": "ca92ff685e8f39366871f64ed523aa3a12d1a989",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDlSnGQzm+fgzpt\nJkWslK/DZU7VgAoJI+k/3sZUeWRKNA2IwWjNDHGk6jvZjARkqwieSmUzMtOMvnPl\ntidrCPnTtQi755KB7KDoSO9i09jAS8I4RcvwUk5VN11yRn2jBojcroqkKPNvTsHR\nuU6g/+pfW39ACUYmYGsfqU4R1gDSFA1N6PfbhUqGkrkrFBHCV1cUp6uP1ieI0bJr\nRAGY1sAgJj+M9KQl3eBRFEUKAsYwbvHbtUe8/8Xp+wv8lmbpqsCbRYtAvndI7UzY\nL3HLlFCOTLDO+vssEfdAbcm9ed7bYSvyjXDDhWfAlv5NSk/9lVUJCAfWPdeSmXYw\nD/I7Mx4TAgMBAAECggEAQOFyRi/r7P6Um0sfnwiJvageiRJMhK6ZM14Fz+RzqP2W\nsNJNpev2AlzXZ6UTnyq4axYREc45h1Ni9ya2e7aT/sB0wrrxvXroQyJUPqpEZJFr\nWUICxbN8f+eFNS9WILnaI1vuVipSS/ZEqOQfKDaSKr54wPV+2KAi39goA6sDG25Q\n0MxL6pSYBSrXdbzBETeSgF5fCJbuYS7aAFwf9znIfsAmHStfvdsiseKtX73YTfyP\n4fEmfQzTCe4zHiUx13JkowEBelqs3wSXmvEog6TgBlufhhAhohEkNCuQ1YSQPL7O\nwvxUsUErOQLmva2Y3NAZmIWYynpMT3qnWunWWiWC9QKBgQD/haDu62TRm0mCK0qt\n9GyDPWX2u8n/QKuR4QDt7n5hu6AfMzUxU0nLZE0Qln/oodxKgSaELST3mxqjA9Uf\ncTr+/kL1DVgAR8YS/EHmtlx/vyRE6I4ECO0zyXvOU4EZ5EYEYA1QLalRpNFY7WkM\nMFlQN3GVwwXHjLqBs+cmaEq2XwKBgQDluECuVT7h7yj8daQJh4TGFBTl2yL71hP8\nOyHS6PIdYRkwYVjzSs3/lSly6VEgcVRgPTcpIjbI8QXDxFPdJS11Wd6LByIypfCL\nTlLAp4x02LAdodXPEQyBS3M1CkzXzefQp3050a8asi+EYyPbmwcLeInKElkbXdPf\nR7hFXfFszQKBgHWJQEfmW4/XQG7x/v4Ziriry3U9WGNjmggWWdkYdWX7amIvqe4w\ng6ddUd2pfNjDa5OR6Oev5GtJG22U27oE2cBlsOML6kjmuwQMqTu48r+IauSPnJPa\nj1HdAmgcHSyNxm9Ix5b0CgiWKf4f5sxGiS7O8h6TgNsTrs7utAsEuik9AoGATT2K\n4hNftXBJA7o6kcmzZzbRYAgy1yLATYtEcDpLTn2bjpzs38FDSrDI4w54bMQubr2m\nknoimaYRHiYhXLZndpHlNjIL2aPaIb0QLh8oJxHFBfGohptg7QiFkEwKUnW1gH8Q\nqCRNEFjhiU4cfHbAA6dgDUXmGEGQP/9Jgml4B/ECgYAPEXVgvNZb7ZsXphIgzMWJ\ntj4FcuWxgXwW9uBsJ3Ma50ijuYZiTiGOH2N2n848OYF0K+8YuCrdDbrq5rVasA46\n5IKdDkNMol/SEsQvmMNeb+xhFJER71YEt6Jr9NOmJKq+Esh/ssXmwMYi7ceru77Z\nJMdYOSppNzzZXKqxECrDnw==\n-----END PRIVATE KEY-----\n",
  "client_email": "guardbot@guardbot-200023.iam.gserviceaccount.com",
  "client_id": "112203121764581840115",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/guardbot%40guardbot-200023.iam.gserviceaccount.com"
}
"""
#sys.stdout.write(r.recognize_google_cloud(audio, language="he-IL", credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)[::-1])
text_file = open('audio.txt', 'w+')
text_file.write(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
text_file.close()

with open('audio.txt', 'r') as content_file:
	content = content_file.read()
	doc = nlp(u"{}".format(content))

 	if "dog" in doc.text:
 		print "Success"
 	else:
 		print "No secret phrase"