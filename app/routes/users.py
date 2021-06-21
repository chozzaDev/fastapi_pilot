from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import User
from app.models.user import Users

router = APIRouter(prefix='/v1/users')


@router.get('/', response_model=Users)
async def read_users(phone_number: Optional[str] = '', offset: int = 0, limit: int = 10,
                     session: Session = Depends(db.session)):
    query = session.query(User).offset(offset).limit(limit)
    if phone_number:
        query.filter(phone_number=phone_number)
    return query.all()
