from flask import Flask
from flask import request

app = Flask(_name_)

#загрузка файла
@app.route('/POST/upload', methods=['POST'])
def upload_file():
    pass

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
