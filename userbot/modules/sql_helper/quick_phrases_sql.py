try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class QuickPhrase(BASE):
    __tablename__ = "quickphrases"
    resp = Column(String(10), primary_key=True)
    phrase = Column(UnicodeText, primary_key=True)

    def __init__(self, resp, phrase):
        self.phrase = str(phrase)
        self.resp = str(resp)


QuickPhrase.__table__.create(checkfirst=True)


def get_phrases(resp):
    try:
        return SESSION.query(QuickPhrase).filter(QuickPhrase.resp == str(resp)).all()
    finally:
        SESSION.close()


def add_phrase(resp, phrase):
    adder = QuickPhrase(str(resp), phrase)
    SESSION.add(adder)
    SESSION.commit()


def remove_phrase(resp, phrase):
    rem = SESSION.query(QuickPhrase).get((str(resp),str(phrase)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
