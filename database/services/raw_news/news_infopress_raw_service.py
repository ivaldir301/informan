from sqlalchemy.orm import Session
from database.utils.database_connection import get_db
from database.main import Base, SessionLocal, engine
from database.models.noticias_raw import noticias_infopress_raw 
from database.models.noticias_raw import noticias_expresso_das_ilhas_raw 
from database.services.models.news import NoticiaANacao, NoticiaExpressoDasIlhas, NoticiaInfopress
from database.utils.news_to_db_model import news_to_infopress_model

noticias_infopress_raw.Base.metadata.create_all(bind=engine)
noticias_expresso_das_ilhas_raw.Base.metadata.create_all(bind=engine)

def get_raw_news_infopress(db: Session):
    noticias_infopress = db.query(noticias_infopress_raw.NoticiasInfoPressRaw).filter().all()
    if noticias_infopress is None:
        print("table found empty")
    
    for noticia in noticias_infopress:
        print(f"ID: {noticia.id}, Title: {noticia.title}, Date: {noticia.release_date}")  

    return noticias_infopress

def get_raw_new_infopress(db: Session, new_id: str):
    infopress_new = db.query(noticias_infopress_raw.NoticiasInfoPressRaw).filter(noticias_infopress_raw.NoticiasInfoPressRaw.id == new_id).first()
    if infopress_new is None:
        print("no new found with that id")
        return False

    return infopress_new

def insert_new_infopress_news_raw(db: Session, new: NoticiaInfopress):
    if new is None:
        print("noticia needs to be filled to be saved")

    db.add(new)
    db.commit()

def update_news_infopress_raw(db: Session, new: NoticiaInfopress):
    if new is None:
        print("the new provided is invalid")

    existing_noticia_infopress = get_raw_new_infopress(db, new.id)
    if existing_noticia_infopress is False:
        return "noticia com este id no found"
    
    existing_noticia_infopress.title = new.title
    existing_noticia_infopress.type_of_news = new.type_news
    existing_noticia_infopress.release_date = new.release_date
    existing_noticia_infopress.news_body = new.news_body
    existing_noticia_infopress.origin_url = new.origin_url
    existing_noticia_infopress.scrappe_date = new.scrappe_date

    db.commit()
    db.refresh(existing_noticia_infopress)

    print("new was updated succesfully")


def delete_news_infopress_raw(db: Session, new_id: str):
    new = get_raw_new_infopress(db, new_id)
    db.delete(new)
    db.commit()
    print("new was deleted succesfully")

db_session = next(get_db())

# get_raw_news_infopress(db_session)

# print(get_raw_new_infopress(db_session, "1"))

# new_news = NoticiaInfopress(
#     id = "2",
#     title = "Ivaldir esta programando DI NOVO",
#     type_news = "Sociedade",
#     release_date = "2024-09-18",
#     news_body = "Ivaldir foi pego programando um projecto super interessante, esta semana, blablabla ... nova noticia",
#     origin_url = "governo.cv",
#     scrappe_date = "2024-09-18"
# )

# insert_new_infopress_news_raw(db_session, news_to_infopress_model(new_news))

# update_news_infopress_raw(db_session, new_news)

# delete_news_infopress_raw(db_session, "1 ")

db_session.close()