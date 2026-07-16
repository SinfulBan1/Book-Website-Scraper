import requests
from bs4 import BeautifulSoup
import csv
from singleproduct import write_article_info

def main():
    url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    response = requests.get(url)
    
    csvfile = open('data.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile, delimiter=',')
    headers = ["product_page_url", "universal_product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
    writer.writerow(headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    write_category_info(writer, soup, url)

    csvfile.close()


# write the info from a category given an initialized writer and soup that has been opened to the correct url
def write_page_info(writer, soup):
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        write_article_info(writer, article, soup)

# handles pagination and calls write_page_info
def write_category_info(writer, soup, url):
    nextPage = soup.find(class_="next")
    while (nextPage):
        write_page_info(writer, soup)
        base = url.rsplit("/", 1)[0]
        pageExtension = nextPage.find("a").get("href")
        newUrl = f"{base}/{pageExtension}"
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
        nextPage = soup.find(class_="next")
        
    write_page_info(writer, soup)


if __name__ == "__main__":
    main()