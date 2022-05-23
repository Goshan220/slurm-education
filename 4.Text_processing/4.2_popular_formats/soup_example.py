from bs4 import BeautifulSoup
import requests


def main():
    html_doc = requests.get("https://httpbin.org").text

    soup = BeautifulSoup(html_doc, "html.parser")

    print(soup.prettify())

    print("*" * 30)

    print(soup.title.string)

    print("*" * 30)

    defs = soup.find("defs").children

    for child in defs:
        print(child)

    print("*" * 30)

    defs = soup.find("symbol")

    for syb in defs.next_siblings:
        print(syb)

    print("*" * 30)

    desc_block = soup.find("div", attrs={"class": "description"})

    print(desc_block)

    print("*" * 30)

    print(soup.get_text())



if __name__ == "__main__":
    main()

