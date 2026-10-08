import requests
from bs4 import BeautifulSoup
import json
import csv

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0 ; Win64 ; x64)"}
books_dict = {}
books_list = []
stars_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url):
    try:
        response = requests.get(url, headers=header, timeout=5)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.ConnectTimeout:
        print("timeout - cant reach site")
    except requests.exceptions.ConnectionError:
        print("cant open the site - check your network connection")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error : {e}")


def fetch_data():
    soup = fetch_page("https://books.toscrape.com/")
    if soup is None:
        print("Could not fetch data")
        return
    rows = soup.find_all("article", class_="product_pod")
    for items in rows:
        title = items.find("h3").find("a")["title"]
        price = float(items.find("p", class_="price_color").text.strip().strip("£"))
        stars = items.find("p", class_="star-rating")["class"]
        availability = items.find("p", class_="instock availability").text.strip()
        books_dict[title] = [price, stars_dict[stars[1]], availability]
        books_list.append([title, price, stars_dict[stars[1]], availability])
    save_json()
    save_csv()
    calculate()


def calculate():
    all_price = 0
    available_books = 0
    for items in books_list:
        all_price += items[1]
        if items[3] == "In stock":
            available_books += 1
    avg = all_price / len(books_list)
    print(f"all books : {len(books_list)}")
    print(f"average price : {avg:.2f}")
    print(f"available books : {available_books}")


def save_json():
    with open("books.json", "w") as f:
        json.dump(books_dict, f, ensure_ascii=False)


def save_csv():
    with open("books.csv", "w") as f:
        fieldname = ["title", "price", "stars", "availability"]
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writeheader()
        for items in books_list:
            writer.writerow(
                {
                    "title": items[0],
                    "price": items[1],
                    "stars": items[2],
                    "availability": items[3],
                }
            )


fetch_data()
