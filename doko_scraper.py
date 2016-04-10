import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime


pages = ['http://doko.dwit.edu.np/?page_id=375', 'http://doko.dwit.edu.np/?page_id=378','http://doko.dwit.edu.np/?page_id=1066',
        'http://doko.dwit.edu.np/?page_id=5675','http://doko.dwit.edu.np/?page_id=9728']

startTime = datetime.now()
with open("students.csv", "ab") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["Name", "High_School", "Goal", "Interests", "Idol"])
    for j in pages:
        res = requests.get(j)
        try:
            res.raise_for_status()
            soup = BeautifulSoup(res.text)
            table = soup.find_all("table", class_="student_info")
            
            for i in range(0, len(table)):
                rows = list()
                for row in table[i].findAll("tr"):
                    rows.append(row)
                    
                name = rows[1].text
                high_school = rows[3].text
                goal = rows[5].text
                interests = rows[7].text
                idol = rows[9].text
                
                csv_row = [name, high_school, goal, interests, idol]
                writer.writerow([unicode(text).encode("utf-8").strip() for text in csv_row])
                
        except Exception as exc:
            print('There was a problem: %s' % (exc))

print "Done"     
print "\nTime taken: " + str(datetime.now() - startTime)