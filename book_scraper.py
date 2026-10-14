import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
import pandas

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s , %(levelname)s , %(message)s",
)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0 ; Win64 ; x64)"}
books_dict = {}
books_list = []
stars_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url, max_try=5):
    for i in range(1, max_try):
        try:
            response = requests.get(url, headers=header, timeout=5)
            response.encoding = "utf-8"
            if response.status_code != 200:
                logging.error(f"{response.status_code} Error for {url}")
                return "error"
            logging.info(f"Successfully fetched {url}")
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.ConnectTimeout:
            logging.warning(f"Timeout on {url} - Can't reach site")
            return "error"
        except requests.exceptions.ConnectionError:
            logging.warning(
                f"Connection Error on {url} - Check Your Network Connection"
            )
            return "error"
        except requests.exceptions.HTTPError as e:
            logging.warning(f"Http Error on {url} - {e}")
            return "error"
        except requests.Timeout:
            logging.warning(f"Timeout on {url} - {i}. retrying")
    else:
        logging.error(f"Can't fetch {url} - Skipping")
        return "timeout"


def fetch_data(url):
    soup = fetch_page(url)
    if soup is None:
        logging.warning(f"Could not fetch data from {url}")
        return
    elif soup == "timeout":
        return "Failed to fetch"
    elif soup == "error":
        return "Connection Error"
    rows = soup.find_all("article", class_="product_pod")
    logging.info(f"Extracted {len(rows)} Books")
    for items in rows:
        title = items.find("h3").find("a")["title"]
        price = float(items.find("p", class_="price_color").text.strip().strip("£"))
        stars = items.find("p", class_="star-rating")["class"]
        availability = items.find("p", class_="instock availability").text.strip()
        books_dict[title] = [price, stars_dict[stars[1]], availability]
        books_list.append([title, price, stars_dict[stars[1]], availability])
    save_json()
    save_csv()
    save_excel()
    time.sleep(1)
    return soup.find("li", class_="next")


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


def save_excel():
    with pandas.ExcelWriter("books.xlsx") as writer:
        datafield = pandas.DataFrame(
            books_list, columns=["title", "price", "stars", "availability"]
        )
        datafield.to_excel(writer, index=False)


current_page = 1


def __main__():
    logging.info("Start The Process")
    global current_page
    while True:
        result = fetch_data(
            f"https://books.toscrape.com/catalogue/page-{current_page}.html"
        )
        if result == "Failed to fetch":
            current_page += 1
            logging.warning(f"Skipping to Page {current_page}")
        elif result == "Connection Error":
            break
        elif result:
            logging.info(f"Page {current_page} ended")
            current_page += 1
        else:
            calculate()
            break


__main__()
logging.info(f"End Of Process - Number Of Books Fetched : {len(books_list)}")


# def convert_to_excel():
#     csv_data = pandas.read_csv("books.csv")
#     print(csv_data.head())
#     print(csv_data.describe())
#     print(csv_data["price"].mean())
#     print(csv_data["price"].max())

#     expensive_books = csv_data[
#         csv_data["price"] > csv_data["price"].mean()
#     ].sort_values("price", ascending=False)
#     cheap_books = csv_data[csv_data["price"] <= 20].sort_values("price")
#     print(f"above avg : {len(expensive_books)}")
#     print(expensive_books.head())
#     print(f"below avg : {len(cheap_books)}")
#     print(cheap_books.head())
#     books_by_rating = csv_data.groupby("stars")["price"].agg(["mean", "count"])
#     print(books_by_rating)
#     with pandas.ExcelWriter("books_report.xlsx") as writer:
#         csv_data.to_excel(writer, sheet_name="All Books", index=False)
#         expensive_books.to_excel(writer, sheet_name="Expensive Books", index=False)
#         cheap_books.to_excel(writer, sheet_name="Cheap Books", index=False)
#         books_by_rating.to_excel(writer, sheet_name="By Rating")
#         pandas.concat([expensive_books.head(10), cheap_books.head(10)]).to_excel(
#             writer, sheet_name="Top And Bottom", index=False
#         )

# convert_to_excel()
