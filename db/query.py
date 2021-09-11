from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import max as db_max

from db.model import Sites, Plots, Taxation


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
        try:
            self.session.query(Sites).filter(Sites.id == id).update(kwargs, synchronize_session='fetch')
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def get_all_sites_obj(self):
        try:
            return self.session.query(Sites).all()
        except IntegrityError:
            self.session.rollback()

    def get_all_sites_list(self):
        try:
            site_list = []
            sites = self.get_all_sites_obj()
            for site in sites:
                site_list.append(site.__str__())
            return site_list
        except IntegrityError:
            self.session.rollback()

    def set_quantity_plots(self):
        try:
            sites = self.get_all_sites_obj()
            for site in sites:
                site.quantity_plots = site.plot.__len__()
        except IntegrityError:
            self.session.rollback()

    def set_last_tax(self):
        try:
            sites_list = self.get_all_sites_obj()
            for site in sites_list:
                tax_list = site.taxation
                for tax in tax_list:
                    last_year = self.session.query(db_max(tax.vegetation_year)).first()[0]
                    if last_year:
                        site.last_tax = last_year
        except IntegrityError:
            self.session.rollback()


class PlotsQuery:
    def __init__(self, session):
        """ передача сессии """
        self.session = session

    def create(self, id_site, TLU, forest_type, number, area):
        try:
            self.session.add(Plots(id_site, TLU, forest_type, number, area))
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
