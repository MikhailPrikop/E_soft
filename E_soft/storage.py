import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

from model import DataFile, Base
import config

db_URL = config.db_URL
class StorageException(Exception):
    pass

class DataStorage:
    def __init__(self, db_url=None):
        self.db_url = db_URL or os.getenv('DATABASE_URL')
        self.engine = None
        self.session = None
    # подключениt
    def connect(self):
        if self.db_url is None:
            raise StorageException("Environment variable 'DATABASE_URL' is not set!")
        try:
            self.engine = create_engine(self.db_url)
            # Создаем таблицы, если их еще нет
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            # проверка соединения
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 2"))
        except Exception as ex:
            raise StorageException(f"Connection error: {ex}")
    # закрытие сессии
    def close(self):
        if self.session:
            self.session.close()

    def save_df(self, df, table_name, df_info)-> DataFile:
        # соединяемся с базой данных
        self.connect()
        try:
            # сохранение датафрейма
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)

            self.session.add(df_info)
            self.session.commit()
            self.session.refresh(df_info)
            return True, df_info
        except Exception as ex:
            self.session.rollback()
            raise StorageException(f"Error during save: {ex}")
        finally:
            self.close()


    # выполнение запросов
    def execute_query(self, query, params=None):
        self.connect()
        try:
            if params:
                result = self.session.execute(query, params)
            else:
                result = self.session.execute(query)
            return result
        except Exception as ex:
            raise StorageException(f"Error executing request: {ex}")








