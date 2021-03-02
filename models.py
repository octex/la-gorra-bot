import os
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import Sequence

load_dotenv()

Column(Integer, Sequence('id'), primary_key=True)
Base = declarative_base()
Table = Table()
DB_PATH = os.getenv('DB_PATH')
engine = create_engine(DB_PATH, echo=True)


class Minion(Base):
    __tablename__ = "minions"

    id = Column(Integer(), Sequence('id'), primary_key=True)
    username = Column(String())
    full_username = Column(String())
    mention_in_server = Column(String())
    strikes = Column(Integer())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "<Minion(id='%s', username='%s', full_username='%s', mention_in_server='%s', strikes='%s')>" % (
                                self.id, self.username, self.full_username, self.mention_in_server, self.strikes)

class BotConfig(Base):
    __tablename__ = "botConfig"

    keyConfig = Column(String(), primary_key=True)
    value = Column(String())
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "<Config(keyConfig='%s', value='%s')>" % (
            self.keyConfig, self.value)

Base.metadata.create_all(engine)
