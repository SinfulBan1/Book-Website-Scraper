import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
import os
import re
from urllib.parse import urlparse

imgFolderName = "img_files"

def main():
    url = "https://books.toscrape.com"
    response = requests.get(url)
    


    csvfile = open('data.csv', 'w', newline='', encoding='utf-8')
    headers = ["product_page_url", "universal_product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)

    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all("article", class_="product_pod")
    write_article_info(writer, articles[0], soup)


    csvfile.close()

def write_article_info(writer, article, soup):

    def make_safe_filename(title):
        safe_title = re.sub(r'[<>:"/\\|?*]+', '', title)
        safe_title = re.sub(r'\s+', ' ', safe_title).strip()
        return safe_title

    # get info
    root_url = "https://books.toscrape.com/catalogue/"
    book_url_extension = article.find("div", class_="image_container").find("a").get("href").split("../")[-1]
    book_url = root_url + book_url_extension
    # print(url)
    image_url_extension = article.find("div", class_="image_container").find("a").find("img").get("src").split("../")[-1]
    image_url = "https://books.toscrape.com/" + image_url_extension
    # print(image_url)
    rating_classes = article.find("p", class_="star-rating").get("class")
    rating = rating_classes[1]
    # print(rating)
    title = article.find("h3").find("a").get("title")
    # print(title)

    response = requests.get(book_url)
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

    product_page = soup.find("article", class_="product_page")
    quantityavailable = product_page.find("div", class_="row").find("div", "product_main").find("p", class_="instock availability").get_text(strip=True)
    # print(quantityavailable)

    links = soup.find("ul", class_="breadcrumb").find_all("li")
    category = links[2].get_text(strip=True)
    # print(category)

    paragraphs = product_page.find_all("p")
    description = paragraphs[3].get_text(strip=True)
    # print(description)

    table_entries = product_page.find("table").find_all("tr")
    upc = table_entries[0].find("td").get_text(strip=True)
    # print(upc)
    pricenontaxed = table_entries[2].find("td").get_text(strip=True)
    # print(pricenontaxed)
    pricetaxed = table_entries[3].find("td").get_text(strip=True)
    # print(pricetaxed)

    # downloads and writes the image
    image_filename = f"{make_safe_filename(title)}.jpg"
    image_path = os.path.join(imgFolderName, image_filename)
    try:
        urllib.request.urlretrieve(image_url, image_path)
    except Exception as e:
        print(f"Error downloading and saving image: {e}")

    # write info to row
    row = [book_url, upc, title, pricetaxed, pricenontaxed, quantityavailable, description, category, rating, image_url]
    writer.writerow(row)


    


if __name__ == "__main__":
    main()