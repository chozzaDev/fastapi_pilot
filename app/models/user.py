from datetime import datetime
from typing import List

from fastapi_camelcase import CamelModel
from pydantic import Field
from pydantic.main import BaseModel


class UserLogin(CamelModel):
    phone_number: str = Field('01094766301', title='휴대전화번호', description='가입한 사용자의 휴대전화번호', max_length=20)
    passwd: str = Field('111111', title='비밀번호', max_length=100)
    login_type: str = Field('Local', title='로그인 유형', max_length=20)
    access_token: str = Field('', title='Firebase Fcm Token', max_length=255)
    device_name: str = Field('y2q', title='Mobile Device Name', max_length=100)
    device_model: str = Field('SM-G986N', title='Mobile Device Model', max_length=100)
    device_id: str = Field('264fd0328238a887', title='Mobile Device ID', max_length=100)
    os: str = Field('Android', title='Android or IOS', max_length=100)


class UserCreate(UserLogin):
    profile_img: str = Field('https://api.hatam.kr/static/upload/profileImg/408/t_f0cbf61079f0f31e5ae96605a9f93257.jpg',
                             title='Profile Image 경로', max_length=255)
    nick_name: str = Field('생계형개발자', title='Nick Name', max_length=10)
    marketing_receive: str = Field('Y', title='마케팅 활용동의', max_length=1)
    marketing_night_reject: str = Field('Y', title='마케팅 야간 알림 동의', max_length=1)
    third_party_agree: str = Field('Y', title='3자 정보제공 동의', max_length=1)
    email: str = Field('chozza@hatam.kr', title='이메일', max_length=100)


class UserToken(CamelModel):
    id: int
    email: str = None
    nick_name: str = None
    phone_number: str = None
    profile_img: str = None

    class Config:
        orm_mode = True


class User(UserCreate):
    id: int = Field(title='사용자 인덱스(PK)', description='Primary Key')
    phone_auth: str = Field(title='휴대전화인증여부', description='인증 완료 여부<br>왜있는지 잘 모르겠음...', max_length=1)
    cover_distance: int = None
    wdate: datetime = None
    last_pw_date: datetime = None
    last_login_date: datetime = None
    trade_point: int = None
    company_auth: str = None

    class Config:
        orm_mode = True


class UserCondition:
    phone_number: str = None


class Users(BaseModel):
    __root__: List[User]


class Token(BaseModel):
    Authorization: str = None
