from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import networkx as nx
import matplotlib.pyplot as plt
import time


# Method for scrolling down the twitter page
def scrolldown():
    for i in range(30):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(.3)

# Waiting for twitter posts to load
def wait():
    WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l']")
        ))

edges = []
driver = webdriver.Chrome()
visited = set()
visited.add('oslo')
visited.add('bergen')
tmp_links = []

counter = 0
def find_hashtag(hashtag):
    global counter
    if counter < 20:
        url = f'https://twitter.com/hashtag/{hashtag}?src=hashtag_click'
        driver.get(url)
        wait()
        scrolldown()
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        hashtags = bs.find_all('a', {'href': re.compile('\/hashtag\/.*')})
        for link in hashtags:
            try:
                hashtag_text = link.get_text()
                if hashtag_text not in visited:
                    if hashtag_text.startswith('#'):
                        tmp_links.append(hashtag_text[1:].lower())

                url = link.attrs['href']
                print(hashtag_text)
                edges.append((f'#{hashtag}', hashtag_text))
            except NoSuchElementException:
                continue
        for links_v in visited:
            for links_n in tmp_links:
                if links_n == links_v:
                    tmp_links.remove(links_n)
        print(len(edges))
        print(len(visited))
        counter = counter + 1
        visit_next = tmp_links.pop(0)
        visited.add(visit_next)
        find_hashtag(visit_next)     

find_hashtag("Oslo")
counter = 0
find_hashtag("Bergen")

print(edges)

G = nx.Graph()
G.add_edges_from(edges)
nx.draw(G, with_labels=True)
name = "network_test"
nx.write_graphml(G, f"{name}.graphml")
plt.show()

driver.quit()