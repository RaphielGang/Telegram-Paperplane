try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise Exception("Hello!")

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GMute.__table__.create(checkfirst=True)


def is_gmuted(sender_id):
    try:
        return SESSION.query(GMute).all()
    except:
        return None
    finally:
        SESSION.close()


def gmute(sender):
    adder = GMute(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender):
    rem = SESSION.query(GMute).get((str(sender)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
