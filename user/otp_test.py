'''
Created on 5 Jul, 2020

@author: DELL
'''

import requests

#url = "https://api.textlocal.in/send/?apiKey=zoL+hAocjgM-w2DUuEnkgYobPgG1jLvUZSlhjpT0cI&sender=TXTLCL&numbers=917205237804&message=Your otp is 1234"
url = ""
resp = requests.get(url)
print(resp.json())
