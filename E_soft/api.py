from flask import Flask, jsonify, request, Response
import json
from io import BytesIO
from logic import DataProccessing

_data_process = DataProccessing()

app = Flask(__name__)

# класс api исключений
class ApiException(Exception):
    pass

# функция вывода в фораме json
def output_data(input_data):
    json_data = json.dumps(input_data, indent=4, ensure_ascii=False)
    return Response(json_data)

#список разрешенных форматов
allowed_extensions = ['csv', 'xls', 'xlsx']

#загрузка файла
@app.route('/POST/upload', methods=['POST'])
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
@app.route('/GET/data/stats', methods=['POST'])
def stats():
    pass

#очистка файла
@app.route('/GET/data/clean', methods=['POST'])
def clean_file():
    pass

#построение графиков
@app.route('/GET/data/plot', methods=['POST'])
def show_plot():
    pass
