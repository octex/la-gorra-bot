from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///gorra-db.db', echo=True)
Base.metadata.create_all(engine)

class Minion(Base):
    __tablename__ = "minions"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    full_username = Column(String())
    mention_in_server = Column(String())
    strikes = Column(Integer())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "<Minion(id='%s', username='%s', full_username='%s', mention_in_server='%s', strikes='%s')>"