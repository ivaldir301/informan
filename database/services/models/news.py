from pydantic import BaseModel

class NoticiaInfopress(BaseModel):
    id: str
    type_news: str
    title: str
    release_date: str
    news_body: str
    origin_url: str
    scrappe_date: str

class NoticiaANacao(BaseModel):
    id: str
    type_news: str
    title: str
    release_date: str
    news_body: str
    origin_url: str
    scrappe_date: str

class NoticiaExpressoDasIlhas(BaseModel):
    id: str
    type_news: str
    title: str
    release_date: str
    news_body: str
    origin_url: str
    scrappe_date: str

