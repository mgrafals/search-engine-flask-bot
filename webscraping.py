#!/usr/bin/env python
# coding: utf-8

# In[190]:


# Allows connection to chrome web browser
# Allows connection to MS SQL Server
#get_ipython().system('pip install selenium')
#get_ipython().system('pip install pyodbc')


# In[191]:


import time
import pyodbc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import string  # Import the string module to handle punctuation removal
import re


# In[192]:


# Download the stopwords list if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')


# In[193]:


# Set up English stopwords list
stop_words = set(stopwords.words('english'))

# Function to remove stop words from the search query
def remove_stop_words(query):
    word_tokens = word_tokenize(query)
    filtered_query = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_query)

# Function to perform search query cleanup
def clean_search_query(query):
    # Remove punctuation marks from the query
    query = re.sub(r'[^\w\s]', '', query)
    cleaned_query = remove_stop_words(query)
    return cleaned_query


# In[194]:


# Establish connection to MS SQL Server
# Server=XPS15
# Driver={SQL Server Native Client 11.0}
# Driver={ODBC Driver 17 for SQL Server}
try:
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=(local);'
                          'Database=MY_CUSTOM_BOT;'
                          'Trusted_Connection=yes;')
    print("Connected Successfully")
except Exception as e:
    print(e)


# In[195]:


# Function to save search query to SQL Server
def save_search_query(original_query, cleaned_query):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SearchQueries (OriginalQuery, CleanedQuery) VALUES (?, ?)", original_query, cleaned_query)
        conn.commit()
        print("Search query saved successfully.")

        # Retrieve the ID of the saved search query
        cursor.execute("SELECT @@IDENTITY")  # Change to use @@IDENTITY to retrieve the last inserted identity value
        search_query_id = cursor.fetchone()[0]

        return search_query_id  # Return the search query ID
    except Exception as e:
        print("Error occurred while saving search query:", e)
        
# Function to save URLs to SQL Server
def save_urls(search_query_id, search_engine, urls):
    try:
        cursor = conn.cursor()
        for url in urls:
            cursor.execute("INSERT INTO URLs (QueryID, SearchEngine, URL) VALUES (?, ?, ?)", search_query_id, search_engine, url)
        conn.commit()
        print("URLs saved successfully.")
    except Exception as e:
        print("Error occurred while saving URLs:", e)

# Function to count frequency of search terms in URLs and save to SQL Server
def save_search_term_frequency(search_query_id, query, urls):
    try:
        cursor = conn.cursor()
        for url in urls:
            # Retrieve the URLID associated with the URL
            cursor.execute("SELECT URLID FROM URLs WHERE URL = ?", url)
            url_id = cursor.fetchone()[0] # if cursor.rowcount > 0 else None

            term_frequency = {}
            for term in query.split():
                term_frequency[term] = 0
                
            for term in query.split():
                if term.lower() in url.lower():
                    term_frequency[term] += 1
                    
            for term, frequency in term_frequency.items():
                # Insert search term frequency data with URLID
                cursor.execute("INSERT INTO SearchTermFrequency (QueryID, URLID, SearchTerm, Frequency) VALUES (?, ?, ?, ?)", search_query_id, url_id, term, frequency)
                
        conn.commit()
        print("Search term frequency saved successfully.")
    except Exception as e:
        print("Error occurred while saving search term frequency:", e)

# In[196]:


# Function to perform Google search
def google_search(query):
    try:
        # Set up headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

        # Initialize WebDriver with headless Chrome
        driver = webdriver.Chrome(options=chrome_options)

        url = f"https://www.google.com/search?q={query}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        search_results = []
        for result in soup.find_all('div'):
            if result.has_attr('data-id') and "https:" in result['data-id']:
                url = result['data-id'].replace("atritem-", "")
                if not url.startswith("https://"):
                    url = "https://" + url
                if url.endswith("/"):
                    url = url[:-1]
                search_results.append(url)

        return search_results

    finally:
        driver.quit()  # Make sure to quit the WebDriver instance

# Function to perform Bing search
def bing_search(query):
    try:
        # Set up headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

        # Initialize WebDriver with headless Chrome
        driver = webdriver.Chrome(options=chrome_options)

        url = f"https://www.bing.com/search?q={query}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        search_results = []
        for result in soup.find_all(True, class_=['pagereco_TTitle','pagereco_TDomain']):
            url = result.find('a')['href']
            if not url.startswith("https://"):
                url = "https://" + url
            if url.endswith("/"):
                url = url[:-1]
            if url not in search_results:
                search_results.append(url)

        for result in soup.find_all(True, class_='tilk'):
            url = result['href']
            if not url.startswith("https://"):
                url = "https://" + url
            if url.endswith("/"):
                url = url[:-1]
            if url not in search_results:
                search_results.append(url)

        return search_results

    finally:
        driver.quit()  # Make sure to quit the WebDriver instance

# Function to perform DuckDuckGo search
def duckduckgo_search(query):
    try:
        # Set up headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

        # Initialize WebDriver with headless Chrome
        driver = webdriver.Chrome(options=chrome_options)

        url = f"https://duckduckgo.com/html/?q={query}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        search_results = []
        for result in soup.find_all('a', class_='result__url'):
            url = result.get_text(strip=True)
            if not url.startswith("https://"):
                url = "https://" + url  # Add "https://" if missing
            if url.endswith("/"):
                url = url[:-1]
            if url not in search_results:               
                search_results.append(url)

        return search_results

    finally:
        driver.quit()  # Make sure to quit the WebDriver instance

# Function to perform Yahoo search
def yahoo_search(query):
    try:
        # Set up headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

        # Initialize WebDriver with headless Chrome
        driver = webdriver.Chrome(options=chrome_options)

        url = f"https://search.yahoo.com/search?q={query}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        search_results = []
        for result in soup.find_all('a'):
            if result.has_attr('data-matarget'):
                url = result['href']
                if not url.startswith("https://"):
                    url = "https://" + url
                if url.endswith("/"):
                    url = url[:-1]
                search_results.append(url)

        return search_results

    finally:
        driver.quit()  # Make sure to quit the WebDriver instance

# In[197]:


# Function to automate the web scraping process
def automate_web_scraping(query):
    try:
        # Clean the search query
        cleaned_query = clean_search_query(query)

        # Save the original and cleaned search queries to SQL Server
        search_query_id = save_search_query(query, cleaned_query)

        # Perform Google search
        google_results = google_search(cleaned_query)
        save_urls(search_query_id, 'Google', google_results)
        save_search_term_frequency(search_query_id, cleaned_query, google_results)

        # Perform Bing search
        bing_results = bing_search(cleaned_query)
        save_urls(search_query_id, 'Bing', bing_results)
        save_search_term_frequency(search_query_id, cleaned_query, bing_results)

        # Perform DuckDuckGo search
        duckduckgo_results = duckduckgo_search(cleaned_query)
        save_urls(search_query_id, 'DuckDuckGo', duckduckgo_results)
        save_search_term_frequency(search_query_id, cleaned_query, duckduckgo_results)

        # Perform Yahoo search
        yahoo_results = yahoo_search(cleaned_query)
        save_urls(search_query_id, 'Yahoo', yahoo_results)
        save_search_term_frequency(search_query_id, cleaned_query, yahoo_results)
        
    except Exception as e:
        print("Error occurred during web scraping:", e)


# In[198]:


# # Test the web scraping automation
# if __name__ == "__main__":
#     query = input('Enter your search query: ')
#     automate_web_scraping(query)


# # In[199]:


# # Close connection
# conn.close()

