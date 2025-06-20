from pyquery import PyQuery
import requests
import pandas as pd
import datetime
import time
import random
from word2number import w2n

baseurl = "https://books.toscrape.com"
main_page = "https://books.toscrape.com/catalogue/page-"
catalogue_pages = "https://books.toscrape.com/catalogue/"
extension = ".html"


all_books = []
log_timer = []

def loadbaseurl(baseurl):
    base_source = getSource(baseurl)
    pq = get_pq(base_source)

    total_resuts = 0
    books_per_page = 0

    total_resuts = pq("form.form-horizontal strong:first").text()
    books_per_page = pq("form.form-horizontal strong:last").text()
    log_timer.append(f" total records found {total_resuts}, each page has {books_per_page}")
    
    total_pages = int(total_resuts) / int(books_per_page)
    if not isinstance(total_pages,float):
        print("Pages not found..")
        return 0,0
    
    return total_pages, books_per_page
    
def get_pq(source):
    return PyQuery(source)

def getSource(url):
    r1 = random.randint(5, 10)
    time.sleep(r1)
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Couldnt get any response!")
        return None

    return response.text
    
def book_detail(book):
    book_page = get_pq(getSource(book)) 
    name = book_page('article.product_page h1').text()
    price = book_page('article.product_page p.price_color').eq(0).text()
    if price:
        price = price.split("£")[-1] 
        price = float(price)
    rating = book_page('article.product_page p.star-rating ').attr('class')
    if rating:
        raa = rating.split()[-1] #if len(rating.split()) > 1 else rating
        rating = w2n.word_to_num(raa)
    stock = book_page('article.product_page p.availability').eq(0).text()
    if stock:
        in_stock = stock.split('(')[0]
    qty = stock.split("(")[1].split(" ")[0]
    qty = int(qty)
    category = book_page("ul.breadcrumb li").eq(2).text()

    return {
                        'url': book,
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'stock': in_stock.strip(),
                        'quantity': qty,
                        'category': category
                    }

def readSource(content):
    return content.splitlines()

def get_time():
    return time.strftime("%H:%M:%S", time.localtime())
    
def main():
        
    every_books = []
    count = 0
    print(f"Starting time {get_time()}")
    total_pages, books_per_page = loadbaseurl(baseurl)

    if not isinstance(books_per_page,int):
        books_per_page = int(books_per_page)

    if total_pages > 0 and isinstance(total_pages,float):
        total_pages = int(total_pages)
        for i in range(1, total_pages + 1): # while making this code there were 50 pages 2025

            url = f"{main_page}{i}{extension}"

            print(f"Staring with page {url} - {get_time()}")  # Get the page content directly instead of writing to a file
           
            # Parse the content
            pq = get_pq(getSource(url))

            book_urls = []
            for book in pq('article.product_pod'):
                book = pq(book)

                url = book.find('h3 a').attr('href')
                if len(url):
                    book_urls.append(catalogue_pages + url)
                        
            for i, book in enumerate(book_urls):
                count += 1
                
                if i%3==0:

                    print(f"{get_time()} {i+1}. url:{book} -- {count}")
                every_books.append(book_detail(book))
            print(f"compelted time {get_time()}")
    else:
        print("Value no catch")
        print(type(total_pages))          

    books_list = pd.DataFrame(every_books)
    file = books_list.to_csv('books_new.csv')
    print(books_list)


if __name__ == "__main__":
    main()
 

# to do list 
# 1. clean Code 
# 2. change to file handling


