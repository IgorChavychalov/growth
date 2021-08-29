import sqlalchemy.orm
from db.model import Base, Sites, Plots, Taxation, Species, Trees, Defects, Heights, Crowns
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
        site1 = Sites(forestry='Сяськое', kvartal='184', vydel='10', clearcut=2000, planting=2001, thinning=2010)
        site2 = Sites(forestry='Сяськое', kvartal='77', vydel='1', clearcut=2000, planting=2001, thinning=2010)
        self.session.add_all([site1, site2])
        # Запись в таблие Plots для тестов
        plot1 = Plots(id_site=1, TLU='В2', forest_type='ЧС', number=1, area=600)
        plot2 = Plots(id_site=1, TLU='С2', forest_type='КС', number=2, area=600)
        plot3 = Plots(id_site=1, TLU='В4', forest_type='ДЛ', number=3, area=600)
        self.session.add_all([plot1, plot2, plot3])
        # Запись в таблие Taxation для тестов
        tax1 = Taxation(id_site=2, name='до рубки', date=date(2010, 2, 10), vegetation_year='2010', age_after_cut=99,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=49)
        tax2 = Taxation(id_site=2, name='после рубки', date=date(2010, 2, 10), vegetation_year='2010', age_after_cut=0,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=79)
        tax3 = Taxation(id_site=2, name='3 года после рубки', date=date(2013, 2, 10), vegetation_year='2013', age_after_cut=3,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=109)
        self.session.add_all([tax1, tax2, tax3])
        # Запись в таблие Species для тестов
        sp1 = Species(id_tax=1, species='Б', age=10, floor=1, step_level=1)
        sp2 = Species(id_tax=2, species='Б', age=11, floor=1, step_level=1)
        sp3 = Species(id_tax=3, species='Б', age=13, floor=1, step_level=2)
        self.session.add_all([sp1, sp2, sp3])
        # Запись в таблие Trees для тестов
        tree1 = Trees(id_tax=1, id_plot=1, id_species=1, number_tree=1, kraft=4, diameter_one=62, diameter_two=64, diameter_med=63)
        tree2 = Trees(id_tax=1, id_plot=1, id_species=1, number_tree=2, kraft=3, diameter_one=82, diameter_two=84, diameter_med=83)
        tree3 = Trees(id_tax=3, id_plot=2, id_species=2, number_tree=3, kraft=2, diameter_one=102, diameter_two=104, diameter_med=103)
        tree4 = Trees(id_tax=1, id_plot=1, id_species=3, number_tree=4, kraft=1, diameter_one=122, diameter_two=124, diameter_med=123)
        self.session.add_all([tree1, tree2, tree3, tree4])
        # Запись в таблие Defect для тестов
        defect = Defects(id_tree=2, defect_info='морозобоина', defect_value='3 см', defect_age=2010)
        self.session.add(defect)
        # Запись в таблие Heights для тестов
        height1 = Heights(diameter_med=63, height_tree=107, height_crown=80)
        height2 = Heights(diameter_med=83, height_tree=127, height_crown=100)
        height3 = Heights(diameter_med=103, height_tree=147, height_crown=120)
        height4 = Heights(diameter_med=123, height_tree=167, height_crown=140)
        self.session.add_all([height1, height2, height3, height4])
        # Запись в таблие Crowns для тестов
        crown1 = Crowns(length=80, north=10, south=10, west=10, east=10, diameter=20, area=78, volume=200)
        crown2 = Crowns(length=90, north=15, south=15, west=15, east=15, diameter=30, area=177, volume=300)
        crown3 = Crowns(length=100, north=20, south=20, west=20, east=20, diameter=40, area=314, volume=400)
        crown4 = Crowns(length=110, north=25, south=25, west=25, east=25, diameter=50, area=491, volume=500)
        self.session.add_all([crown1, crown2, crown3, crown4])

    def get_data_by_id(self, table, id):
        return self.session.query(table).filter(table.id == id).one()

    def test_exist_data_in_sites_table(self):
        result = self.get_data_by_id(Sites, 1).__repr__()
        answer = 'Сяськое; 184; 10; 2000; 2001; 2010'

        assert result == answer

    def test_exist_data_in_plots_table(self):
        result = self.get_data_by_id(Plots, 1).__repr__()
        answer = '1; В2; ЧС; 1; 600'

        assert result == answer

    def test_exist_data_in_taxation_table(self):
        result = self.get_data_by_id(Taxation, 2).__repr__()
        answer = '2; после рубки; 2010-02-10; 2010; 0; 3; 1800; 5.555556; 79'

        assert result == answer

    def test_exist_data_in_species_table(self):
        result = self.get_data_by_id(Species, 3).__repr__()
        answer = '3; Б; 13; 1; 2'

        assert result == answer

    def test_exist_data_in_trees_table(self):
        result = self.get_data_by_id(Trees, 4).__repr__()
        answer = '1; 1; 3; 4; 1; 122; 124; 123'

        assert result == answer

    def test_exist_data_in_defect_table(self):
        result = self.get_data_by_id(Defects, 1).__repr__()
        answer = '2; морозобоина; 3 см; 2010'

        assert result == answer

    def test_exist_data_in_height_table(self):
        result = self.get_data_by_id(Heights, 3).__repr__()
        answer = '103; 147; 120'

        assert result == answer

    def test_exist_data_in_crown_table(self):
        result = self.get_data_by_id(Crowns, 3).__repr__()
        answer = '100; 20; 20; 20; 20; 40; 314; 400'

        assert result == answer

    def test_relation_plot_in_site_table(self):
        answer = 1
        plot = self.get_data_by_id(Plots, 3)
        result = self.session.query(Sites).filter(Sites.id == plot.id_site).one().id
        assert result == answer

    def test_relation_taxation_in_site_table(self):
        answer = 2
        taxation = self.get_data_by_id(Taxation, 3)
        result = self.session.query(Sites).filter(Sites.id == taxation.id_site).one().id
        assert result == answer

    def test_relation_species_in_taxation_table(self):
        answer = '3 года после рубки'
        species = self.get_data_by_id(Species, 3)
        result = self.session.query(Taxation).filter(Taxation.id == species.id_tax).one().name
        assert result == answer

    def test_relation_trees_in_taxation_table(self):
        answer = '3 года после рубки'
        tree = self.get_data_by_id(Trees, 3)
        result = self.session.query(Taxation).filter(Taxation.id == tree.id_tax).one().name
        assert result == answer

    def test_relation_trees_in_plots_table(self):
        answer = 'С2'
        tree = self.get_data_by_id(Trees, 3)
        result = self.session.query(Plots).filter(Plots.id == tree.id_plot).one().TLU
        assert result == answer

    def test_relation_trees_in_species_table(self):
        answer = 11
        tree = self.get_data_by_id(Trees, 3)
        result = self.session.query(Species).filter(Species.id == tree.id_species).one().age
        assert result == answer

    def test_relation_defects_in_tree_table(self):
        answer = 3
        defect = self.get_data_by_id(Defects, 1)
        result = self.session.query(Trees).filter(Trees.id == defect.id_tree).one().kraft
        assert result == answer
