from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean, func,
)
from sqlalchemy.orm import Session

from app.database.conn import Base, db
from app.models.user import UserCreate


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.key != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        # for col in obj.all_columns():
        #     col_name = col.name
        for col_name in kwargs:
            setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        ret = None

        self._session.flush()
        if qs > 0:
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        print(self.served)
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


class User(Base, BaseMixin):
    __tablename__ = "tb_member"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, name="idx")
    phone_number = Column(String(length=20), nullable=False, name="phoneNumber")
    phone_auth = Column(String(length=1), nullable=False, default='N', name="phoneAuth")
    passwd = Column(String(length=100), nullable=False)
    login_type = Column(String(length=20), nullable=False, name="loginType")
    access_token = Column(String(length=255), nullable=True, name="accessToken")
    profile_img = Column(String(length=255), nullable=False, name="profileImg")
    nick_name = Column(String(length=10), nullable=False, name="nickName")
    email = Column(String(length=100), nullable=True)
    cover_distance = Column(Integer, nullable=False, name="coverDistance", default=3000)
    created_at = Column(DateTime, nullable=False, name="wdate", default=func.utc_timestamp())
    last_pw_date = Column(DateTime, nullable=False, name="lastPWDate", default=func.utc_timestamp())
    last_login_date = Column(DateTime, nullable=False, name="lastLoginDate", default=func.utc_timestamp())
    device_name = Column(String(length=100), nullable=False, name="deviceName")
    device_model = Column(String(length=100), nullable=False, name="deviceModel")
    device_id = Column(String(length=100), nullable=False, name="deviceID")
    trade_point = Column(Integer, nullable=False, name="tradePoint", default=0)
    company_auth = Column(String(length=1), nullable=False, name="companyAuth")
    marketing_receive = Column(String(length=1), nullable=False, name="marketingReceive")
    marketing_night_reject = Column(String(length=1), nullable=False, name="marketingNightReject")
    # thirdPartyAgree = Column(String(length=1), nullable=False)


class Deal(Base, BaseMixin):
    __tablename__ = "tb_pDeal"
    idx = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    phone_number = Column(String(length=20), nullable=False)
    goods_name = Column(String(length=60), nullable=False)
    hope_price = Column(Integer, nullable=False)
