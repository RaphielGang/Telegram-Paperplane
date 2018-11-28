from userbot.modules.sql_helper import SESSION,BASE
from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func
class Notes(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)
    def __init__(self, chat_id, keyword, reply):
            self.chat_id = str(chat_id)  # ensure string
            self.keyword = keyword
            self.reply = reply
    def __eq__(self, other):
        return bool(isinstance(other, Filters)
                    and self.chat_id == other.chat_id
                    and self.keyword == other.keyword)
Notes.__table__.create(checkfirst=True)
def get_notes(chat_id):
    try:
        return SESSION.query(Notes).all()
    finally:
        SESSION.close()
def add_note(chat_id, keyword, reply):
    adder=Notes(str(chat_id),keyword,reply)
    SESSION.add(adder)
    SESSION.commit()
def remove_notes(chat_id,keyword):
    rem = SESSION.query(Notes).get((str(chat_id), keyword))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
