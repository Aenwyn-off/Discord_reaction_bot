from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, select, Table, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    dis_id = Column(BigInteger, nullable=False)
    dis_name = Column(String, nullable=False)
    emojik = relationship('Emoji', backref='emojik', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.dis_id


class Emoji(Base):
    __tablename__ = 'Emojis'
    id = Column(Integer, primary_key=True)
    emoji = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return self.emoji


engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
