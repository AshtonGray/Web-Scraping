from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

username = input("Enter username of user you would like to see:\n")
likes = [] # number of likes to a post
dates = [] # date of each picture
comments = [] # number of comments
posts = None # number of posts user has
photolink = [] # a link to all the photos

# open instagram link
driver = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe")
driver.get("https://www.instagram.com/%s/"%username)

# scroll down
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# get page data
content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")

# get the links to all pictures from page data
for link in soup.find_all('div',class_="v1Nh3 kIKUG _bz0w"):
    for i in link.find_all('a'):
        photolink.append(i.get('href'))

# go through each link and open in new tab
for link in photolink:
    driver.get("https://www.instagram.com%s"%link)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    # get number of likes
    if soup.find_all('div',class_="Nm9Fw") == []: # checking if empty list (video)
        for view in soup.find_all('div', class_="HbPOm _9Ytll"):
            #print(view.get_text())
            likes.append(view.get_text())
    else:# it is a photo, get likes
        for like in soup.find_all('div', class_="Nm9Fw"):
            #print(like.get_text())
            likes.append(like.get_text())
    # get date of photo
    for date in soup.find_all('a', class_="c-Yi7"):
        dates.append(date.get_text())
        #print(date.get_text())

    # get number of comments
    comments.append(len(soup.find_all('ul', class_="Mr508")))
    # need to get the nested comments

driver.quit()

data = pd.DataFrame({'Number of Likes':likes, 'Date':dates, 'Number of Comments':comments})
data.to_csv('instagram.csv', index = False, encoding='utf-8')

