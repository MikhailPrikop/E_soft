from flask import Flask
from flask import request
import model

app = Flask(__name__)

# класс api исключений
class ApiException(Exception):
    pass

#список разрешенных форматов
allowed_extensions = ['csv', 'xls', 'xlsx']

#загрузка файла
@app.route('/POST/upload', methods=['POST'])
def upload_file():
    #проверка file в запросе
    if 'file' not in request.files:
        return  'Error: file not selected or not file part', 400

    file = request.files['file']
    #проверка формата файла
    if file.filename.split('.')[1] not in allowed_extensions:
        return 'Error: unsupported file format', 400
    else:
        note = model.Note()
        note.id = None
        note.filename = file.filename
        return 'The file was saved successfully'


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
