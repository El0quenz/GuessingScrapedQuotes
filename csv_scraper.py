import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter


BASE_URL="http://quotes.toscrape.com" #Konstante



def scrape_quotes():
    url = "/page/1"
    all_quotes = []
    while url:         # While Schleife um die Quotes jeder Seite zu scrappen
        res = requests.get(f"{BASE_URL}{url}") #
        print(f"Now Scraping {BASE_URL}{url}....") #Statusüberprüfung
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")    #Finde "quote" Klassen Elemente

    # For Loop die alle Elemente der Klasse "text" durchgeht und .getText() um nur den
    # Text auszugeben, ansonsten würde man die <span> sehen.
        for quote in quotes:
           all_quotes.append({
                "text":quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
                                    # Bis es nicht mehr "weiter" geht.
    sleep(1)  #Um den Server nicht zu überlasten, da einige Seiten dagegen vorgehen.
    return all_quotes


#write quotes to csv file
def write_quotes(quotes):
    with open("quotes.csv", "w") as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)
quotes = scrape_quotes()
write_quotes(quotes)