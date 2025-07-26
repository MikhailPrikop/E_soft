<<<<<<< E_SOFT
### запуск приложения

#### в среде виндовс
 необходимо создать и активировать виртуальное окружение, загрузить требуемые библиотеки:
- используя в терминале команду cd укажите директорию расположения файлов приложения ;
- для создания виртуальной среды в командной строке запустите команду python -m venv .venv ;
- для установки необходимых зависимостей используйте в терминале команду pip install -r requirements.txt .
- для запуска приложения используйте команду flask --app server.py run/

### настройка подключения к базе данных

#### вариант 1
- указать в файле config.py db_URL с параметрами для подключения к базе данных
- db_URL = "postgresql://имя пользователя:пароль@localhost:номер порта/название базы данных"

####вариант 2
- для подключения к базе данных необходимо настроить переменное окружение DATABASE_URL\
- для настройки переменного окружения введите следующую команду:\
- для windows в cmd:  set DATABASE_URL=postgresql://user:password@localhost:5432/database\
- для linux в терминале: export DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase\
заменив user, password, 5432, database имеющимися (реальными) параметрами.


### cURL  запросы для тестирования

#### загрузка файла
...
curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@path_name"
...

- где path_name - полное имя загружаемого файла

#### получение списка таблиц имеющихся в  базе данных
...
http://127.0.0.1:5000/GET/data/history -X GET
...

#### очистка данных от дубликатов
...
curl http://127.0.0.1:5000/GET/data/clean -X GET -d "file"
...
- где table_name имя интересующей вас таблицы (сформировано от имени ранее загруженного файла)
- (загружаемый ранее файл filename.csv, table_name = filename)
- измененные данные в результате очистки сохраняются под новым именем (с добалением к имени таблицы префикса new_)

#### вызов аналитики
...  
curl http://127.0.0.1:5000/GET/data/stats -X GET -d "table_name|command"
...
- где table_name имя интересующей вас таблицы (сформировано по имения файла)
- (загружаемый ранее файл filename.csv, table_name = filename)
- | разделитель
- где command название команды (correlation - вызывает корреляционную матрицу, в других случаях независимо от написания вызывается описательная статистика)
- данные описательной статитистики и корреляции сохраняются в базе данных по именами c добавением префиксов statistics_ и correlation_ соответсвенно

#### вызов графиков
...  
curl http://127.0.0.1:5000/GET/data/plot -X GET -d "table_name|command"
...
- где table_name имя интересующей вас таблицы (сформировано по имения файла)
- (загружаемый ранее файл filename.csv, table_name = filename)
- | разделитель
- где command название команды (correlation - вызывает рисунок корреляционной матрицы, в других случаях независимо от написания вызывается box plot)
- данные описательной статитистики и корреляции сохраняются в базе данных по именами c добавением префиксов statistics_ и correlation_ соответсвенно


### примеры исполнения команд с выводом

### загрузка файла

##### - успешная загрузка файла
curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\file.xlsx"
{
    "1. Result": "The file was saved successfully.",
    "2. ID": 23,
    "2. Table name": "file",
    "3. Number of rows": 8,
    "4. Number of cols": 3
}
##### - отсутвие в запросе файла
...
$ curl  http://127.0.0.1:5000/POST/upload -X POST
...
Error: file not selected or file not part

##### - неверное расширение файла
...
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.txt"
...
Error: unsupported file format

##### - файл успешно загружен
...
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.csv"
...
The file was saved successfully

##### - файл пустой
curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\empty.csv"
...
Uploaded file is empty\
...

### запрос stats

#### запрос общей статистики
...

curl http://127.0.0.1:5000/GET/data/stats -X GET -d "file"
...

[
    {
        "index": "count",
        "ID name": 10.0,
        "age": 10.0,
        "salary": 10.0
    },
    {
        "index": "mean",
        "ID name": 5.5,
        "age": 36.0,
        "salary": 413772.2
    },
    {
        "index": "std",
        "ID name": 3.0276503540974917,
        "age": 9.72967967955095,
        "salary": 1078413.5449973417
    },
    {
        "index": "min",
        "ID name": 1.0,
        "age": 23.0,
        "salary": 345.0
    },
    {
        "index": "25%",
        "ID name": 3.25,
        "age": 32.5,
        "salary": 845.0
    },
    {
        "index": "50%",
        "ID name": 5.5,
        "age": 34.0,
        "salary": 3335.0
    },
    {
        "index": "75%",
        "ID name": 7.75,
        "age": 40.75,
        "salary": 161210.25
    },
    {
        "index": "max",
        "ID name": 10.0,
        "age": 56.0,
        "salary": 3453245.0
    }
]
#### запрос матрицы корреляции
...

curl http://127.0.0.1:5000/GET/data/stats -X GET -d "file|correlation"
[
    {
        "index": "ID name",
        "ID name": 1.0,
        "age": -0.14332990894082015,
        "salary": -0.02821630010901915
    },
    {
        "index": "age",
        "ID name": -0.14332990894082015,
        "age": 1.0,
        "salary": 0.27469454263057114
    },
    {
        "index": "salary",
        "ID name": -0.02821630010901915,
        "age": 0.27469454263057114,
        "salary": 1.0
    }
	]
	
	
### запрос clean

#### запрос clean когда дубликаты отсутствуют
...

curl http://127.0.0.1:5000/GET/data/clean -X GET -d "file"
No duplicates found in file
...


#### запрос clean при наличии дубликатов
curl http://127.0.0.1:5000/GET/data/clean -X GET -d "file"
...

Duplicates removed successfully (number = 1). Edited file saved by name ('new_file',)
...


### вызов plot
...

###№ построение матрицы корреляции
...

curl http://127.0.0.1:5000/GET/data/plot -X GET -d "file|correlation"
...

Correlation matrix file has been successfully constructed

### построение box_plot
...

curl http://127.0.0.1:5000/GET/data/plot -X GET -d "file"
...

The diagram file has been successfully built.