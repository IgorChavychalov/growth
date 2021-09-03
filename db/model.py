import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER, 'growth.db')

Base = declarative_base()
engine = create_engine(f'sqlite:///{PATH}', echo=False)


class Sites(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    forestry = Column(String)
    kvartal = Column(Integer)
    vydel = Column(String)
    clearcut = Column(Integer)
    planting = Column(Integer)
    thinning = Column(Integer)

    def __init__(self, forestry, kvartal, vydel, clearcut, planting, thinning):
        self.forestry = forestry
        self.kvartal = kvartal
        self.vydel = vydel
        self.clearcut = clearcut
        self.planting = planting
        self.thinning = thinning

    def __repr__(self):
        return f'{self.forestry}; {self.kvartal}; {self.vydel}; {self.clearcut}; {self.planting}; {self.thinning}'


class Plots(Base):
    __tablename__ = 'plots'

    id = Column(Integer, primary_key=True)
    id_site = Column(Integer, ForeignKey('sites.id'))
    site = relationship("Sites", backref="plot")
    relation = relationship("Relations", backref="plot")

    TLU = Column(String)
    forest_type = Column(String)
    number = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)

    def __init__(self, id_site, TLU, forest_type, number, area):
        self.id_site = id_site
        self.TLU = TLU
        self.forest_type = forest_type
        self.number = number
        self.area = area

    def __repr__(self):
        return f'{self.id_site}; {self.TLU}; {self.forest_type}; {self.number}; {self.area}'


class Taxation(Base):
    __tablename__ = 'taxation'

    id = Column(Integer, primary_key=True)
    id_site = Column(Integer, ForeignKey('sites.id'))
    site = relationship("Sites", backref="taxation")

    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    vegetation_year = Column(Integer)
    age_after_cut = Column(Integer)
    quantity_plots = Column(Integer)
    total_area = Column(Integer)
    trans_coef = Column(Float)
    diameter_med = Column(Integer)

    def __init__(self, id_site, name, date, vegetation_year, age_after_cut, quantity_plots, total_area, trans_coef, diameter_med):
        self.id_site = id_site
        self.name = name
        self.date = date
        self.vegetation_year = vegetation_year
        self.age_after_cut = age_after_cut
        self.quantity_plots = quantity_plots
        self.total_area = total_area
        self.trans_coef = trans_coef
        self.diameter_med = diameter_med

    def __repr__(self):
        return f'{self.id_site}; {self.name}; {self.date}; {self.vegetation_year}; {self.age_after_cut}; {self.quantity_plots};' \
               f' {self.total_area}; {self.trans_coef}; {self.diameter_med}'


class Species(Base):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    id_tax = Column(Integer, ForeignKey('taxation.id'))
    taxation = relationship("Taxation", backref="species")
    relation = relationship("Relations", backref="species")

    species = Column(String, nullable=False)
    age = Column(Integer)
    floor = Column(Integer)
    step_level = Column(Integer)

    def __init__(self, id_tax, species, age, floor, step_level):
        self.id_tax = id_tax
        self.species = species
        self.age = age
        self.floor = floor
        self.step_level = step_level

    def __repr__(self):
        return f'{self.id_tax}; {self.species}; {self.age}; {self.floor}; {self.step_level}'


class Trees(Base):
    __tablename__ = 'trees'

    id = Column(Integer, primary_key=True)
    id_tax = Column(Integer, ForeignKey('taxation.id'))
    id_plot = Column(Integer, ForeignKey('plots.id'))
    id_species = Column(Integer, ForeignKey('species.id'))
    taxation = relationship("Taxation", backref="tree")
    plot = relationship("Plots", backref="tree")
    species = relationship("Species", backref="tree")
    relation = relationship("Relations", backref="tree")

    number_tree = Column(Integer)
    kraft = Column(Integer)
    diameter_one = Column(Integer)
    diameter_two = Column(Integer)
    diameter_med = Column(Integer)

    def __init__(self, id_tax, id_plot, id_species, number_tree, kraft, diameter_one, diameter_two, diameter_med):
        self.id_tax = id_tax
        self.id_plot = id_plot
        self.id_species = id_species
        self.number_tree = number_tree
        self.kraft = kraft
        self.diameter_one = diameter_one
        self.diameter_two = diameter_two
        self.diameter_med = diameter_med

    def __repr__(self):
        return f'{self.id_tax}; {self.id_plot}; {self.id_species}; {self.number_tree}; {self.kraft};' \
               f' {self.diameter_one}; {self.diameter_two}; {self.diameter_med}'


class Defects(Base):
    __tablename__ = 'defects'

    id = Column(Integer, primary_key=True)
    id_tree = Column(Integer, ForeignKey('trees.id'))
    tree = relationship("Trees", backref="defect")

    info = Column(String)
    value = Column(String)
    age = Column(Integer)

    def __init__(self, id_tree, info, value, age):
        self.id_tree = id_tree
        self.info = info
        self.value = value
        self.age = age

    def __repr__(self):
        return f'{self.id_tree}; {self.info}; {self.value}; {self.age}'


