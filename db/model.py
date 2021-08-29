import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker

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


# применим изменения
Base.metadata.create_all(engine)
