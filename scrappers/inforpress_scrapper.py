import os
import httpx
import time
from selectolax.parser import HTMLParser
import asyncio
from httpx import HTTPStatusError, RequestError
from dotenv import load_dotenv
import datetime
import json
from scrappers.models.inforpress import InforpressScrappedData
from scrappers.utils.utils import get_page_data
load_dotenv()

class InforpresScrapper():
    def __init__(self):
        self.base_url = os.getenv("INFORRPRESS_BASE_URL")
        self.news_tags = ["politics", "economy", "society", "culture", "sports", "nature", "cooperation", "international"]
        self.tag = ""
        self.current_url = "" 
        self.current_page = 1
        self.scrapping_start_time = 0
        self.scrapping_end_time = 0
        self.scrapped_news = []


    # async def get_page_data(self, url, retries=5, backoff_factor=1.0, timeout=10.0):
    #     """
    #     Fetch a URL with retries and exponential backoff.

    #     Args:
    #         url (str): The URL to fetch.
    #         retries (int): Number of retries before giving up.
    #         backoff_factor (float): Factor by which the wait time increases after each retry.
    #         timeout (float): Timeout for the request in seconds.

    #     Returns:
    #         str: The HTML content of the page if successful.

    #     Raises:
    #         Exception: If all retries fail.
    #     """

    #     for attempt in range(retries):
    #         try:
    #             async with httpx.AsyncClient(timeout=timeout) as client:
    #                 response = await client.get(url)
    #                 response.raise_for_status()  
    #                 return response.content
    #         except (HTTPStatusError, RequestError) as e:
    #             print(f"Attempt {attempt + 1}/{retries} failed: {e}")
    #             if attempt < retries - 1:
    #                 sleep_time = backoff_factor * (8 ** attempt)
    #                 print(f"Retrying in {sleep_time:.2f} seconds...")
    #                 await asyncio.sleep(sleep_time)
    #             else:
    #                 print("Max retries reached. Failing...")
    #                 raise

    def generate_url_pagination(self):
        return os.getenv("INFORRPRESS_BASE_URL") + "/tags/" + self.tag + "?page=" + str(self.current_page)

    def reset_config_variables(self):
        self.current_page = 1

    def check_page_pagination_end(self, parsed_data):
        div = parsed_data.css_first("body > div > div > .grid")
        print(f"\n\n the div variable: {div.text()} \n")
        if div.text() is "":
            print("\n\n pagination end reached. \n\n")
            return True
        return div

    def get_news_page_links_from_container(self, container):
        news_links = []
        if container:
            print("\n\nCards container found.\n")
            
            for card in container.css("a"):  
                link = card.css_first("a")
                news_links.append(link.attributes['href'])
            return news_links
        else:
            print("No cards container found.")

    async def get_news_model_from_links(self, news_links):
        for link in news_links:
            start = time.time()
            time.sleep(2)
            new_url = os.getenv("INFORRPRESS_BASE_URL") + "/" + link
            print(new_url)
            new_page = await get_page_data(new_url)
            parsed_page = HTMLParser(new_page)

            page_title = parsed_page.css_first("h1.text-black")
            news_image_container = parsed_page.css_first("img.rounded-sm")
            image_link = news_image_container.attributes['src']
            news_publication_time = parsed_page.css_first("body > div > div > div > div > div > div > span")
            news_body_text = parsed_page.css_first("div.news-body")

            end = time.time()
            elapsed_time = end - start

            news_obj = InforpressScrappedData(
                scrapping_date=str(datetime.datetime.now()),
                scrappe_duration=str(elapsed_time),
                news_category=self.tag,
                news_title=page_title.text(),
                news_body_text=news_body_text.text(),
                news_publising_date=news_publication_time.text(),
                news_image_link=image_link
            )

            f = open("json_result.json", "a")
            dict_data = news_obj.dict()
            f.write(json.dumps(dict_data, indent=4))
            f.close()   

            self.scrapped_news.append(news_obj)
            print("\n\n news publish date: ", news_publication_time.text())
            print("\n\n", news_obj)
            print("\n", news_obj.news_title)   

    def save_data(self):
        pass

    async def run_scrapper(self):
        start = time.time()
        for tag in self.news_tags:
            self.tag = tag
            while True:
                start = time.time()
                time.sleep(1)
                new_page_link = self.generate_url_pagination()
                page_response = await get_page_data(new_page_link)
                print(f"\n\n GOING TO NEW LINK: {new_page_link} \n\n")
                print(f"\nTHE DATATYPE OF PAGEDATA: {type(new_page_link)}\n")
                parser = HTMLParser(page_response)

                container = self.check_page_pagination_end(parser)
                if container is True:
                    break

                news_links = self.get_news_page_links_from_container(container)
                print(f"\n\n the links: {news_links}")
                await self.get_news_model_from_links(news_links)
                self.current_page+=1
            self.reset_config_variables()

        end = time.time()
        elapsed = end - start

        print(f"\n\nthe entire operation lasted: {elapsed / 60}\n\n")
