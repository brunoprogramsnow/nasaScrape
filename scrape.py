from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

def runScrape():

    def init_browser():

        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        return Browser("chrome", **executable_path, headless=True)


    def scrape_mars_nasa():
        browser = init_browser()

        # Visit site
        url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        # Get the news title
        news_title1 = soup.find("div",{"class":"content_title"})
        news_title = news_title1.find("a").text
       
        # Get the news paragraph text
        news_p = soup.findAll("div", {"class": "article_teaser_body"})[0].text

        # Store data in a dictionary
        mars_news_title = {
            "news_title": news_title,
            "news_p": news_p
        }

        # Close the browser after scraping
        browser.quit()

        # Return results
        return mars_news_title

    scrape_mars_nasa()

    def scrape_mars_jpl():
        browser = init_browser()

        # Visit site
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        # Get featured image
        get_featured_image_url= soup.find('article', {"class":"carousel_item"})["style"]
        featured_image_split = get_featured_image_url.split("background-image: url(")[1]
        featured_image_split2=featured_image_split.split(")")[0]
        featured_image_split3 = featured_image_split2.split("'")[1]
        
        base_url = "https://www.jpl.nasa.gov"
        
        featured_image_url = base_url + featured_image_split3


        # Store data in a dictionary
        mars_jpl_data = {
            "featured_image_url": featured_image_url
        }

        # Close the browser after scraping
        browser.quit()

        # Return results
        return mars_jpl_data

    scrape_mars_jpl()

    def scrape_mars_weather():
        browser = init_browser()

        # Visit site
        url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        # Get featured image
        mars_weather= soup.find('p', {"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text

        # Store data in a dictionary
        mars_weather_data = {
            "mars_weather": mars_weather
        }

        # Close the browser after scraping
        browser.quit()

        # Return results
        return mars_weather_data

    scrape_mars_weather()

    # get mars data from pandas
    mars_table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_table_url , encoding= "utf-8")
    tables

    #convert to df
    type(tables)
    mars_df = tables[0]
    mars_df.columns = ['Data Name', 'Data Value']
    mars_df.head()

    #html 
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    html_table
    mars_df.to_html('mars_table.html')
    # !open mars_table.html

    #hemisphere images
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    #add all to python dict
    def pythondict():
        all_mars_data = {
            "mars_news_title": scrape_mars_nasa(),
            "mars_jpl_data": scrape_mars_jpl(),
            "mars_weather_data":scrape_mars_weather(),
            "hemisphere_image_urls": hemisphere_image_urls       
        }
        return all_mars_data
    pythondict()

runScrape()


