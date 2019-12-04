import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

all_quotes = []
base_url="http://quotes.toscrape.com"
url = "/page/1"

while url:         # While Schleife um die Quotes jeder Seite zu scrappen
    res = requests.get(f"{base_url}{url}") #
    print(f"Now Scraping {base_url}{url}....") #Statusüberprüfung
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
    #sleep(2)  #Um den Server nicht zu überlasten, da einige Seiten dagegen vorgehen.

quote = choice(all_quotes)
remaining_guesses = 4
print("Here's a quote: ")
print(quote["text"])
#print(quote["author"]) #Answer to the question
guess =""

while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
    guess = input(F"Who said this quote? Guesses remaining: {remaining_guesses}\n")
    if guess.lower() == quote['author'].lower():
        print("YOU WON. RIGHT ANSWER!")
        break
    remaining_guesses -= 1
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here's a hint. The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
        print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
    elif remaining_guesses == 1:
        last_initial = quote['author'].split(" ")[1][0]
        print(f"Here's a hint: The author's last name starts with: {last_initial}")
    else:
        print(f"Game over, too many wrong guesses. The answer was {quote['author']}")


