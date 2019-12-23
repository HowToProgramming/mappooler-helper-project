import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyosu import main
from thisisatoken import token
import base64
import json
osu = main(token)
loginfile = open("agpwejgepigh888887777.otnpj", "rb").read()
logindata = base64.decodebytes(loginfile)
logindatareal = json.loads(logindata.decode("ascii"))
scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(logindatareal, scope)
atr = gspread.authorize(credentials)