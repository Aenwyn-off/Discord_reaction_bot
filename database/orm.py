from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Emoji

from os import getenv
from dotenv import load_dotenv

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
load_dotenv()


def add_user(dis_id, dis_name):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    if user is None:
        new_user = User(dis_id=dis_id, dis_name=dis_name)
        session.add(new_user)
        session.commit()


def add_emoji(dis_id, emoji):
    session = Session()
    user = session.query(User).filter(User.dis_id == dis_id).first()
    new_report = Emoji(emoji=emoji, owner=user.id)
    session.add(new_report)
    session.commit()


# def get_emoji(dis_id):
#     session = Session()
#     user = session.query(User).filter(User.dis_id == dis_id).all
#     emoji = user.emoji
#     return emoji
#
#
# def delete_user_emoji(emoji):
#     session = Session()
#     emojis = session.get(Emoji, emoji)
#     session.delete(emojis)
#     session.commit()
#
#
# def delete_all_emoji_from_user():
#     session = Session()
#     users = session.query(User).all()
#     return users