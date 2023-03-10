from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/educational_forms', tags=['Educational_forms'])


# ==================== routers =======================
@router.post('/', response_model=api_models.EducationalForms)
async def create(educational_form: api_models.EducationalForms) -> api_models.EducationalForms:
    return await create_educational_form(educational_form)


@router.get('/', response_model=List[api_models.EducationalForms])
async def get_all() -> List[api_models.EducationalForms]:
    return await get_educational_forms()


@router.get('/{record_id}', response_model=api_models.EducationalForms)
async def get_by_id(record_id: int) -> api_models.EducationalForms:
    return await get_educational_form_by_id(record_id)


# ==================== resolvers =======================
async def create_educational_form(educational_form: api_models.EducationalForms) -> api_models.EducationalForms:
    print(educational_form)
    ed_form = sql_models.EducationalForms(**educational_form.to_filter_dict())
    async with get_session() as session:
        session.add(ed_form)
        await session.commit()
        return api_models.EducationalForms(**ed_form.to_filter_dict())


async def get_educational_forms() -> List[api_models.EducationalForms]:
    stmt = select(sql_models.EducationalForms)
    async with get_session() as session:
        educational_forms_source = (await session.execute(stmt)).scalars().all()
        educational_forms = [api_models.EducationalForms(**form.to_filter_dict())
                             for form in educational_forms_source]
        return educational_forms


async def get_educational_form_by_id(record_id: int) -> api_models.EducationalForms:
    async with get_session() as session:
        ed_form = await session.get(sql_models.EducationalForms, record_id)
        if ed_form:
            return api_models.EducationalForms(**ed_form.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
