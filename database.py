from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    lvl = Column(Integer, nullable=False, default=0)


engine = create_engine('sqlite:///levels.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)


def set_lvl(uid: int, new_level: int):
    session = DBSession()
    edited_user = session.query(User).filter_by(uid=uid).first()

    if not edited_user:
        edited_user = User(uid=uid)

    edited_user.lvl = new_level
    session.add(edited_user)
    session.commit()


def get_lvl(uid: int):
    session = DBSession()
    user = session.query(User).filter_by(uid=uid).first()

    if not user:
        user = User(uid=uid)

    session.close()

    return user.lvl
