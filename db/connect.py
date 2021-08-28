import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import PATH


class Connect:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connect, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        # создадим подключение к базе
        engine = create_engine(f'sqlite:///{PATH}')
        # создадим сессию для базы
        self.session = sessionmaker(bind=engine)()

    def get_session(self):
        return self.session
