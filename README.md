# Custom Search Engine with Real-Time Data Aggregation

This project is a custom-built search engine web application that performs real-time web scraping across multiple search engines (Google, Bing, DuckDuckGo, Yahoo), stores search query data in a SQL Server database, and presents results in an organized and user-friendly interface.

## Features
- Real-time query scraping using Selenium and BeautifulSoup
- Data stored in a SQL Server database with structured tables for queries, URLs, and search term frequencies
- Dynamic Flask front-end to display URLs by relevance
- Duplicate filtering and frequency aggregation of search terms
- Integrated search functionality from both the home and results pages

##  Technologies Used
- **Python**, **Flask**
- **SQL Server** (T-SQL)
- **Selenium**, **BeautifulSoup**
- **HTML/CSS**
- **Jupyter Notebook**

## How to Run

1. **Set Up the Database**
   - Run the SQL file `Custom Bot Database Query v2.0.sql` in SQL Server Management Studio to initialize the schema.

2. **Set Up the Environment**
   - Install required libraries:
     ```bash
     pip install flask selenium pyodbc nltk beautifulsoup4
     ```

   - Download NLTK corpora:
     ```python
     import nltk
     nltk.download('stopwords')
     nltk.download('punkt')
     ```

3. **Start the App**
   - Run the Flask application from your terminal:
     ```bash
     python webscraping.py
     ```
   - Go to `http://127.0.0.1:5000/` in your browser.

## Project Structure

├── webscraping.py<br/>
├── app.ipynb<br/>
├── Custom Bot Database Query v2.0.sql<br/>
├── static/<br/>
│ ├── styles.css<br/>
│ └── logo.png<br/>
├── templates/<br/>
│ ├── index.html<br/>
│ └── search_results.html<br/>
├── presentation/<br/>
│ └── Project Presentation.pptx

