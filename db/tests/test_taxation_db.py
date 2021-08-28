import sqlalchemy.orm
from db.model import Base, Sites, Plots, Taxation
from datetime import date


class TestInitBase:
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
        plot1 = Plots(site=1, TLU='В2', forest_type='ЧС', number=1, area=600)
        plot2 = Plots(site=1, TLU='В2', forest_type='ЧС', number=2, area=600)
        plot3 = Plots(site=1, TLU='В2', forest_type='ЧС', number=3, area=600)
        self.session.add_all([plot1, plot2, plot3])
        # Запись в таблие Taxation для тестов
        tax1 = Taxation(id_site=2, name='до рубки', date=date(2010, 2, 10), vegetation_year='2010', age_after_cut=99,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=49)
        tax2 = Taxation(id_site=2, name='после рубки', date=date(2010, 2, 10), vegetation_year='2010', age_after_cut=0,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=79)
        tax3 = Taxation(id_site=2, name='3 года после рубки', date=date(2013, 2, 10), vegetation_year='2013', age_after_cut=3,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=109)
        self.session.add_all([tax1, tax2, tax3])

    def test_exist_data_in_sites_table(self):
        result = self.session.query(Sites).filter(Sites.id == 1).one().__repr__()
        answer = 'Сяськое; 184; 10; 2000; 2001; 2010'

        assert result == answer

    def test_exist_data_in_plots_table(self):
        result = self.session.query(Plots).filter(Plots.id == 1).one().__repr__()
        answer = '1; В2; ЧС; 1; 600'

        assert result == answer

    def test_relation_plot_in_site_table(self):
        answer = 1
        plot = self.session.query(Plots).filter(Plots.id == 3).one()
        result = self.session.query(Sites).filter(Sites.id == plot.id_site).one()
        assert result.id == answer

    def test_exist_data_in_taxations_table(self):
        result = self.session.query(Taxation).filter(Taxation.id == 2).one().__repr__()
        answer = '2; после рубки; 2010-02-10; 2010; 0; 3; 1800; 5.555556; 79'

        assert result == answer

    def test_relation_taxations_in_site_table(self):
        answer = 2
        taxation = self.session.query(Taxation).filter(Taxation.id == 3).one()
        result = self.session.query(Sites).filter(Sites.id == taxation.id_site).one()
        assert result.id == answer
