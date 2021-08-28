import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
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
    thining = Column(Integer)

    def __init__(self, forestry, kvartal, vydel, clearcut, planting, thining):
        self.forestry = forestry
        self.kvartal = kvartal
        self.vydel = vydel
        self.clearcut = clearcut
        self.planting = planting
        self.thining = thining

    def __repr__(self):
        return f'{self.forestry}; {self.kvartal}; {self.vydel}; {self.clearcut}; {self.planting}; {self.thining}'


class Plots(Base):
    __tablename__ = 'plots'

    id = Column(Integer, primary_key=True)
    id_site = Column(Integer, ForeignKey('sites.id'))
    TLU = Column(String)
    forest_type = Column(String)
    number = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)

    def __init__(self, site, TLU, forest_type, number, area):
        self.id_site = site
        self.TLU = TLU
        self.forest_type = forest_type
        self.number = number
        self.area = area

    def __repr__(self):
        return f'{self.id_site}; {self.TLU}; {self.forest_type}; {self.number}; {self.area}'


# применим изменения
Base.metadata.create_all(engine)
