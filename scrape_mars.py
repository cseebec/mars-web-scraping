from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict = {}

    # Go to Mars News Site Browser on the google chrome web browser
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    #Initiate beatiful soup for this site
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')
    # Find the latest news title and paragraph from this site
    news_title = mars_soup.find('div', class_='content_title').text
    news_p = mars_soup.find('div', class_="article_teaser_body").text

    # Navigate to another url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    #Initiate beatiful soup for this site
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Find image url 
    image_mars = image_soup.find('img', class_="fancybox-image")['src']
    featured_image_url = url + "/" + image_mars

    #Navigate to another url
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)
    tables = pd.read_html(url)
    mars_earth_df = tables[0]
    mars_earth_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    mars_earth_df.set_index('Mars-Earth Comparison', inplace=True)
    mars_html_table = mars_earth_df.to_html()
    mars_html_table = mars_html_table.replace('\n','')

    #Navigate to another url
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Initiate beautiful soup for this website
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all of the hemisphere names
    headers = soup.body.find_all('h3')
    hemis_extra = []
    for i in headers:
        hemis_extra.append(i.text)
    hemis_extra.remove('Back')
    hemis =[]
    for i in hemis_extra:
        i = i.replace(' Enhanced', '')
        hemis.append(i)
    
    # Find all hemisphere image urls
    # I tried countless different ways of putting this same exact code in a for loop but it did not work
    hemisphere_list = []
    browser.links.find_by_partial_text(hemis[0]).click()
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    image_extension = image_soup.find('img', class_="wide-image")['src']
    image_url = url + image_extension
    hemi_dict = {"title": hemis[0], "image_url": image_url}
    hemisphere_list.append(hemi_dict)
    browser.links.find_by_partial_text('Back').click()

    browser.links.find_by_partial_text(hemis[1]).click()
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    image_extension = image_soup.find('img', class_="wide-image")['src']
    image_url = url + image_extension
    hemi_dict = {"title": hemis[1], "image_url": image_url}
    hemisphere_list.append(hemi_dict)
    browser.links.find_by_partial_text('Back').click()
    
    browser.links.find_by_partial_text(hemis[2]).click()
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    image_extension = image_soup.find('img', class_="wide-image")['src']
    image_url = url + image_extension
    hemi_dict = {"title": hemis[2], "image_url": image_url}
    hemisphere_list.append(hemi_dict)
    browser.links.find_by_partial_text('Back').click()

    browser.links.find_by_partial_text(hemis[3]).click()
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    image_extension = image_soup.find('img', class_="wide-image")['src']
    image_url = url + image_extension
    hemi_dict = {"title": hemis[3], "image_url": image_url}
    hemisphere_list.append(hemi_dict)


    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table": mars_html_table,
        "hemisphere_list": hemisphere_list}

    # Close Browser
    browser.quit()

    return mars_dict