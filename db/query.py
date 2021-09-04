from sqlalchemy.exc import IntegrityError

from .model import Sites, Plots, Base


class SitesQuery:
    def __init__(self, session):
        """ передача сессии """
        self.session = session

    def read(self, id):
        try:
            return self.session.query(Sites).get(id)
        except IntegrityError:
            self.session.rollback()

    def create(self, forestry, kvartal, vydel, clearcut, planting, thinning):
        try:
            self.session.add(Sites(forestry, kvartal, vydel, clearcut, planting, thinning))
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def delete(self, id):
        try:
            row = self.session.query(Sites).get(id)
            self.session.delete(row)
        except IntegrityError:
            self.session.rollback()

    def update(self, id, kwargs):
        self.session.query(Sites).filter(Sites.id == id).update(kwargs, synchronize_session='fetch')
        self.session.commit()


