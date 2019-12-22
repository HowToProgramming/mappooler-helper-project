import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyosu import main
from thisisatoken import token
osu = main(token)

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name('omdtmappool-d88728cc74b2.json', scope)
atr = gspread.authorize(credentials)