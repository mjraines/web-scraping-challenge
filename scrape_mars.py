# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    Mars_News_dict = Mars_News()
    Mars_Featured_Image_dict = Mars_Featured_Image()
    Mars_Fact_dict = Mars_Fact()
    Mars_Hemispheres_dict = Mars_Hemispheres()

    mars_dict = {**Mars_News_dict, **Mars_Featured_Image_dict, **Mars_Fact_dict, **Mars_Hemispheres_dict}

    return mars_dict

def Mars_News():
    # Setup splinter
    executable_path = {'executable_path': '/Users/Melissa/anaconda3/Library/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url for NASA Mars News -- Latest News
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Extract article title and paragraph text
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    print(news_title)
    print(news_p)

    news_title = "10.9 Million Names Now Aboard NASA's Perseverance Mars Rover"
    news_p = "As part of NASA's 'Send Your Name to Mars' campaign, they've been stenciled onto three microchips along with essays from NASA's 'Name the Rover' contest. Next stop: Mars."

    Mars_News_dict ={}
    Mars_News_dict['news_title'] = news_title
    Mars_News_dict['news_paragraph'] = news_p
    return Mars_News_dict

def Mars_Featured_Image():
    # Setup splinter
    executable_path = {'executable_path': '/Users/Melissa/anaconda3/Library/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url for JPL Featured Space Image
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    # Create bs & parser
    html = browser.html
    image_soup = bs(html, 'html.parser')

    header = soup.find('div', class_='header')

    # Open up full image
    status = True
    while status:
        try:
            browser.links.find_by_partial_text('FULL IMAGE').click()

            html = browser.html
            soup = bs(html, 'html.parser')

            image_box = soup.find('div', class_='fancybox-inner')
            featured_image_url = image_url.replace('index.html', '') + image_box.img['src']
            featured_image_url
            status = False
        except:
            pass
    

    browser.quit()

    Mars_Featured_Image_dict = {}
    Mars_Featured_Image_dict['featured_image_url'] = featured_image_url

    return Mars_Featured_Image_dict

def Mars_Fact():

    # Setup splinter
    executable_path = {'executable_path': '/Users/Melissa/anaconda3/Library/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Create BeautifulSoup object & html parser 
    html = browser.html
    soup = bs(html, 'html.parser')

    tables = pd.read_html(url)
    table = tables[0]
    table.columns = ['Key: Comparisons', 'Mars', 'Earth']
    table

    table_html = table.to_html()
    Mars_Fact_dict= {'table_html': table_html}

    browser.quit()

    return Mars_Fact_dict

def Mars_Hemispheres():

    # Setup splinter
    executable_path = {'executable_path': '/Users/Melissa/anaconda3/Library/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create BeautifulSoup object & html parser 
    html = browser.html
    soup = bs(html, 'html.parser')

    images = soup.find_all('div', class_='description')

    image_list = []
    for image in images:
        image_dict = {}
        image_title = image.a.h3.text
        image_dict['title'] = image_title
    
        browser.links.find_by_partial_text(image_title).click()
    
        new_html = browser.html
        new_soup = bs(new_html, 'html.parser')
    
        download = new_soup.find('div', class_='downloads')
        original = download.find_all('li')[1].a['href']
        image_dict['img_url'] = original
        image_list.append(image_dict)
    
        browser.back()
    browser.quit()
    
    Mars_Hemispheres_dict = {}
    Mars_Hemispheres_dict['image_urls'] = image_list
    
    return Mars_Hemispheres_dict  
   
