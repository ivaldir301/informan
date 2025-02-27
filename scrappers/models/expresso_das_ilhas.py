from pydantic import BaseModel
from typing import Optional

class ExpressoDasIlhasScrappedData(BaseModel):
    news_title: str
    link: str
    thumbnail: str
    publication_date: str
    section: str
    news_body: str