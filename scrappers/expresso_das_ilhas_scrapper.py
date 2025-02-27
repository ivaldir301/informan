import asyncio
import os
from dotenv import load_dotenv
import httpx
from scrappers.utils.utils import get_page_data
from selectolax.parser import HTMLParser
from scrappers.models.expresso_das_ilhas import ExpressoDasIlhasScrappedData

load_dotenv()

async def get_news_specifics(link: str):
	url: str = link

	print(f"the url: {url}")
	page_response = await get_page_data(url)
	tree = HTMLParser(page_response.decode("utf-8"))
	article_text = tree.css_first(".articleText")
	return article_text.text() 

async def list_of_news_models(json_response):
	news_list = []
	for new in json_response:
		new_model = ExpressoDasIlhasScrappedData(
			news_title = new["title"],
			link = new["url"],
			thumbnail = new["thumbnail"],
			publication_date = new["cvdate"],
			section = new["section"],
			news_body = await get_news_specifics(new["url"])
		)
		news_list.append(new_model)
	return news_list


async def first_request():
	url = os.getenv("EXPRESSO_DAS_ILHAS_API_BASE_URL")
	headers = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate, br, zstd",
		"Accept-Language": "pt-CV,pt;q=0.9,en-GB;q=0.8,en;q=0.7,pt-PT;q=0.6,en-US;q=0.5",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Origin": "https://expressodasilhas.cv",
		"Referer": "https://expressodasilhas.cv/politica",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest",
	}

	# Define the payload form data
	payload = {
		"user": "nobody",
		"path": "/politica",
		"section": "politica",
		"lastTime": "1737054619",
		"referrer": "https://expressodasilhas.cv/conteudo-patrocinado",
	}

	# Make the POST request to the API
	response = httpx.post(url, headers=headers, data=payload)

	collected_news = []
	# Check if the request was successful
	if response.status_code == 200:	
		news_data = response.json()
		collected_news = await list_of_news_models(news_data["latest"])
	else:
		print(f"Error: {response.status_code}, {response.text}")

	print(collected_news)