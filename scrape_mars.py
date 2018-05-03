from bs4 import BeautifulSoup as BS
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

def scrape():

	#NASA news

	#set up splinter browser
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless = False)

	#visit url
	url = "https://mars.nasa.gov/news/"
	browser.visit(url)

	#pull html text and parse
	html_code = browser.html
	soup = BS(html_code, "html.parser")

	#grab needed info
	news_title = soup.find('div', class_="bottom_gradient").text
	news_p = soup.find('div', class_="rollover_description_inner").text

	#latest featured image
	url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	url_base = 'https://www.jpl.nasa.gov'

	response = requests.get(url)
	soup = BS(response.text, 'html.parser')

	result = soup.find('article', class_='carousel_item').attrs
	style = str(result['style'])
	trim1 = style.replace("background-image:", "")
	trim2 = trim1.replace(" url('", "")
	image = trim2.replace("');", "")
	featured_image_url = url_base + image

	#NASA Twitter


	#url of the twitter account
	url = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(url)
	soup = BS(response.text, 'html.parser')
	mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


	#mars facts

	#mars facts url and splinter visit
	facts_url = "https://space-facts.com/mars/"
	browser.visit(facts_url)

	#get html
	facts_html = browser.html

	soup = BS(facts_html, 'html.parser')
	#get the entire table
	table_data = soup.find('table', class_="tablepress tablepress-id-mars")
	#find all instances of table row
	table_all = table_data.find_all('tr')

	#set up lists to hold td elements which alternate between label and value
	parameters = []
	values = []

	#for each tr element append the first td element to labels and the second to values
	for tr in table_all:
    	td_elements = tr.find_all('td')
    	parameters.append(td_elements[0].text)
    	values.append(td_elements[1].text)

    #make a data frame and view
	mars_facts_df = pd.DataFrame({
    "Parameters": parameters,
    "Values": values
	})
    
    # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False)
    fact_table

	#mars hemisphere
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	url_base = "https://astrogeology.usgs.gov"

	browser = Browser('chrome', headless=False)
	browser.visit(url)
	soup = BS(browser.html, 'html.parser')

	results = soup.find_all('div', class_="item")

	url_list = []

	for result in results:
    	link = result.find('a')['href']
    	url_list.append(link)

    hemisphere_url_images = []

	for x in url_list:
    	url = url_base + x
        
    browser.visit(url)
    
    # Sleep script to ensure the page fully loads
    time.sleep(5)
    
    soup = BS(browser.html, 'html.parser')
    
    # Grab image url
    result1 = soup.find('img', class_="wide-image")
    image = url_base + result1["src"]
    
    # Grab page title and remove "Enhanced" from string
    result2 = soup.find('h2', class_='title')
    title = result2.text
    title = title.rsplit(' ', 1)[0]
    
    dict_hem = {"Title": title, "Image URL": image}
    hemisphere_url_images.append(dict_hem)
    
    time.sleep(10)


     mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict




 
