import pandas as pd
import io
from storage import DataStorage
from model import DataFile
from model import Base
from model import Note
import sqlalchemy
from sqlalchemy import text

# класс api исключений
class LogicException(Exception):
    pass

class DataProccessing:
    def __init__(self):
        self.storage = DataStorage()


    def upload_file(self,file,filename):

        try:
            file = file.read()
            #проверка содержимого файлв
            if len(file) == 0:
                raise LogicException(f'Uploaded file is empty')

            #чтение файла в зависимости от разрешения
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(io.BytesIO(file))
            elif filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file))
            else:
                return f"The file could not be read"

            #создаем имя сохраняемой таблицы
            table_name = filename.split('.')[0].lower()

            ##формируем осноную информацию о датасете
            df_info = DataFile(
                filename=table_name,
                num_rows=len(df),
                num_cols=len(df.columns),
                data_summary=str(df.describe()))

            save_file, df_info = self.storage.save_df(df, table_name, df_info)
            if save_file == True:
                return df_info
            else:
                return 'Failed to save data'

        except Exception as ex:
            raise LogicException(f"{ex}")

    def existence_table(self, table_name):
        query = text(
            """SELECT EXISTS (
                   SELECT 1 
                   FROM data_files 
                   WHERE filename = :filename
               );"""
        )
        result = self.storage.execute_query(query, {'filename': table_name})
        exists = result[0][0] if result else False
        return exists



