from sqlalchemy.orm import Session
from database.utils.database_connection import get_db
from database.main import Base, SessionLocal, engine
from database.models.noticias_raw import noticias_expresso_das_ilhas_raw 
from database.services.models.news import NoticiaExpressoDasIlhas
from database.utils.news_to_db_model import news_to_expresso_das_ilhas_model

noticias_expresso_das_ilhas_raw.Base.metadata.create_all(bind=engine)

def get_raw_news_expresso_das_ilhas(db: Session):
    noticias_expresso_das_ilhas = db.query(noticias_expresso_das_ilhas_raw.NoticiasExpressoDasIlhasRaw).filter().all()
    if noticias_expresso_das_ilhas is None:
        print("table found empty")
    
    for noticia in noticias_expresso_das_ilhas:
        print(f"ID: {noticia.id}, Title: {noticia.title}, Date: {noticia.release_date}")  

    return noticias_expresso_das_ilhas

def get_raw_new_expresso_das_ilhas(db: Session, new_id: str):
    new = db.query(noticias_expresso_das_ilhas_raw.NoticiasExpressoDasIlhasRaw).filter(noticias_expresso_das_ilhas_raw.NoticiasExpressoDasIlhasRaw.id == new_id).first()
    if new is None:
        print("no new found with that id")
        return False

    return new

def insert_new_expresso_das_ilhas_raw(db: Session, new: NoticiaExpressoDasIlhas):
    if new is None:
        print("noticia needs to be filled to be saved")

    db.add(new)
    db.commit()
    db.refresh(new)
    return new.id

def update_news_expresso_das_ilhas(db: Session, new: NoticiaExpressoDasIlhas):
    if new is None:
        print("the new provided is invalid")

    existing_noticia_expresso_das_ilhas = get_raw_new_expresso_das_ilhas(db, new.id)
    if existing_noticia_expresso_das_ilhas is False:
        return "noticia com este id no found"
    
    existing_noticia_expresso_das_ilhas.title = new.title
    existing_noticia_expresso_das_ilhas.type_of_news = new.type_news
    existing_noticia_expresso_das_ilhas.release_date = new.release_date
    existing_noticia_expresso_das_ilhas.news_body = new.news_body
    existing_noticia_expresso_das_ilhas.origin_url = new.origin_url
    existing_noticia_expresso_das_ilhas.scrappe_date = new.scrappe_date

    db.commit()
    db.refresh(existing_noticia_expresso_das_ilhas)

    print("new was updated succesfully")


def delete_news_a_nacao_raw(db: Session, new_id: str):
    new = get_raw_new_expresso_das_ilhas(db, new_id)
    db.delete(new)
    db.commit()
    print("new was deleted succesfully")


db_session = next(get_db())

# get_raw_news_a_nacao(db_session)

# print(get_raw_new_a_nacao(db_session, "1"))

# new_news = NoticiaExpressoDasIlhas(
#     id = "1",
#     title = "Ivaldir esta programando DI NOVO hoje 18 setembro",
#     type_news = "Sociedade",
#     release_date = "2024-09-18",
#     news_body = "Ivaldir foi pego programando um projecto super interessante, esta semana, blablabla ... nova noticia",
#     origin_url = "governo.cv",
#     scrappe_date = "2024-09-18"
# )

# insert_new_expresso_das_ilhas_raw(db_session, news_to_expresso_das_ilhas_model(new_news))

# update_news_expresso_das_ilhas(db_session, new_news)

# delete_news_a_nacao_raw(db_session, "2")

# db_session.close()