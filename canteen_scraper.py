from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import csv
from datetime import datetime

startTime = datetime.now()
driver = webdriver.Firefox()
driver.get("http://system.deerwalkfoods.com:8053/")
time.sleep(10)
username = driver.find_element_by_id("txtUsername")
password = driver.find_element_by_id("txtPassword")

username.send_keys("email")
password.send_keys("password")

form = driver.find_element_by_name("btnLogin")
form.click()
driver.get("http://system.deerwalkfoods.com:8053/Feedback.aspx")
time.sleep(10) 
done = 0
with open("canteen.csv", "ab") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["Date", "Email", "Feedback"])
        while done == 0: 
            for j in range(2, 7):
                time.sleep(10)
                date = ""
                email = ""
                feedback = ""
                html = driver.page_source
                soup = BeautifulSoup(html)
                table = soup.find( "table", class_="dtTable fixedTbl" )
                rows = list()
                count = 0
                for row in table.findAll("tr"):
                    rows.append(row)
                    count += 1

                for i in range(1, count-2):
                    date = rows[i].find("td", {"valign" : "middle"}).get_text()
                    email = rows[i].find("span", {"id" : re.compile('ContentPlaceHolder1_gvFeedback_lblEmail.*')}).get_text()
                    if rows[i].find('span', class_='allcontent') == None:
                        feedback = rows[i].find('span', class_='FeedbackMessage').get_text()
                    else:
                        feedback = rows[i].find('span', class_='allcontent').get_text()
                    csv_row = [date, email, feedback]
                    writer.writerow([unicode(text).encode("utf-8") for text in csv_row])
                    
                div = driver.find_element_by_class_name('pager')
                links = div.find_elements_by_tag_name('td')

                if (links[1].text == '...'):
                    try:
                        links[j+1].click()
                    except IndexError:
                        done = 1
                else:
                    links[j].click()
print "Done"     
print "\nTime taken: " + str(datetime.now() - startTime)