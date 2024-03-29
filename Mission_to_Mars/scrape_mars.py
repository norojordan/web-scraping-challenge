# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# create scrape function
def scrape():
    browser = init_browser()

    #use browser to open the url
    url = "https://redplanetscience.com"
    # open the url
    browser.visit(url)

    # create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    #Get the latest news
    news_title = soup.find('div',class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # for Mars latest image visit the url and get the full image url
    image_url ="https://spaceimages-mars.com"
    browser.visit(image_url)

    # create BeautifulSoup object; parse with 'html.parser'
    image_html = browser.html   
    soup = bs(image_html, "html.parser")

    #Get the featured space image
    image = soup.find("img", class_="headerimage fade-in")
    featured_image_url = 'https://spaceimages-mars.com/image/featured/mars1.jpg'

     # for Mars facts visit the url and get the full image url
    facts_url ="https://galaxyfacts-mars.com/"
    browser.visit(facts_url)

    # create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    facts_html = browser.html   
    soup = bs(facts_html, "html.parser")

    # Use Pandas to get and read the table
    table = pd.read_html(facts_url)

    #Pull out the first table on the page and put into a dataframe
    mars_facts_df = table[0]

    #Clean dataframs
    mars_facts_df.columns =['Facts','Mars','Earth']
    mars_facts_df = mars_facts_df.drop(mars_facts_df.index[:1])
    mars_facts_df.set_index('Facts', inplace=True)

    # convert the data to an HTML table string
    html_table = mars_facts_df.to_html()
    html_table.replace('\n', '')    

    # get the url for Mars Hemispheres
    hemisphere_url ="https://marshemispheres.com/"
    browser.visit(hemisphere_url)

    # create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    hemi_html = browser.html
    soup = bs(hemi_html, "html.parser")

    image = soup.find_all("div", class_="description")



    img_urls_list = []

    # loop through image data to find title and url info
    for i in image:
    
        title = i.find("h3").text
        img_url = i.find('a')['href']
   
        each_url = 'https://marshemispheres.com/' + img_url
    
         # use requests to get full images for each url 
        response = requests.get(each_url)
    
        # create soup object
        soup = bs(response.text,"html.parser")
    
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
    
        # create full image url
        full_url = 'https://marshemispheres.com/'+ new_url
    
        #make a dict and append to the list
        img_urls_list.append({"title": title, "img_url": full_url}) 
                          


    # create mars data dictionary to hold data
    mars_data = {
        "news_title": news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_img_urls": img_urls_list
    }

    # close the browser after scraping
    browser.quit()

    # return results
    return mars_data
