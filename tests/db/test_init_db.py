import sqlalchemy.orm
from ...db.model import Base, Sites, Plots, Taxation, Species, Trees, Defects, Heights, Crowns, Models, Sections, Relations
from datetime import date


class FullBase:
    def setup(self):
        # Создаём суслика
        engine = sqlalchemy.create_engine(f'sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)  # импорт структуры БД
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()

        self.session = session
        # Запись в таблие Site для тестов
        site1 = Sites(forestry='Сяськое', kvartal=184, vydel='10', clearcut=2000, planting=2001, thinning=2010)
        site2 = Sites(forestry='Сяськое', kvartal=77, vydel='1', clearcut=2000, planting=2001, thinning=2010)
        self.session.add_all([site1, site2])
        # Запись в таблие Plots для тестов
        plot1 = Plots(id_site=1, TLU='В2', forest_type='ЧС', number=1, area=600)
        plot2 = Plots(id_site=1, TLU='С2', forest_type='КС', number=2, area=600)
        plot3 = Plots(id_site=1, TLU='В4', forest_type='ДЛ', number=3, area=600)
        self.session.add_all([plot1, plot2, plot3])
        # Запись в таблие Taxation для тестов
        tax1 = Taxation(id_site=2, name='до рубки', date=date(2010, 2, 10), vegetation_year=2010, age_after_cut=99,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=49)
        tax2 = Taxation(id_site=2, name='после рубки', date=date(2010, 2, 10), vegetation_year=2010, age_after_cut=0,
                        quantity_plots=3, total_area=1800, trans_coef=5.555556, diameter_med=79)
        tax3 = Taxation(id_site=2, name='3 года после рубки', date=date(2013, 2, 10), vegetation_year=2013, age_after_cut=3,
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
        tree5 = Trees(id_tax=1, id_plot=1, id_species=3, number_tree=5, kraft=1, diameter_one=112, diameter_two=114, diameter_med=113)
        tree6 = Trees(id_tax=1, id_plot=1, id_species=3, number_tree=6, kraft=1, diameter_one=122, diameter_two=124, diameter_med=123)
        tree7 = Trees(id_tax=1, id_plot=1, id_species=3, number_tree='m1', kraft=1, diameter_one=122, diameter_two=124, diameter_med=123)
        tree8 = Trees(id_tax=1, id_plot=1, id_species=3, number_tree='m2', kraft=1, diameter_one=122, diameter_two=124, diameter_med=123)
        self.session.add_all([tree1, tree2, tree3, tree4, tree5, tree6, tree7, tree8])
        # Запись в таблие Defect для тестов
        defect = Defects(id_tree=2, info='морозобоина', value='3 см', age=2010)
        self.session.add(defect)
        # Запись в таблие Heights для тестов
        height1 = Heights(id_tree=1, height_tree=107, height_crown=80)
        height2 = Heights(id_tree=2, height_tree=127, height_crown=100)
        height3 = Heights(id_tree=3, height_tree=147, height_crown=120)
        height4 = Heights(id_tree=4, height_tree=167, height_crown=140)
        height5 = Heights(id_tree=5, height_tree=157, height_crown=130)
        height6 = Heights(id_tree=6, height_tree=167, height_crown=135)
        self.session.add_all([height1, height2, height3, height4, height5, height6])
        # Запись в таблие Crowns для тестов
        crown1 = Crowns(length=80, north=10, south=10, west=10, east=10, diameter=20, area=78, volume=200)
        crown2 = Crowns(length=90, north=15, south=15, west=15, east=15, diameter=30, area=177, volume=300)
        crown3 = Crowns(length=100, north=20, south=20, west=20, east=20, diameter=40, area=314, volume=400)
        crown4 = Crowns(length=110, north=25, south=25, west=25, east=25, diameter=50, area=491, volume=500)
        crown5 = Crowns(length=120, north=20, south=20, west=20, east=20, diameter=40, area=314, volume=400)
        crown6 = Crowns(length=125, north=25, south=25, west=25, east=25, diameter=50, area=491, volume=500)
        self.session.add_all([crown1, crown2, crown3, crown4, crown5, crown6])
        # Запись в таблие Models для тестов
        model1 = Models(age=12, last_grw_length=100, last_grw_age=5, length_liquid=80, vol_wood=100,
                       vol_wood_bk=105, vol_bark=5, vol_liquid=60)
        model2 = Models(age=14, last_grw_length=100, last_grw_age=5, length_liquid=80, vol_wood=100,
                       vol_wood_bk=105, vol_bark=5, vol_liquid=60)
        self.session.add_all([model1, model2])
        # Запись в таблие Sections для тестов
        sec1 = Sections(id_model=2, section_relation=0, section_length=0, bark=False, diameter_sw=90, diameter_we=96, diameter_med=93, volume=100)
        sec2 = Sections(id_model=2, section_relation=10, section_length=100, bark=False, diameter_sw=80, diameter_we=86, diameter_med=83, volume=90)
        sec3 = Sections(id_model=2, section_relation=20, section_length=200, bark=False, diameter_sw=70, diameter_we=76, diameter_med=73, volume=80)
        sec4 = Sections(id_model=2, section_relation=30, section_length=300, bark=False, diameter_sw=60, diameter_we=66, diameter_med=63, volume=70)
        sec5 = Sections(id_model=2, section_relation=40, section_length=400, bark=False, diameter_sw=50, diameter_we=56, diameter_med=53, volume=60)
        sec6 = Sections(id_model=2, section_relation=50, section_length=500, bark=False, diameter_sw=40, diameter_we=46, diameter_med=43, volume=50)
        sec7 = Sections(id_model=2, section_relation=60, section_length=600, bark=False, diameter_sw=30, diameter_we=36, diameter_med=33, volume=40)
        sec8 = Sections(id_model=2, section_relation=70, section_length=700, bark=False, diameter_sw=20, diameter_we=26, diameter_med=23, volume=30)
        sec9 = Sections(id_model=2, section_relation=80, section_length=800, bark=False, diameter_sw=10, diameter_we=16, diameter_med=13, volume=20)
        sec10 = Sections(id_model=2, section_relation=90, section_length=900, bark=False, diameter_sw=5, diameter_we=11, diameter_med=8, volume=10)
        sec11 = Sections(id_model=2, section_relation=100, section_length=100, bark=False, diameter_sw=0, diameter_we=0, diameter_med=0, volume=1)
        self.session.add_all([sec1, sec2, sec3, sec4, sec5, sec6, sec7, sec8, sec9, sec10, sec11])
        # Запись в таблие Relations для тестов
        rel1 = Relations(id_tree=1, id_model=0, id_species=1, id_height=1, id_crown=1, id_plot=1, kraft=4, step=6)
        rel2 = Relations(id_tree=2, id_model=0, id_species=1, id_height=2, id_crown=2, id_plot=1, kraft=3, step=8)
        rel3 = Relations(id_tree=3, id_model=0, id_species=2, id_height=3, id_crown=3, id_plot=2, kraft=2, step=10)
        rel4 = Relations(id_tree=4, id_model=0, id_species=3, id_height=4, id_crown=4, id_plot=1, kraft=1, step=12)
        rel5 = Relations(id_tree=None, id_model=1, id_species=2, id_height=5, id_crown=5, id_plot=1, kraft=1, step=8)
        rel6 = Relations(id_tree=None, id_model=2, id_species=2, id_height=6, id_crown=6, id_plot=1, kraft=1, step=10)
        self.session.add_all([rel1, rel2, rel3, rel4, rel5, rel6])

    def get_data_by_id(self, table, id):
        return self.session.query(table).filter(table.id == id).one()


class TestInitTable(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestInitTable, self).get_data_by_id(table, id)

    def test_init_get_attribute_in_sites_table(self):
        result = self.get_data_by_id(Sites, 1).get_attribute()
        answer = ['Сяськое', 184, "10", 2000, 2001, 2010, 0, 0]

        assert result == answer

    def test_init_data_in_plots_table(self):
        result = self.get_data_by_id(Plots, 1).__repr__()
        answer = '1; 1; 600; В2; ЧС'

        assert result == answer

    def test_init_data_in_taxation_table(self):
        result = self.get_data_by_id(Taxation, 2).__repr__()
        answer = '2; после рубки; 2010-02-10; 2010; 0; 3; 1800; 5.555556; 79'

        assert result == answer

    def test_init_data_in_species_table(self):
        result = self.get_data_by_id(Species, 3).__repr__()
        answer = '3; Б; 13; 1; 2'

        assert result == answer

    def test_init_data_in_trees_table(self):
        result = self.get_data_by_id(Trees, 4).__repr__()
        answer = '1; 1; 3; 4; 1; 122; 124; 123'

        assert result == answer

    def test_init_data_in_defects_table(self):
        result = self.get_data_by_id(Defects, 1).__repr__()
        answer = '2; морозобоина; 3 см; 2010'

        assert result == answer

    def test_init_data_in_heights_table(self):
        result = self.get_data_by_id(Heights, 2).__repr__()
        answer = '127; 100'

        assert result == answer

    def test_init_data_in_crowns_table(self):
        result = self.get_data_by_id(Crowns, 3).__repr__()
        answer = '100; 20; 20; 20; 20; 40; 314; 400'

        assert result == answer

    def test_init_data_in_models_table(self):
        result = self.get_data_by_id(Models, 1).__repr__()
        answer = '12; 100; 5; 80; 100.0; 105.0; 5.0; 60.0'

        assert result == answer

    def test_init_data_in_sections_table(self):
        result = self.get_data_by_id(Sections, 6).__repr__()
        answer = '2; 50; 500; False; 40; 46; 43; 50.0'

        assert result == answer

    def test_init_tree_in_relations_table(self):
        result = self.get_data_by_id(Relations, 2).__repr__()
        answer = '2; 0; 1; 2; 2; 1; 3; 8'

        assert result == answer

    def test_init_model_in_relations_table(self):
        result = self.get_data_by_id(Relations, 6).__repr__()
        answer = 'None; 2; 2; 6; 6; 1; 1; 10'

        assert result == answer


class TestRelationsManually(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationsManually, self).get_data_by_id(table, id)

    def test_relation_plots_in_sites_table(self):
        answer = 1
        plot = self.get_data_by_id(Plots, 3)
        result = self.session.query(Sites).filter(Sites.id == plot.id_site).one().id
        assert result == answer

    def test_relation_taxation_in_sites_table(self):
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

    def test_relation_defects_in_trees_table(self):
        answer = 3
        defect = self.get_data_by_id(Defects, 1)
        result = self.session.query(Trees).filter(Trees.id == defect.id_tree).one().kraft
        assert result == answer

    def test_relation_sections_in_models_table(self):
        answer = 14
        section = self.get_data_by_id(Sections, 1)
        result = self.session.query(Models).filter(Models.id == section.id_model).one().age
        assert result == answer

    def test_relation_relations_in_trees_table(self):
        answer = 4
        relation = self.get_data_by_id(Relations, 1)
        result = self.session.query(Trees).filter(Trees.id == relation.id_tree).one().kraft
        assert result == answer

    def test_relation_relations_in_model_table(self):
        answer = 14
        relation = self.get_data_by_id(Relations, 6)
        result = self.session.query(Models).filter(Models.id == relation.id_model).one().age
        assert result == answer

    def test_relation_relations_in_species_table(self):
        answer = 10
        relation = self.get_data_by_id(Relations, 2)
        result = self.session.query(Species).filter(Species.id == relation.id_species).one().age
        assert result == answer

    def test_relation_relations_in_heights_table(self):
        answer = 127
        relation = self.get_data_by_id(Relations, 2)
        result = self.session.query(Heights).filter(Heights.id == relation.id_height).one().height_tree
        assert result == answer

    def test_relation_relations_in_crown_table(self):
        answer = 90
        relation = self.get_data_by_id(Relations, 2)
        result = self.session.query(Crowns).filter(Crowns.id == relation.id_crown).one().length
        assert result == answer

    def test_relation_relations_in_plot_table(self):
        answer = 'В2'
        relation = self.get_data_by_id(Relations, 2)
        result = self.session.query(Plots).filter(Plots.id == relation.id_plot).one().TLU
        assert result == answer


class TestFirstID(FullBase):
    def first_id(self, table):
        return self.session.query(table).all()[0].id

    def test_first_id_sites(self):
        answer = 1
        result = self.first_id(Sites)
        assert result == answer

    def test_first_id_plots(self):
        answer = 1
        result = self.first_id(Plots)
        assert result == answer

    def test_first_id_taxation(self):
        answer = 1
        result = self.first_id(Taxation)
        assert result == answer

    def test_first_id_species(self):
        answer = 1
        result = self.first_id(Species)
        assert result == answer

    def test_first_id_trees(self):
        answer = 1
        result = self.first_id(Trees)
        assert result == answer

    def test_first_id_defects(self):
        answer = 1
        result = self.first_id(Defects)
        assert result == answer

    def test_first_id_heights(self):
        answer = 1
        result = self.first_id(Heights)
        assert result == answer

    def test_first_id_crowns(self):
        answer = 1
        result = self.first_id(Crowns)
        assert result == answer

    def test_first_id_models(self):
        answer = 1
        result = self.first_id(Models)
        assert result == answer

    def test_first_id_sections(self):
        answer = 1
        result = self.first_id(Sections)
        assert result == answer

    def test_first_id_relations(self):
        answer = 1
        result = self.first_id(Relations)
        assert result == answer


class TestRelationShipSitesToPlot(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationShipSitesToPlot, self).get_data_by_id(table, id)

    def test_plots_to_site(self):
        answer = 184
        plot = self.get_data_by_id(Plots, 1)
        result = plot.site.kvartal
        assert result == answer

    def test_plots_to_site_all_attribute(self):
        answer = ['Сяськое', 184, '10', 2000, 2001, 2010, 0, 0]
        plot = self.get_data_by_id(Plots, 1)
        result = plot.site.get_attribute()
        assert result == answer

    def test_all_plots_in_site(self):
        answer = [[1, 600, 'В2', 'ЧС'], [2, 600, 'С2', 'КС'], [3, 600, 'В4', 'ДЛ']]
        site = self.get_data_by_id(Sites, 1)
        plots = site.plot

        result = []
        for elem in plots:
            result.append(elem.get_attribute())

        assert result == answer

    def test_site_to_plots(self):
        answer = "В4"
        site = self.get_data_by_id(Sites, 1)
        result = site.plot[2].TLU
        assert result == answer

    def test_site_to_plots_all_attribute(self):
        answer = [2, 600, 'С2', 'КС']
        site = self.get_data_by_id(Sites, 1)
        result = site.plot[1].get_attribute()
        assert result == answer


class TestRelationShipPlotToTax(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationShipPlotToTax, self).get_data_by_id(table, id)

    def test_site_to_taxation_get_names(self):
        answer = ['до рубки', 'после рубки', '3 года после рубки']
        site = self.get_data_by_id(Sites, 2)
        tax = site.taxation

        result = []
        for elem in tax:
            result.append(elem.get_attribute()[0])

        assert result == answer

    def test_taxation_to_site(self):
        answer = 77
        tax = self.get_data_by_id(Taxation, 2)
        result = tax.site.kvartal
        assert result == answer

    def test_taxation_to_plot_to_site(self):
        answer = 77
        tax = self.get_data_by_id(Taxation, 2)
        res = tax.plot
        result = res.site

        assert result == answer

    def test_site_to_taxation(self):
        answer = "3 года после рубки"
        site = self.get_data_by_id(Sites, 2)
        result = site.taxation[2].name
        assert result == answer


class TestRelationShipTaxToTrees(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationShipTaxToTrees, self).get_data_by_id(table, id)

    def test_taxation_to_species(self):
        answer = 13
        tax = self.get_data_by_id(Taxation, 3)
        result = tax.species[0].age
        assert result == answer

    def test_taxation_to_trees(self):
        answer = 2
        tax = self.get_data_by_id(Taxation, 3)
        result = tax.trees[0].kraft
        assert result == answer

    def test_taxation_to_trees_get_attribute(self):
        answer = [[3, 2, 102, 104, 103]]
        tax = self.get_data_by_id(Taxation, 3)
        trees = tax.trees
        result = []
        for elem in trees:
            result.append(elem.get_attribute())

        assert result == answer


class TestRelationShipTreesToAll(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationShipTreesToAll, self).get_data_by_id(table, id)

    def test_trees_to_defects(self):
        answer = "морозобоина"
        trees = self.get_data_by_id(Trees, 2)
        result = trees.defect[0].info
        assert result == answer

    def test_trees_to_height(self):
        answer = [127, 100]
        trees = self.get_data_by_id(Trees, 2)
        result = list(trees.height)
        assert result == answer

    def test_defects_to_trees(self):
        answer = 3
        defect = self.get_data_by_id(Defects, 1)
        result = defect.trees.kraft
        assert result == answer

    def test_height(self):
        answer = '107; 80'
        result = self.get_data_by_id(Heights, 1)

        assert result == answer








class TestRelationShep(FullBase):
    def get_data_by_id(self, table, id):
        return super(TestRelationShep, self).get_data_by_id(table, id)


    def test_sections_to_models(self):
        answer = 14
        section = self.get_data_by_id(Sections, 1)
        result = section.model.age
        assert result == answer

    def test_models_to_sections(self):
        answer = 100
        model = self.get_data_by_id(Models, 2)
        result = model.section[-1].section_relation
        assert result == answer

    def test_relations_to_tree(self):
        answer = 4
        rel = self.get_data_by_id(Relations, 1)
        result = rel.trees.kraft
        assert result == answer

    def test_relations_to_model(self):
        answer = 14
        rel = self.get_data_by_id(Relations, 6)
        result = rel.model.age
        assert result == answer

    def test_relations_to_species(self):
        answer = 11
        rel = self.get_data_by_id(Relations, 6)
        result = rel.species.age
        assert result == answer

    def test_relations_to_heights(self):
        answer = 167
        rel = self.get_data_by_id(Relations, 6)
        result = rel.height.height_tree
        assert result == answer

    def test_relations_to_crowns(self):
        answer = 125
        rel = self.get_data_by_id(Relations, 6)
        result = rel.crown.length
        assert result == answer

    def test_relations_to_plots(self):
        answer = 'В2'
        rel = self.get_data_by_id(Relations, 4)
        result = rel.plot.TLU
        assert result == answer
