## cURL  запросы для тестирования

## примеры исполнения команд с выводом
### загрузка файла
#### - отсутвие в запросе файла
$ curl  http://127.0.0.1:5000/POST/upload -X POST
Error: file not selected or file not part

#### - неверное расширение файла
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.txt"
Error: unsupported file format

#### - файл успешно загружен
$ curl http://127.0.0.1:5000/POST/upload -X POST -F "file=@D:\filename.csv"
The file was saved successfully