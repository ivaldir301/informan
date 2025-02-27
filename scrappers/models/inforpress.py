from pydantic import BaseModel
from typing import Optional

class InforpressScrappedData(BaseModel):
    scrapping_date: str
    scrappe_duration: str
    news_category: Optional[str] = None
    news_title: Optional[str] = None
    news_body_text: Optional[str] = None
    news_publising_date: Optional[str] = None
    news_image_link: Optional[str] = None
