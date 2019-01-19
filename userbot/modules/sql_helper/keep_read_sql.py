try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise Exception("Hello!")

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func


class KRead(BASE):
    __tablename__ = "kread"
    groupid = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.groupid = str(sender)


KRead.__table__.create(checkfirst=True)


def is_kread():
    try:
        return SESSION.query(KRead).all()
    except:
        return None
    finally:
        SESSION.close()


def kread(chat):
    adder = KRead(str(chat))
    SESSION.add(adder)
    SESSION.commit()


def unkread(chat):
    rem = SESSION.query(KRead).get((str(chat)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
