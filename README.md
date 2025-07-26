<<<<<<< HEAD
### настройка подключения к базе данных
- для подключения к базе данных необходимо настроить переменное окружение DATABASE_URL\
- для настройки переменного окружения введите следующую команду:\
- для windows в cmd:  set DATABASE_URL=postgresql://user:password@localhost:5432/database\
- для linux в терминале: export DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase\
заменив user, password, 5432, database имеющимися (реальными) параметрами.


### cURL  запросы для тестирования

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
$ curl  http://127.0.0.1:5000/POST/upload -X POST
Error: file not selected or file not part

##### - неверное расширение файла
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.txt"
Error: unsupported file format

##### - файл успешно загружен
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.csv"
The file was saved successfully

##### - файл пустой
curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\empty.csv"\
Uploaded file is empty\

### запрос статистика
#### запрос общей статистики
curl http://127.0.0.1:5000/GET/data/stats -X GET -d "file"
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
#### запрос корреляционной матрицы
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