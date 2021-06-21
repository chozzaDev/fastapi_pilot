import asyncio
import os
from os import path
from typing import List

import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.schema import User
from app.main import create_app
from app.database.conn import db, Base
from app.models.user import UserToken
from app.routes.auth import create_access_token

"""
1. DB 생성
2. 테이블 생성
3. 테스트 코드 작동
4. 테이블 레코드 삭제 
"""


@pytest.fixture(scope="session")
def app():
    os.environ["API_ENV"] = "test"
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    # Create tables
    Base.metadata.create_all(db.engine)
    return TestClient(app=app)


@pytest.fixture(scope="function", autouse=True)
def session():
    sess = next(db.session())
    yield sess
    clear_all_table_data(
        session=sess,
        metadata=Base.metadata,
        except_tables=[]
    )
    sess.rollback()


@pytest.fixture(scope="function")
def login(session):
    """
    테스트전 사용자 미리 등록
    :param session:
    :return:
    """
    db_user = User.create(session=session,
                          phone_number="01094766301",
                          passwd=bcrypt.hashpw('111111'.encode("utf-8"), bcrypt.gensalt()),
                          login_type="Local",
                          access_token="",
                          device_name="y2q",
                          device_model="SM-G986N",
                          device_id="264fd0328238a887",
                          os="Android",
                          profile_img="https://api.hatam.kr/static/upload/profileImg/408"
                                     "/t_f0cbf61079f0f31e5ae96605a9f93257.jpg",
                          nick_name="생계형개발자",
                          marketing_receive="Y",
                          marketing_night_reject="Y",
                          third_party_agree="Y",
                          email="chozza@hatam.kr", company_auth='N')
    session.commit()
    access_token = create_access_token(data=UserToken.from_orm(db_user).dict(exclude={'passwd', 'marketing_agree'}), )
    return dict(Authorization=f"Bearer {access_token}")


def clear_all_table_data(session: Session, metadata, except_tables: List[str] = None):
    session.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table in metadata.sorted_tables:
        if table.name not in except_tables:
            session.execute(table.delete())
    session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()
