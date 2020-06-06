# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt



# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Full Scrape function.

def scrape():

    # NASA Mars News Site Web Scraper
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # Visit Nasa news url.
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")

    try:

        slide_element = news_soup.select_one("ul.item_list li.slide")
    
        slide_element.find("div", class_="content_title")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
        news_title = slide_element.find("div", class_="content_title").get_text()
        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        news_title = None
        news_paragraph = None

    # Exit Browser.
    browser.quit()

    # Print Title and Text.
    print(f'Title: {news_title}\nText: {news_paragraph}')
    

    #################################################
    # JPL Mars Space Images - Featured Image
    #################################################

    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path)

    # Visit the url for JPL Featured Space Image.
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()


    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.links.find_by_partial_text("more info")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    try:
        image_url = image_soup.select_one("figure.lede a img").get("src")
        image_url

    # Use Base URL to Create Absolute URL
        image_url = f"https://www.jpl.nasa.gov{image_url}"
        print(image_url)
    except AttributeError:

        image_url = None

    # Exit Browser.
    browser.quit()

    #################################################
    # Mars Weather
    #################################################
    # Visit the Mars Weather Twitter Account
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)


    # Visit the url for Mars Weather twitter account.
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # HTML Object.
    html = browser.html 

    # Parse HTML with Beautiful Soup
    weather_soup = BeautifulSoup(html, "html.parser")

    # Retrieve ALL 'ol' tags and save to variable 'tweets'.
    tweets_tags = weather_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    tweets=[]

    # Iterate through all 'tweets' and find text in 'p' tag.
    # Break for most recent tweet if keyword 'InSight' in text.
    # Otherwise move onto next tweet.

    for x in tweets_tags:
        if 'InSight' in x.text:
            print(x)
            tweets.append(x.text)
            break
        else: 
            continue

    # Exit Browser.
    browser.quit()

    #################################################
    # Mars Facts
    #################################################
    # Mars Facts Web Scraper

    # URL for Mars Facts.
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Data']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    mars_df.to_html()

    mars_facts = mars_df.to_dict(orient='records')  # Here's our added param..

    # Display mars_df
    mars_df

    # Convert DF to HTML string.
    mars_facts = mars_df.to_html(header=True, index=True)
    print(mars_facts)

    #################################################
    # Mars Hemispheres
    #################################################

    # Visit the USGS Astrogeology Science Center Site
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Visit the url for USGS Astrogeology.
    astrogeo_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeo_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    astrogeo_soup = BeautifulSoup(html, "html.parser")

    # Store main URL in a variable so that 'href' can be appended to it after each iteration.
    main_astrogeo_url = "https://astrogeology.usgs.gov"

    # Each link is located in 'div' tag, class "item".
    # Locate all 4 and store in variable.
    hems_url = astrogeo_soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hemis_url = []

    for hem in hems_url:
        hem_url = hem.find('a')['href']
        hemis_url.append(hem_url)

    browser.quit()

    # Create list of dictionaries called hemisphere_image_urls.
    # Iterate through all URLs saved in hemis_url.
    # Concatenate each with the main_astrogeo_url.
    # Confirm the concat worked properly: confirmed.
    # Visit each URL.

    hemisphere_image_urls = []
    for hemi in hemis_url:
        hem_astrogeo_url = main_astrogeo_url + hemi
        print(hem_astrogeo_url)
        
        # Run browser/driver
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        browser = Browser("chrome", **executable_path, headless=False)
        
        browser.visit(hem_astrogeo_url)
        
        # HTML Object.
        html = browser.html

        # Parse HTML with Beautiful Soup
        hemi_soup = BeautifulSoup(html, "html.parser")

        # Locate each title and save to raw_title, to be cleaned.
        raw_title = hemi_soup.find("h2", class_="title").text
        
        # Remove ' Enhanced' tag text from each "title" via split on ' Enhanced'.
        title = raw_title.split(' Enhanced')[0]
        
        # Locate each 'full.jpg' for all 4 Hemisphere URLs.
        img_url = hemi_soup.find("li").a['href']
        
        # Append both title and img_url to 'hemisphere_image_url'.
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        browser.quit()

    print(hemisphere_image_urls)

    """ Mars Data Dictionary - MongoDB """

    # Create empty dictionary for all Mars Data.
    mars_data = {}

    # Append news_title and news_paragraph to mars_data.
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    # Append featured_image_url to mars_data.
    mars_data['img_url'] = img_url

    # Append mars_weather to mars_data.
    mars_data['tweets'] = tweets

    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = mars_facts

    # Append hemisphere_image_urls to mars_data.
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print("Scrape Complete!!!")

    return mars_data