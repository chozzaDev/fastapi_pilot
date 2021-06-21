from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.database.conn import db
from app.database.schema import User
from app.models.user import UserCreate, UserLogin, UserToken, Token

"""

400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method not allowed
500 Internal Error
502 Bad Gateway 
504 Timeout
200 OK
201 Created

"""

router = APIRouter(prefix="/v1/auth")


#
@router.put("/create", status_code=201, response_model=Token)
async def create(user: UserCreate, session: Session = Depends(db.session)):
    """
    `회원가입 API`\n
    :param user:
    :param session:
    :return:
    """
    response = has_user_response(user)
    if response:
        return response
    hash_pw = bcrypt.hashpw(user.passwd.encode("utf-8"), bcrypt.gensalt())

    new_user = User.create(session=session, auto_commit=True, phone_number=user.phone_number,
                           login_type=user.login_type, profile_img=user.profile_img, nick_name=user.nick_name,
                           passwd=hash_pw, email=user.email, marketing_receive=user.marketing_receive,
                           marketing_night_reject=user.marketing_night_reject, third_party_agree=user.third_party_agree,
                           device_id=user.device_id, device_name=user.device_name, device_model=user.device_model,
                           company_auth='N')
    return dict(
        Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'passwd'}), )}")


@router.post("/login", status_code=200, response_model=Token)
async def login(login_user: UserLogin):
    users = User.filter(phone_number=login_user.phone_number).all()
    if not users:
        return JSONResponse(status_code=400, content=dict(msg="User not found."))
    user = users[0]
    is_verified = bcrypt.checkpw(login_user.passwd.encode("utf-8"), user.passwd.encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
    token = dict(
        Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'passwd'}), )}")
    return token


def has_user_response(user: UserCreate):
    users = User.filter(phone_number=user.phone_number).all()
    if users:
        return JSONResponse(status_code=400, content=dict(msg="User already exists."))
    return


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
