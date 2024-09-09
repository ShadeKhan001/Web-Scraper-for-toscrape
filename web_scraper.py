import requests

from bs4 import BeautifulSoup

import pandas as pd

books = []

for i in range(1,51):
    url = f"http://books.toscrape.com/catalogue/page-{i}.html"
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, "html.parser")
    ol = soup.find("ol")
    articles = ol.find_all("article", class_="product_pod")

    for article in articles:
        imgs = article.find("img")
        titles = imgs.attrs["alt"]
        ti = titles.replace(":", "")
        star = article.find("p")["class"][1]
        price = article.find("p", class_="price_color").text
        price = float(price[1:])
        src = article.div.a.img["src"]
        stripped = src.strip("../")
        img = "https://books.toscrape.com/{}".format(stripped)
        flag = requests.get(img)
        filename = img.split("/")[-1]
        if flag.status_code != 200:
            print("Error Geting {}".format(filename))
        else:
            with open(f"pic/{filename}", "wb") as f:
                noop = f.write(flag.content)
                print(f"Save {titles}.jpg")

        books.append([img,titles, star, price])

    df = pd.DataFrame(books, columns=["Image link", "Titles", "Star", "Price"])
    df.to_csv("Books.csv")