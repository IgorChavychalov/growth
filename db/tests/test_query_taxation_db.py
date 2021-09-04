import sqlalchemy.orm
from db.model import Base, Sites, Plots, Taxation, Species, Trees, Defects, Heights, Crowns, Models, Sections, Relations
from datetime import date
from db.query import SitesQuery


class SetupBase:
    def setup(self):
        # Создаём суслика
        engine = sqlalchemy.create_engine(f'sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)  # импорт структуры БД
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()
        self.session = session
        self.sites_query = SitesQuery(self.session)

    def get_data_by_id(self, table, id):
        return self.session.query(table).filter(table.id == id).one()


class TestSiteQuery(SetupBase):

    def get_data_by_id(self, id, table=Sites):
        return super(TestSiteQuery, self).get_data_by_id(table, id)

    def test_create(self):
        args = ['Сяськое', 184, '10', 2000, 2001, 2010]
        self.sites_query.create(*args)

        answer = "; ".join(map(str, args))
        result = self.get_data_by_id(1).__repr__()
        assert result == answer

    def test_read(self):
        self.sites_query.create('Сяськое', 184, '10', 2000, 2001, 2010)
        self.sites_query.create('Пригородное', 184, '10', 2000, 2001, 2010)

        result = self.sites_query.read(2).forestry
        answer = 'Пригородное'
        assert result == answer

    def test_delete(self):
        self.sites_query.create('Сяськое', 184, '10', 2000, 2001, 2010)
        self.sites_query.create('Пригородное', 184, '10', 2000, 2001, 2010)
        self.sites_query.create('Пригородное', 184, '10', 2000, 2001, 2010)

        self.sites_query.delete(2)
        result = self.session.query(Sites).count()
        answer = 2
        assert result == answer

    def test_update(self):
        self.sites_query.create('Сяськое', 184, '10', 2000, 2001, 2010)
        self.sites_query.create('Пригородное', 184, '10', 2000, 2001, 2010)

        self.sites_query.update(2, {'forestry': 'Шомушское'})
        result = self.sites_query.read(2).forestry
        answer = 'Шомушское'
        assert result == answer
