# Book Scraper

A Python script that scrapes **all books across all pages** of [books.toscrape.com](https://books.toscrape.com/), a sandbox site built for scraping practice. It handles pagination, retries failed requests, logs everything, and saves results as CSV, JSON, and Excel file(xlsx).

## Features

- **Full pagination**: automatically follows the "next" button through all pages (no hardcoded page count)
- **Retry logic**: retries on timeout (e.g. slow connection) up to 5 times before giving up on a page
- **Status code validation**: treats non-200 responses as failures instead of silently processing bad pages
- **Logging**: every fetch, retry, extraction, and error is logged to `scraper.log` with timestamps
- **multi-output**: saves results to `books.csv`, `books.json`, and `books.xlsx`
- **Summary report**: prints total books, average price, and number in stock

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`

Install dependencies:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Usage

```bash
python3 book_scraper.py
```

Output files (`books.csv`, `books.json`, `books.xlsx`, `scraper.log`) are created in the same folder.

## Sample Output

```
all books : 1000
average price : 35.07
available books : 1000
```

## Sample Log

```
2026-10-12 01:45:22,991 , INFO , Start The Process
2026-10-12 01:45:25,784 , INFO , Successfully fetched https://books.toscrape.com/catalogue/page-1.html
2026-10-12 01:45:25,833 , INFO , Extracted 20 Books
2026-10-12 01:45:26,848 , INFO , Page 1 ended
...
2026-10-12 01:48:38,286 , INFO , End Of Process - Number Of Books Fetched : 1000
```

## How It Works

1. Starts at page 1 and fetches each book's title, price, star rating, and stock status.
2. Checks for a "next page" link to know when to stop (works even if the site's page count changes).
3. On a timeout, retries the same page up to 5 times with a short delay before giving up.
4. On a connection error (e.g. unreachable domain), stops immediately rather than retrying pointlessly.
5. Saves progress to CSV/JSON/xlsx(Excel) after each page and logs every step for later review.

## Notes

Built as a learning project to practice real-world scraping concerns: pagination, network error handling, retry strategies, and logging -- the kind of robustness a one-off script usually lacks.

---

# اسکرپر کتاب

یک اسکریپت پایتون که **همه‌ی کتاب‌های تمام صفحات** سایت [books.toscrape.com](https://books.toscrape.com/) -- یک سایت آزمایشی برای تمرین اسکرپینگ -- را استخراج می‌کند. این اسکریپت صفحه‌بندی (pagination) را مدیریت می‌کند، درخواست‌های ناموفق را دوباره تلاش می‌کند، همه‌چیز را لاگ می‌کند، و نتیجه را به‌صورت CSV , JSON و جدول اکسل (xlsx) ذخیره می‌کند.

## ویژگی‌ها

- **صفحه‌بندی کامل**: به‌صورت خودکار دکمه‌ی "next" را دنبال می‌کند تا همه‌ی صفحات را بگیرد (بدون نیاز به دانستن تعداد صفحات از قبل)
- **منطق تلاش مجدد (Retry)**: در صورت تایم‌اوت (مثلاً اتصال کند)، تا ۵ بار دوباره تلاش می‌کند قبل از صرف‌نظر کردن از آن صفحه
- **اعتبارسنجی کد وضعیت**: پاسخ‌های غیر از ۲۰۰ را به‌عنوان خطا در نظر می‌گیرد، نه اینکه بی‌صدا صفحه‌ی نامعتبر را پردازش کند
- **لاگ‌گیری**: هر درخواست، تلاش مجدد، استخراج داده و خطا با زمان دقیق در فایل `scraper.log` ثبت می‌شود
- **خروجی چندگانه**: نتایج در `books.csv` , `books.json`و ‍‍‍‍‍‍‍‍‍‍‍`books.xlsx` ذخیره می‌شوند
- **گزارش خلاصه**: تعداد کل کتاب‌ها، میانگین قیمت، و تعداد موجود در پایان چاپ می‌شود

## پیش‌نیازها

- Python 3.8 یا بالاتر
- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`

نصب پیش‌نیازها:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## نحوه‌ی اجرا

```bash
python3 book_scraper.py
```

فایل‌های خروجی (`books.csv`, `books.json`, `books.xlsx`, `scraper.log`) در همان پوشه ساخته می‌شوند.

## نمونه‌ی خروجی

```
all books : 1000
average price : 35.07
available books : 1000
```

## نحوه‌ی عملکرد

۱. از صفحه‌ی ۱ شروع می‌کند و عنوان، قیمت، امتیاز ستاره‌ای و وضعیت موجودی هر کتاب را می‌گیرد.
۲. برای فهمیدن زمان توقف، وجود لینک "next" را بررسی می‌کند (حتی اگر تعداد صفحات سایت تغییر کند، درست کار می‌کند).
۳. در صورت تایم‌اوت، همان صفحه را تا ۵ بار با یک تأخیر کوتاه دوباره تلاش می‌کند.
۴. در صورت خطای اتصال (مثلاً دامنه‌ی غیرقابل‌دسترس)، بدون تلاش بی‌فایده‌ی مجدد، فوراً متوقف می‌شود.
۵. بعد از هر صفحه پیشرفت را در CSV/JSON/xlsx(فایل اکسل) ذخیره می‌کند و هر مرحله را برای بررسی بعدی لاگ می‌کند.

## توضیحات

این پروژه برای تمرین مسائل واقعی اسکرپینگ ساخته شده: صفحه‌بندی، مدیریت خطای شبکه، استراتژی تلاش مجدد، و لاگ‌گیری -- نوع مقاوم‌بودنی که یک اسکریپت یک‌بارمصرف معمولاً ندارد.
