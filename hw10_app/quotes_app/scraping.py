
import requests
from bs4 import BeautifulSoup
from lxml import etree

base_url = "https://quotes.toscrape.com"


# http://quotes.toscrape.com/page/2/

def make_scraping():
    quotes = []
    authors = []
    authors_references_used = []

    page_count = 9

    while True:

        authors_references = []
        page_count += 1

        print(f"Page count: {page_count}")
        temp_url = f"{base_url}/page/{page_count}/"

        response = requests.get(temp_url)

        print(f"temp_url: {temp_url}")
        print(f"response.status_code: {response.status_code}")

        if response.status_code != 200:
            break
        else:
            soup = BeautifulSoup(response.text, "lxml")

            tree = etree.HTML(str(soup))

            quote_divs = tree.xpath("//div[@class='quote']")

            if not quote_divs:
                break

            for div in quote_divs:
                # print("---------------------------------------------------------------------")
                # Tags
                tag_list = []
                tags_elements = div.xpath(".//div[@class='tags']/a")

                for tags in tags_elements:
                    tag_list.append(tags.text)

                # Author
                span_elements = div.xpath(".//span/small")
                if span_elements:
                    author = str(span_elements[0].text).strip()

                # Author ref
                span_elements = div.xpath(".//span/a/@href")
                if span_elements:
                    # print(span_elements[0].text)
                    # author = str(span_elements).strip()
                    author_ref = str(span_elements[0]).strip()

                    if not (author_ref in authors_references_used):
                        authors_references_used.append(author_ref)
                        if not (author_ref in authors_references):
                            authors_references.append(author_ref)

                # Quot
                span_elements = div.xpath(".//span[@class='text']")

                if span_elements:
                    quote = span_elements[0].text

                quotes.append({"tags": tag_list, "author": author, "quote": quote})

            # Get authors info
            for author_ref in authors_references:
                url_author = f"{base_url}{author_ref}"
                # print(url_author)
                response = requests.get(url_author)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "lxml")

                    tree = etree.HTML(str(soup))

                    quote_divs = tree.xpath("//div[@class='author-details']")

                    for div in quote_divs:
                        # print("---------------------------------------------------------------------")
                        name_tags = div.xpath(".//h3")
                        if name_tags:
                            fullname = name_tags[0].text

                        born_date_tags = div.xpath(".//span[@class ='author-born-date']")
                        if born_date_tags:
                            born_date = born_date_tags[0].text

                        born_location_tags = div.xpath(".//span[@class ='author-born-location']")
                        if born_location_tags:
                            born_location = born_location_tags[0].text

                        author_description_tags = div.xpath(".//div[@class ='author-description']")
                        if author_description_tags:
                            author_description = str(author_description_tags[0].text).strip()

                        authors.append({
                            "fullname": fullname,
                            "born_date": born_date,
                            "born_location": born_location,
                            "description": author_description
                        })

    return {"authors": authors, "quotes": quotes}


if __name__ == "__main__":
    make_scraping()
