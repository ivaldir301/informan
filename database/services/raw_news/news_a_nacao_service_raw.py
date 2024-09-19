from sqlalchemy.orm import Session
from database.utils.database_connection import get_db
from database.main import Base, SessionLocal, engine
from database.models.noticias_raw import noticias_a_nacao_raw 
from database.services.models.news import NoticiaANacao
from database.utils.news_to_db_model import news_to_a_nacao_model

noticias_a_nacao_raw.Base.metadata.create_all(bind=engine)


def get_raw_news_a_nacao(db: Session):
    noticias_a_nacao = db.query(noticias_a_nacao_raw.NoticiasANacaoRaw).filter().all()
    if noticias_a_nacao is None:
        print("table found empty")
    
    for noticia in noticias_a_nacao:
        print(f"ID: {noticia.id}, Title: {noticia.title}, Date: {noticia.release_date}")  

    return noticias_a_nacao

def get_raw_new_a_nacao(db: Session, new_id: str):
    a_nacao_new = db.query(noticias_a_nacao_raw.NoticiasANacaoRaw).filter(noticias_a_nacao_raw.NoticiasANacaoRaw.id == new_id).first()
    if a_nacao_new is None:
        print("no new found with that id")
        return False

    return a_nacao_new

def insert_new_a_nacao_news_raw(db: Session, new: NoticiaANacao):
    if new is None:
        print("noticia needs to be filled to be saved")

    db.add(new)
    db.commit()
    db.refresh(new)
    return new.id

def update_news_a_nacao_raw(db: Session, new: NoticiaANacao):
    if new is None:
        print("the new provided is invalid")

    existing_noticia_a_nacao = get_raw_new_a_nacao(db, new.id)
    if existing_noticia_a_nacao is False:
        return "noticia com este id no found"
    
    existing_noticia_a_nacao.title = new.title
    existing_noticia_a_nacao.type_of_news = new.type_news
    existing_noticia_a_nacao.release_date = new.release_date
    existing_noticia_a_nacao.news_body = new.news_body
    existing_noticia_a_nacao.origin_url = new.origin_url
    existing_noticia_a_nacao.scrappe_date = new.scrappe_date

    db.commit()
    db.refresh(existing_noticia_a_nacao)

    print("new was updated succesfully")


def delete_news_a_nacao_raw(db: Session, new_id: str):
    new = get_raw_new_a_nacao(db, new_id)
    db.delete(new)
    db.commit()
    print("new was deleted succesfully")


db_session = next(get_db())

# get_raw_news_a_nacao(db_session)

# print(get_raw_new_a_nacao(db_session, "1"))

# new_news = NoticiaANacao(
#     id = "2",
#     title = "Ivaldir esta programando DI NOVO(UPDATED)",
#     type_news = "Sociedade",
#     release_date = "2024-09-18",
#     news_body = "Ivaldir foi pego programando um projecto super interessante, esta semana, blablabla ... nova noticia",
#     origin_url = "governo.cv",
#     scrappe_date = "2024-09-18"
# )

# insert_new_a_nacao_news_raw(db_session, news_to_a_nacao_model(new_news))

# update_news_a_nacao_raw(db_session, new_news)

# delete_news_a_nacao_raw(db_session, "2")

# db_session.close()