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

##### - Файл пустой
curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\empty.csv"\
Uploaded file is empty\

