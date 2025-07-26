import pandas as pd
import io
from storage import DataStorage
from model import DataFile
from model import Base
from model import Note
import sqlalchemy
from sqlalchemy import text
import model
from make_plot import make_box_plot,make_corr_matrix

# класс api исключений
class LogicException(Exception):
    pass

class DataProccessing:
    def __init__(self):
        self.storage = DataStorage()

    def requiest_proccesing(self, note: model.Note):
        query = (f'SELECT * '
                 f'FROM "{note.name}";')
        # запрос статистика
        if note.id == 1:
            result = self.stats(query, note)
        elif note.id == 2:
            result = self.clean(query, note)
        elif note.id == 3:
            result = self.plot(query, note)
        elif note.id == 4:
            data_fales = 'data_fales'
            query = (f'SELECT * '
                     f'FROM data_files;')
            result = self.info(query)
        return result

    #загрузка файлов
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

            ##формируем основную информацию о датасете
            df_info = DataFile(
                filename=table_name,
                num_rows=len(df),
                num_cols=len(df.columns))

            save_file, df_info = self.storage.save_df(df, table_name, df_info)
            if save_file == True:
                return df_info
            else:
                return 'Failed to save data'
        except Exception as ex:
            raise LogicException(f"{ex}")

    #проверка наличия в базе данных указанной таблицы
    def existence_table(self, note: model.Note):
        table_name = note.name
        query = text(
                    """SELECT EXISTS (
                           SELECT 1 
                           FROM data_files 
                           WHERE filename = :filename
                       );"""
                    )

        result_query = self.storage.execute_query(query, {'filename': table_name})
        result_query = result_query.fetchall()
        result_query= result_query[0][0] if result_query else False
        if result_query == False:
            raise LogicException(f'Table {note.name} not found.')


    # описательная статисткика
    def stats(self, query ,note:model.Note):
        try:
            result_query =  self.storage.execute_query(text(query))
            rows = result_query.fetchall()
            keys = result_query.keys()
            df =  pd.DataFrame(rows, columns=keys)
            df_num = df.select_dtypes(include=['number'])
            #получаем описание статистики и корреляции в зависмимости от команды
            if note.command.lower() == "correlation":
                df_stats = df_num.corr()
                new_name_table = f'correlation_{note.name}'
            else:
                df_stats = df_num.describe()
                new_name_table = f'statistics_{note.name}'

            # сохраняем новый df в базу данных
            df_info = DataFile(
                filename=new_name_table,
                num_rows=len(df_stats),
                num_cols=len(df_stats.columns))

            # сохраняем описание в базу данных
            self.storage.save_df(df_stats, new_name_table, df_info)


            # результат в список словарей
            result = df_stats.reset_index().to_dict(orient='records')
            return result
        except Exception as ex:
            raise LogicException(f"Failed to get statistics: {ex}")

    # очистка дубликатов
    def clean(self, query, note: model.Note):
        try:
            result_query = self.storage.execute_query(text(query))
            rows = result_query.fetchall()
            keys = result_query.keys()
            df = pd.DataFrame(rows, columns=keys)
            init_rows = len(df)
            df_cleaned = df.drop_duplicates()
            rows_clean = init_rows - len(df_cleaned)
            if  rows_clean == 0:
                return f'No duplicates found in {note.name}'
            else:
                new_name_table = f"new_{note.name}"
                # сохраняем новый df в базу данных
                df_info = DataFile(
                    filename=new_name_table,
                    num_rows=len(df),
                    num_cols=len(df.columns))

                self.storage.save_df(df, new_name_table, df_info)

            return (f'Duplicates removed successfully (number = {rows_clean}). '
                    f'Edited file saved by name {new_name_table,}')

        except Exception as ex:
            raise LogicException(f"Failed to get statistics: {ex}")

    # построение графиков
    def plot(self, query, note: model.Note):
        try:
            result_query =  self.storage.execute_query(text(query))
            rows = result_query.fetchall()
            keys = result_query.keys()
            df =  pd.DataFrame(rows, columns=keys)
            df_num = df.select_dtypes(include=['number'])

            # рисунок корреляционной матрицы
            if note.command.lower() == "correlation":
                make_corr_matrix(df_num, note.name)
                return f'Correlation matrix "{note.name}" has been successfully constructed'
            else:
                make_box_plot(df_num,  note.name)
                return (f'The Box plots "{note.name}" has been successfully built.')
        except Exception as ex:
            raise LogicException(f"Failed to plot the graph {ex}")

    #вызов списка таблиц
    def info(self, query):
        try:
            result_query = self.storage.execute_query(text(query))
            rows = result_query.fetchall()
            keys = result_query.keys()
            df = pd.DataFrame(rows, columns=keys)
            # результат в список словарей
            result = df.reset_index().to_dict(orient='records')
            return result
        except Exception as ex:
            raise LogicException(f"Failed to load table list: {ex}")




