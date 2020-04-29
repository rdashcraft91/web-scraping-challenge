# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

# Connect Chromedriver to Browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Run url through chromedriver browser
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(5)

    # Scrape relevant data

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Set path to first article
    article = soup.find('li', class_='slide')

    # Finding the First Article Title
    slide_text = article.find('div', class_='list_text')
    title_content = slide_text.find('div', class_='content_title')
    news_title = title_content.text

    #Finding the First Article Body
    body_content = slide_text.find('div', class_="article_teaser_body")
    news_p = body_content.text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Scrape relevant data

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Set path to Featured Section
    main = soup.find('div', class_="carousel_container")

    # Finding the Image URL
    article = main.find('article', class_="carousel_item")
    image = article.get('style')
    image_split = image.split("'")
    image_url = image_split[1]

    # Create full link to Featured Image
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(10)

    # Scrape relevant data

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Selecting all tweet blocks
    tweets = soup.select('div[style*="translateY(0px)"]')

    # Finding the tweet text within each block
    first_block = tweets[0]
    all_first_tweet_text = first_block.find_all('span')

    # Selecting the correct text
    mars_weather = all_first_tweet_text[4].text

    mars_table_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_table_url, header=None)

    mars_df = mars_facts[0]
    mars_df

    mars_table_html = mars_df.to_html(header=False, index=False)
    mars_df.to_html('mars_table.html', header=False, index=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(5)

    hemispheres = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']
    hemisphere_images_urls = []

    for item in hemispheres:
        
        # Scrape relevant data
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Finding the Image URL
        browser.click_link_by_partial_text(f'{item}')
        current_url = browser.url
        response = requests.get(current_url)
        time.sleep(5)
        soup = BeautifulSoup(response.text, 'html.parser')
        wide_image = soup.find('div', class_="wide-image-wrapper")
        downloads = wide_image.find('div', class_="downloads")
        image_one = downloads.find('a')
        href_one = image_one['href']
        new_dict = {'title': item, 'img_url': href_one}
        hemisphere_images_urls.append(new_dict)
        
        browser.visit(url)
        time.sleep(5)
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_table_html": mars_table_html,
        "hemisphere_data": hemisphere_images_urls
    }

    browser.quit()

    return mars_data

if __name__ == "__main__":
    print("\nTesting Data Retrieval...\n")
    print(scrape())
    print("\nProcess Complete!\n")