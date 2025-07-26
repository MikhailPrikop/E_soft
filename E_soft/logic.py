import pandas as pd
import io
from storage import DataStorage
from model import DataFile
from model import Base
from model import Note
import sqlalchemy
from sqlalchemy import text
import model

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

    #проверка наличия в базе данных указанной таблицы
    def existence_table(self, table_name):
        query = text(
                    """SELECT EXISTS (
                           SELECT 1 
                           FROM data_files 
                           WHERE filename = :filename
                       );"""
                    )
        try:
            result_query = self.storage.execute_query(query, {'filename': table_name})
            result_query = result_query.fetchall()
            result_query= result_query[0][0] if result_query else False
            return result_query
        except Exception as ex:
            raise LogicException(f'Table {note.name} not found. {ex}')

    def requiest_proccesing(self, note: model.Note):
        #запрос статистика
        if note.id == 1:
            query = (f'SELECT * '
                     f'FROM "{note.name}";'
                     )
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
                    # сохраняем описание в базу данных
                    new_name_table = f'statistics_{note.name}'

                # сохраняем описание в базу данных
                df_stats.to_sql(new_name_table,
                                       con=self.storage.engine,
                                       if_exists='replace',
                                        index=False)


                # результат в список словврей
                result = df_stats.reset_index().to_dict(orient='records')
                return result

            except Exception as ex:
                raise LogicException(f"Failed to get statistics: {ex}")

