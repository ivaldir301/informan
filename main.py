from scrappers.inforpress_scrapper import InforpresScrapper
from scrappers.expresso_das_ilhas_scrapper import first_request
import asyncio

Inforpress = InforpresScrapper()

asyncio.run(Inforpress.run_scrapper())
asyncio.run(first_request())