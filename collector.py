from pyquery import PyQuery
import requests
import pandas as pd

main = "https://books.toscrape.com/catalogue/page-"
pages = "https://books.toscrape.com/catalogue/"
extension = ".html"

all_books = []

def getSource(url):
    response = requests.get(url)
    return response.text
    
def readSource(content):
    return content.splitlines()

if __name__ == "__main__":

    every_books = []

    for i in range(1,51): # while making this code there were 50 pages 2025
        url = f"{main}{i}{extension}"
      
        # Get the page content directly instead of writing to a file
        source = getSource(url)
        
        # Parse the content
        pq = PyQuery(source)
        print(f"Books from page {i}:")

        for j in range(1,21):
            page_url=pq('article.product_pod .image_container a').eq(j).attr('href')
            if page_url:
                price = ""
                page_source = getSource(pages + page_url)
                pq_page = PyQuery(page_source)


                name = pq_page('article.product_page h1').text()
                price = pq_page('article.product_page p.price_color').eq(0).text()
                if price:
                    price = price.replace('Â','').strip() 
                rating = pq_page('article.product_page p.star-rating ').attr('class')
                if rating:
                    rating = rating.split()[-1] #if len(rating.split()) > 1 else rating
                stock = pq_page('article.product_page p.availability').eq(0).text()
                if stock:
                    in_stock = stock.split('(')[0]
                    qty = stock.split("(")[1].split(" ")[0]
                category = pq_page("ul.breadcrumb li").eq(2).text()
            
                    
                every_books.append({
                    'url': pages + page_url,
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'stock': in_stock.strip(),
                    'quantity': qty.strip(),
                    'category': category
                })
            
        
    # print(every_books)
    # Print books from this page
    books_list = pd.DataFrame(every_books)
    file = books_list.to_csv('books.csv')
    print(books_list)

# all_books_df = pd.DataFrame(all_books)
# print("---"*20)
# print(f"\nTotal books collected: {len(all_books)}")
# print(all_books_df.head())


to_list 
1. total number of products verify
2. code clean
3. write steps 
4. include time, random seconds
5. 