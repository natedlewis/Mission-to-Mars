#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[16]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[17]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[18]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[19]:


slide_elem.find('div', class_='content_title')


# In[20]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[21]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[22]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[23]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[24]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[25]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[26]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[27]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[28]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[29]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[30]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[31]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for hemis in range(4):
    # Create an empty dictionary inside the for loop.
    hemispheres = {}
    
    # Click on each hemisphere link
    browser.links.find_by_partial_text('Hemisphere')[hemis].click()
    
    # Parse the HTML
    html = browser.html
    hemi_soup = soup(html,'html.parser')
    
    # Retrieve the full-resolution image URL string and title for the hemisphere image
    title = hemi_soup.find('h2', class_='title').text
    img_url = hemi_soup.find('li').a.get('href')
    
    # Store findings into dictionary and append to list
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Navigate back to the beginning to get the next hemisphere image
    browser.back()


# In[32]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[33]:


# 5. Quit the browser
browser.quit()

