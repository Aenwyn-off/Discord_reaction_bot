from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Emoji

from os import getenv
from dotenv import load_dotenv

load_dotenv()
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



def add_user(dis_id, dis_name):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    if user is None:
        new_user = User(dis_id=dis_id, dis_name=dis_name)
        session.add(new_user)
        session.commit()


def get_user(dis_id):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    return user


def add_emoji(dis_id, emoji):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    new_report = Emoji(emoji=emoji, owner=user.id)
    session.add(new_report)
    session.commit()


def get_emojis(dis_id):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    emojis = user.emote
    return emojis


def delete_user_emoji(emoji):
    session = Session()
    emo = session.query(Emoji).filter(Emoji.emoji == emoji).first().id
    emojis = session.get(Emoji, emo)
    session.delete(emojis)
    session.commit()


def delete_all_emoji_from_user(dis_id):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    emotions = user.emote
    for emote in emotions:
        session.delete(emote)
    session.commit()