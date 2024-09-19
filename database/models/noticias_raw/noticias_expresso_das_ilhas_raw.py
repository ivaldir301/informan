from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.main import Base

class NoticiasExpressoDasIlhasRaw(Base):
    __tablename__ = "noticias_expresso_das_ilhas_raw"
    id = Column(Integer, primary_key=True, index=True)
    type_of_news = Column(String)
    title = Column(String)
    release_date = Column(DateTime, default=datetime.now)
    news_body = Column(String)
    origin_url = Column(String)
    scrappe_date = Column(DateTime, default=datetime.now)
