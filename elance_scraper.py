import re
import csv
import requests
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
#in case of error related to urllib3.poolmanager, replace the above line with: from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)
        
s = requests.Session()
s.mount('https://', MyAdapter())
count = 0
with open("elance_dataset.csv", "ab") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["Name", "Tagline", "Rate", "Rating", "Level", "Number_of_jobs", "Category", "Skills"])
        for page in range(1, 161):
            url = 'https://www.elance.com/r/contractors/cry-NP/fbk-0/p-' + str(page)
            res = s.get(url)
            try:
                res.raise_for_status()

                #bs object
                soup = BeautifulSoup(res.text)

                #name
                namelist = soup.find_all("a", class_='title-link')

                #tagline
                infobar = soup.find_all("div", class_='info')

                #rate
                stats = soup.find_all("div", class_='stats')

                #skills
                skillsbar = soup.find_all("div", class_='prof')

                for i in range(0,25):
                        #clear all values
                        rate = ""
                        numbers = ""
                        category = ""
                        skills = ""
                        tagline = ""
                        name = ""
                        level = ""
                        number_of_jobs = ""

			#get name
                        name = namelist[i].get_text().strip()

			#tagline may be empty, if not, then just assign it to the tagline variable
                        if infobar[i].find("div", class_="tagline") is not None:
                            tagline = infobar[i].find("div", class_="tagline").get_text().strip()

                        info = ",".join([text.get_text().strip() for text in stats[i].find_all("div", class_="left")])

			#regex to find '$' from the text (for rate)
                        rate = re.findall('\${1}[,0-9]{1,10}', info)

                        #check whether rate is private (the start variable is necessary while grabbing category, since the position to start searching for category
			#changes depending on whether the rate is private / public.)
                        if "Rate" in info:
                            rate = rate[0]
                            start = 4
                        else:
                            start = 0
                            rate = ""

                        # split numbers
                        numbers = [token for token in info.split() if token.isdigit()]

                        #the first element is level
                        level = numbers[0]

                        #and the second element is the number of jobs
                        number_of_jobs = numbers[1]

                        #split everything else (i.e. texts)
                        field = [token for token in info.split() if not token.isdigit()]

                        #if rate is public, then category is the text between the 4th pipe and the immediate next pipe
                        #else, we need to grab the text between the first two pipes starting from the first letter.

                        for x in range(start, len(field)):
                            if (field[x] == '|'):
                                x = x+1
                                while (field[x]!='|'):
                                    category += field[x] + " "
                                    x=x+1
                                break

                        #category (-1 deletes the last space)
                        category = category[:-1]


			#getting skills
                        for div in skillsbar[i].find_all("div", class_="skills-bar left"):
                            for a in div.find_all('a'):
                                 skills += a.text.strip() + ", "

                        #delete the comma and space in the end
                        skills = skills[:-2]

                        #rating (rating is grabbed from the style attribute. The css width is the rating.)
                        rating = soup.find_all("div", class_='eol-scale')[i]['style'].split(':')

                        #remove the 'px' in the end
                        rating[1] = rating[1][:-2]
                        rating = rating[1]

                        #and finally write it to the CSV
                        row = [name, tagline, rate, rating, level, number_of_jobs, category, skills]
                    	writer.writerow([unicode(t).encode("utf-8") for t in row])

		#write the page number to another file, just so I could 'cat' the progress on terminal
                with open('done.txt','ab') as donefile:
                    donefile.write("\nDoing : " + str(page+1))

                #sleep for 5 minutes
                time.sleep(180)   

            except Exception as exc:
                count += 1

		#write error to another file
                with open('error.txt','ab') as f: f.write("\nError on: " + str(page) + " " + str(exc))

