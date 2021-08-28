from pytest import raises
import sqlalchemy.orm
from db.model import Base, Site


class TestBase:
    def setup(self):
        # Создаём суслика
        engine = sqlalchemy.create_engine(f'sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)  # импорт структуры БД
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()
        # Создаём параметры
        self.session = session
        # Запись в таблие User для тестов
        site1 = Site(forestry='Сяськое',
                     kvartal='184',
                     vydel='10',
                     clearcut=2000,
                     planting=2001,
                     thining=2010)
        self.session.add_all([site1])

    def test_exist_data_site_table(self):
        result = self.session.query(Site).all()[0].__repr__()
        answer = 'Сяськое; 184; 10; 2000; 2001; 2010'
        # Логин уникальный
        assert result == answer
