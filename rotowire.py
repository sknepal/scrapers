# -*- coding: utf-8 -*-
"""
Created on Thu May 26 22:10:03 2016

@author: conf
"""
import mechanize
from bs4 import BeautifulSoup
import cookielib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

browser = mechanize.Browser()
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_robots(False)
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
browser.open('http://www.rotowire.com/users/loginnow.htm')
browser.select_form(nr = 0)
browser.form['username'] = 'USERNAME'
browser.form['p1'] = 'PASSWORD'
browser.submit()
url = browser.open('http://www.rotowire.com/daily/mlb/value-report.htm')
returnPage = url.read()

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('thelacunablog-dedbba9514d6.json', scope)
gc = gspread.authorize(credentials)
worksheet = gc.open("Rotowire").sheet1

worksheet.update_cell(1, 1, 'Pos')
worksheet.update_cell(1, 2, 'Player Name')
worksheet.update_cell(1, 3, 'Team')
worksheet.update_cell(1, 4, 'T')
worksheet.update_cell(1, 5, 'Opp')
worksheet.update_cell(1, 6, 'Opp Pitcher')
worksheet.update_cell(1, 7, 'Slot')
worksheet.update_cell(1, 8, 'Salary')
worksheet.update_cell(1, 9, 'FP')
worksheet.update_cell(1, 10, 'Value')
worksheet.update_cell(1, 11, 'FP\G')
worksheet.update_cell(1, 12, 'Value')
worksheet.update_cell(1, 13, 'FP\G')
worksheet.update_cell(1, 14, 'Value')

worksheet.resize(1)
soup = BeautifulSoup(returnPage)
table = soup.find( "table", {"id":"playerPoolTable"} )
for tr in table.find_all('tr')[2:]:
    tds = tr.find_all('td')
    worksheet.append_row([tds[0].text, tds[1].text, tds[2].text, tds[3].text,\
    tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text,\
    tds[10].text, tds[11].text, tds[12].text, tds[13].text])
    
  