from db.tests.test_init_db import FullBase
from db.query import SitesQuery
from db.model import Sites, Plots, Base


class TestSiteQuery(FullBase):
    def setup(self):
        super().setup()
        self.sites_query = SitesQuery(self.session)

    def get_data_by_id(self, table, id):
        return super(TestSiteQuery, self).get_data_by_id(table, id)

    def test_set_quantity_plots(self):
        answer = 3
        self.sites_query.set_quantity_plots()
        result = self.get_data_by_id(Sites, 1).quantity_plots

        assert result == answer

    def test_set_last_tax(self):
        answer = 2013
        self.sites_query.set_last_tax()
        result = self.get_data_by_id(Sites, 2).last_tax

        assert result == answer

    def test_get_all_sites_list(self):
        answer = ['Сяськое', 184, '10', 2000, 2001, 2010, 0, 0]
        result = self.sites_query.get_all_sites_list()

        assert result[0] == answer
