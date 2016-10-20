from selenium import webdriver
from bs4 import BeautifulSoup
import contextlib
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import time, os
import urllib, urlparse

i=0
with contextlib.closing(webdriver.Firefox(firefox_profile=profile)) as driver:    
    driver.get('https://depositfiles.com/login.php')
    html = driver.page_source
    if not "You have Gold access" in html:
        username = driver.find_element_by_name('login')
        username.send_keys('USERNAME)
        password = driver.find_element_by_name('password')
        password.send_keys('PASSWORD')
        button = driver.find_element_by_id('login_btn')
        button.submit()
    time.sleep(10)
    for j in range(1, 29): #number of pages
        driver.get("http://www.freelibros.org/category/salud/page/" + str(j))
        main_html = driver.page_source
        main_soup = BeautifulSoup(main_html)
        titles = main_soup.findAll("h2", class_="entry-title")
        for title in titles:
            if os.path.exists(title.get_text()):
                continue
            book_href = title.a["href"]
            print book_href
            driver.get(title.a["href"])
            html = driver.page_source
            try:
                if ("Enlaces Privados de descarga" in html):
                    driver.find_element_by_xpath("//a[@data-reveal-id='download-public-links']").click()
                time.sleep(5)
                driver.find_element_by_link_text("DepositFiles").click()
                driver.switch_to_window(driver.window_handles[-1])
                time.sleep(15)
                html = driver.page_source
                soup = BeautifulSoup(html)
                url = soup.find("a", { "class" : "df_button df_button_lines hide_download_started" })["href"]
                split = urlparse.urlsplit(url)
                filename =  split.path.split("/")[-1]
                fullfilename = os.path.join(title.get_text(),filename)
                if not os.path.exists(title.get_text()):
                    os.makedirs(title.get_text().encode('utf-8'))
                urllib.urlretrieve(url, fullfilename.encode('utf-8'))
                i = i+1
                print "Got file: ", str(i), ", URL: ", str(book_href)
                driver.switch_to_window(driver.window_handles[0])
                time.sleep(5)

            except:
                i = i+1
                print "Not gotten: ", str(i), str(book_href)


