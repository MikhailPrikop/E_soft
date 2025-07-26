from flask import Flask, jsonify, request, Response
import json
from io import BytesIO
import model
from logic import DataProccessing

_data_process = DataProccessing()
note = model.Note()

app = Flask(__name__)

#список разрешенных форматов
allowed_extensions = ['csv', 'xls', 'xlsx']

# класс api исключений
class ApiException(Exception):
    pass

# функция вывода в фораме json
def output_data(input_data):
    json_data = json.dumps(input_data, indent=4, ensure_ascii=False)
    return Response(json_data)

#функция чтения причечания к запросу
def _from_raw(raw_note: str) -> model.Note:
    parts = raw_note.split('|')
    if len(parts) == 1:
        note = model.Note()
        note.id = None
        note.name = parts[0]
        note.command = ""
        return note
    elif len(parts) == 2:
        note = model.Note()
        note.id = None
        note.name = parts[0]
        note.command = parts[1]
        return note
    else:
        raise ApiException(f"invalid RAW note data")

#загрузка файла
@app.route('/POST/data/upload', methods=['POST'])
def upload_file():
    #проверка file в запросе
    if 'file' not in request.files:
        return  'File not selected or not file part', 400

    file = request.files['file']
    #проверка формата файла
    if file.filename.split('.')[1].lower() not in allowed_extensions:
        return 'Unsupported file format', 415
    else:
        try:
           df_info = _data_process.upload_file(file,file.filename)
           result = {"1. Result" :"The file was saved successfully.",
                     "2. ID": df_info.id,
                     "2. Table name" : df_info.filename,
                     "3. Number of rows" : df_info.num_rows,
                     "4. Number of cols" : df_info.num_cols
                     }
           return output_data(result)
        except Exception as ex:
            return f"{ex}", 400


#статистика
@app.route('/GET/data/stats', methods=['GET'])
def stats():
    data = request.get_data().decode('utf-8')
    note = _from_raw(data)
    note.id = 1
    try:
        _data_process.existence_table(note)
        result = _data_process.requiest_proccesing(note)
        return output_data(result)
    except Exception as ex:
        return f"{ex}", 400


#очистка файла
@app.route('/GET/data/clean', methods=['GET'])
def clean_file():
    data = request.get_data().decode('utf-8')
    note = _from_raw(data)
    note.id = 2
    try:
        _data_process.existence_table(note)
        result = _data_process.requiest_proccesing(note)
        return result
    except Exception as ex:
        return f"{ex}", 400

#построение графиков
@app.route('/GET/data/plot', methods=['GET'])
def show_plot():
    data = request.get_data().decode('utf-8')
    note = _from_raw(data)
    note.id = 3
    try:
        _data_process.existence_table(note)
        result = _data_process.requiest_proccesing(note)
        return result
    except Exception as ex:
        return f"{ex}", 400

#информация о имеющихся в базе данных таблицах
@app.route('/GET/data/history', methods=['GET'])
def list_table():
    data = request.get_data().decode('utf-8')
    note = _from_raw(data)
    note.id = 4
    try:
        result = _data_process.requiest_proccesing(note)
        return output_data(result)
    except Exception as ex:
        return f"{ex}", 400

