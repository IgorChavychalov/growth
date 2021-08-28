from pytest import raises
import sqlalchemy.orm
from db.model import Base, Sites, Plots


class TestBase:
    def setup(self):
        # Создаём суслика
        engine = sqlalchemy.create_engine(f'sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)  # импорт структуры БД
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()

        self.session = session
        # Запись в таблие Site для тестов
        site1 = Sites(forestry='Сяськое', kvartal='184', vydel='10', clearcut=2000, planting=2001, thining=2010)
        site2 = Sites(forestry='Сяськое', kvartal='77', vydel='1', clearcut=2000, planting=2001, thining=2010)
        self.session.add_all([site1, site2])
        # Запись в таблие Site для тестов
        plot1 = Plots(site=1, TLU='В2', forest_type='ЧС', number=1, area=800)
        plot2 = Plots(site=1, TLU='В2', forest_type='ЧС', number=2, area=800)
        plot3 = Plots(site=1, TLU='В2', forest_type='ЧС', number=3, area=800)
        self.session.add_all([plot1, plot2, plot3])

    def test_exist_data_in_sites_table(self):
        result = self.session.query(Sites).filter(Sites.id == 1).one().__repr__()
        answer = 'Сяськое; 184; 10; 2000; 2001; 2010'
        # Логин уникальный
        assert result == answer

    def test_exist_data_in_plots_table(self):
        result = self.session.query(Plots).filter(Plots.id == 1).one().__repr__()
        answer = '1; В2; ЧС; 1; 800'
        # Логин уникальный
        assert result == answer

    def test_relation_plot_in_site_table(self):
        answer = 1
        plot = self.session.query(Plots).filter(Plots.id == 3).one()
        result = self.session.query(Sites).filter(Sites.id == plot.id_site).all()[0]
        assert result.id == answer
