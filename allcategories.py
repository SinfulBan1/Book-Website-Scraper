import requests
from bs4 import BeautifulSoup
import csv
from singlecategory import write_category_info
import os

csvFolderName = "csv_files"

def main():
    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)
    

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

    categories = soup.find("div", class_="side_categories").find("ul", class_="nav nav-list").find("ul").find_all("li")
    
    print("Starting all categories scraper")
    for category in categories:
        link = f"https://books.toscrape.com/{category.find("a").get("href")}"
        response = requests.get(link)

        csvName = f"{category.find("a").get_text(strip=True)}.csv"
        csvPath = os.path.join(csvFolderName, csvName)
        csvfile = open(csvPath, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvfile, delimiter=',')
        headers = ["product_page_url", "universal_product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
        writer.writerow(headers)

        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

        write_category_info(writer, soup, link)

        csvfile.close()
        
    print("Finished")




if __name__ == "__main__":
    main()