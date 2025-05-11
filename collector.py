from pyquery import PyQuery
import requests
import pandas as pd

main = "https://books.toscrape.com/catalogue/page-"
extension = ".html"

all_books = []

for i in range(1, 51):
    url = f"{main}{i}{extension}"
    
    def getSource(url):
        response = requests.get(url)
        return response.text
    
    def readSource(content):
        return content.splitlines()
    
    if __name__ == "__main__": #dunder
        # Get the page content directly instead of writing to a file
        source = getSource(url)
        
        # Parse the content
        pq = PyQuery(source)
        title = pq('title').text()
        print(f"Processing page {i}: {title}")
        
        books = []
        
        for j in range(20):
            name = pq('article.product_pod h3 a').eq(j).attr('title')
            price = pq('article.product_pod div p.price_color').eq(j).text()
            if price:
                price = price.split('Â')[-1]
            rating = pq('article.product_pod p.star-rating ').eq(j).attr('class')
            if rating:
                rating = rating.split()[-1] #if len(rating.split()) > 1 else rating
            stock = pq('article.product_pod div p.availability').eq(j).text()
                
            books.append({
                'name': name,
                'price': price,
                'rating': rating,
                'stock': stock
            })
        
        all_books.extend(books)
        
        # Print books from this page
        books_list = pd.DataFrame(books)
        print(f"Books from page {i}:")
        print(books_list)
all_books_df = pd.DataFrame(all_books)
print(f"\nTotal books collected: {len(all_books)}")
print(all_books_df.head())