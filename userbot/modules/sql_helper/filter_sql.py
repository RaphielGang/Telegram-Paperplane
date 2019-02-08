try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise Exception("Hello!")
from sqlalchemy import Column, String, UnicodeText


class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, keyword, reply):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.reply = reply

    def __eq__(self, other):
        return bool(
            isinstance(other, Filters)
            and self.chat_id == other.chat_id
            and self.keyword == other.keyword
        )


Filters.__table__.create(checkfirst=True)


def get_filters(chat_id):
    try:
        return SESSION.query(Filters).filter(Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply):
    adder = Filters(str(chat_id), keyword, reply)
    SESSION.add(adder)
    SESSION.commit()


def remove_filter(chat_id, keyword):
    rem = SESSION.query(Filters).get((str(chat_id), keyword))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
