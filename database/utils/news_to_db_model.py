from database.models.noticias_raw.noticias_infopress_raw import NoticiasInfoPressRaw
from database.models.noticias_raw.noticias_a_nacao_raw import NoticiasANacaoRaw
from database.models.noticias_raw.noticias_expresso_das_ilhas_raw import NoticiasExpressoDasIlhasRaw
from database.services.models.news import NoticiaInfopress, NoticiaANacao, NoticiaExpressoDasIlhas

def news_to_infopress_model(pydantic_model: NoticiaInfopress) -> NoticiasInfoPressRaw:
    new = NoticiasInfoPressRaw(
        id=pydantic_model.id,
        type_of_news=pydantic_model.type_news,
        title=pydantic_model.title,
        release_date=pydantic_model.release_date,
        news_body=pydantic_model.news_body,
        origin_url=pydantic_model.origin_url,
        scrappe_date=pydantic_model.scrappe_date
    )
    return new


def news_to_a_nacao_model(pydantic_model: NoticiaANacao) -> NoticiasANacaoRaw:
    new = NoticiasANacaoRaw(
        id=pydantic_model.id,
        type_of_news=pydantic_model.type_news,
        title=pydantic_model.title,
        release_date=pydantic_model.release_date,
        news_body=pydantic_model.news_body,
        origin_url=pydantic_model.origin_url,
        scrappe_date=pydantic_model.scrappe_date
    )
    return new

def news_to_expresso_das_ilhas_model(pydantic_model: NoticiaExpressoDasIlhas) -> NoticiasExpressoDasIlhasRaw:
    new = NoticiasExpressoDasIlhasRaw(
        id=pydantic_model.id,
        type_of_news=pydantic_model.type_news,
        title=pydantic_model.title,
        release_date=pydantic_model.release_date,
        news_body=pydantic_model.news_body,
        origin_url=pydantic_model.origin_url,
        scrappe_date=pydantic_model.scrappe_date
    )
    return new