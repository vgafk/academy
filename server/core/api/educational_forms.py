from typing import List, Dict

from fastapi import APIRouter

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select, insert

router = APIRouter(prefix='/educational_forms', tags=['Educational_forms'])


# ==================== routers =======================
@router.post('/')
async def create(educational_form: api_models.EducationalForms) -> Dict[str, str]:
    return await create_educational_form(educational_form)


@router.get('/', response_model=List[api_models.EducationalForms] | Dict[str, str])
async def get_all() -> List[api_models.EducationalForms]:
    return await get_educational_forms()


@router.get('/{record_id}', response_model=api_models.EducationalForms | Dict[str, str])
async def get_by_id(record_id: int) -> api_models.EducationalForms | Dict[str, str]:
    return await get_educational_form_by_id(record_id)


# ==================== resolvers =======================
async def create_educational_form(educational_form: api_models.EducationalForms) -> Dict[str, str]:
    stmt = insert(sql_models.EducationalForms).values(name=educational_form.name)
    async with get_session() as session:
        result = (await session.execute(stmt))
        await session.commit()

    return {'code': '200', 'inserted_id': result.inserted_primary_key[0]}


async def get_educational_forms() -> List[api_models.EducationalForms] | Dict[str, str]:
    stmt = select(sql_models.EducationalForms)
    async with get_session() as session:
        result = (await session.execute(stmt)).all()
        if len(result) > 0:
            educational_forms = [api_models.EducationalForms(id=form.id, name=form.name) for form in result[0]]
            return educational_forms
        else:
            return {'code': "404", "text": f"На данный момент в базе не создано ни одной формы обучения"}


async def get_educational_form_by_id(record_id: int) -> api_models.EducationalForms | Dict[str, str]:
    stmt = select(sql_models.EducationalForms).where(sql_models.EducationalForms.id == record_id)
    async with get_session() as session:
        result = (await session.execute(stmt)).first()
        if result:
            return api_models.EducationalForms(id=result[0].id, name=result[0].name)
        else:
            return {'code': "404", "text": f"Формы обучения с идентификатором {record_id} в базе не существует"}