class Heights(Base):
    __tablename__ = 'heights'

    id = Column(Integer, primary_key=True)
    relation = relationship("Relations", backref="height")

    diameter_med = Column(Integer)
    height_tree = Column(Integer, nullable=False)
    height_crown = Column(Integer)

    def __init__(self, diameter_med, height_tree, height_crown):
        self.diameter_med = diameter_med
        self.height_tree = height_tree
        self.height_crown = height_crown

    def __repr__(self):
        return f'{self.diameter_med}; {self.height_tree}; {self.height_crown}'


class Crowns(Base):
    __tablename__ = 'crowns'

    id = Column(Integer, primary_key=True)
    relation = relationship("Relations", backref="crown")

    length = Column(Integer)
    north = Column(Integer)
    south = Column(Integer)
    west = Column(Integer)
    east = Column(Integer)
    diameter = Column(Integer, nullable=False)
    area = Column(Integer)
    volume = Column(Integer)

    def __init__(self, length, north, south, west, east, diameter, area, volume):
        self.length = length
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.diameter = diameter
        self.area = area
        self.volume = volume

    def __repr__(self):
        return f'{self.length}; {self.north}; {self.south}; {self.west}; {self.east}; {self.diameter}; {self.area}; {self.volume}'


class Models(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    relation = relationship("Relations", backref="model")

    number = Column(Integer, nullable=False)
    age = Column(Integer)
    last_grw_length = Column(Integer)
    last_grw_age = Column(Integer)
    length_liquid = Column(Integer)
    vol_wood = Column(Float)
    vol_wood_bk = Column(Float)
    vol_bark = Column(Float)
    vol_liquid = Column(Float)

    def __init__(self, number, age, last_grw_length, last_grw_age, length_liquid, vol_wood, vol_wood_bk, vol_bark, vol_liquid):
        self.number = number
        self.age = age
        self.last_grw_length = last_grw_length
        self.last_grw_age = last_grw_age
        self.length_liquid = length_liquid
        self.vol_wood = vol_wood
        self.vol_wood_bk = vol_wood_bk
        self.vol_bark = vol_bark
        self.vol_liquid = vol_liquid

    def __repr__(self):
        return f'{self.number}; {self.age}; {self.last_grw_length}; {self.last_grw_age}; {self.length_liquid};' \
               f' {self.vol_wood}; {self.vol_wood_bk}; {self.vol_bark}; {self.vol_liquid}'


class Sections(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    id_model = Column(Integer, ForeignKey('models.id'))
    model = relationship("Models", backref="section")

    section_relation = Column(Integer, nullable=False)
    section_length = Column(Integer, nullable=False)
    bark = Column(Boolean, nullable=False)
    diameter_sw = Column(Integer, nullable=False)
    diameter_we = Column(Integer, nullable=False)
    diameter_med = Column(Integer)
    volume = Column(Float)

    def __init__(self, id_model, section_relation, section_length, bark, diameter_sw, diameter_we, diameter_med, volume):
        self.id_model = id_model
        self.section_relation = section_relation
        self.section_length = section_length
        self.bark = bark
        self.diameter_sw = diameter_sw
        self.diameter_we = diameter_we
        self.diameter_med = diameter_med
        self.volume = volume

    def __repr__(self):
        return f'{self.id_model}; {self.section_relation}; {self.section_length}; {self.bark}; {self.diameter_sw};' \
               f' {self.diameter_we}; {self.diameter_med}; {self.volume}'


class Relations(Base):
    __tablename__ = 'relations'

    id = Column(Integer, primary_key=True)
    id_tree = Column(Integer, ForeignKey('trees.id'))
    id_model = Column(Integer, ForeignKey('models.id'))
    id_species = Column(Integer, ForeignKey('species.id'))
    id_height = Column(Integer, ForeignKey('heights.id'))
    id_crown = Column(Integer, ForeignKey('crowns.id'))
    id_plot = Column(Integer, ForeignKey('plots.id'))

    kraft = Column(Integer, nullable=False)
    step = Column(Integer)

    def __init__(self, id_tree, id_model, id_species, id_height, id_crown, id_plot, kraft, step):
        self.id_tree = id_tree
        self.id_model = id_model
        self.id_species = id_species
        self.id_height = id_height
        self.id_crown = id_crown
        self.id_plot = id_plot
        self.kraft = kraft
        self.step = step

    def __repr__(self):
        return f'{self.id_tree}; {self.id_model}; {self.id_species}; {self.id_height}; {self.id_crown}; {self.id_plot};' \
               f' {self.kraft}; {self.step}'


# применим изменения
Base.metadata.create_all(engine)
