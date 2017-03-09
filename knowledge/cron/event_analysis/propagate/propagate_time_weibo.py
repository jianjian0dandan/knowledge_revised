# -*- coding: utf-8 -*-

from config import db

class PropagateTimeWeibos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True))
    weibos = db.Column(db.Text) # weibos=[weibos]

    def __init__(self, topic, end, range, mtype, limit, weibos):
        self.topic = topic
        self.end = end
        self.range = range
        self.mtype = mtype
        self.limit = limit
        self.weibos = weibos

    @classmethod
    def _name(cls):
        return u'PropagateTimeWeibos'

if __name__ == '__main__':
    db.create_all()