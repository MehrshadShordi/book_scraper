# Book Scraper

A Python script that scrapes book data (title, price, rating, availability) from [books.toscrape.com](https://books.toscrape.com/), a sandbox site built for scraping practice, and saves the results as both CSV and JSON.

## Features

- Fetches book listings from the site's homepage
- Extracts title, price, star rating, and stock availability for each book
- Handles network errors gracefully (timeout, connection issues) without crashing
- Saves results to `books.csv` and `books.json`
- Prints a summary: total books, average price, and number of books in stock

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`

Install dependencies:
```bash
pip install requests beautifulsoup4
```

## Usage

```bash
python3 book_scraper.py
```

Output files (`books.csv`, `books.json`) will be created in the same folder.

## Sample Output

```
all books : 20
average price : 38.05
available books : 19
```

## Notes

This project was built as a learning exercise to practice web scraping fundamentals: HTTP requests, HTML parsing, error handling, and saving structured data to common file formats.