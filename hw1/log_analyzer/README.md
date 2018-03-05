# Log Analyzer
# (Otus-Python-2018-02 Homework)

## Общее описание

Утилита для анализа логов веб-сервера Nginx, основной задачей которой является выявление наиболее долго загружающихся URL-ов. 

## Запуск утилиты
Утилита запускается из командной строки и может принимать параметр --config, указывающий на местоположение конфигурационного файла, например:
```
log_anlyzer.py --config "/tmp/config.file"
```

## Конфигурационный файл

Конфигурационный файл должен содержать данные в формате json. Пример правильно оформленного конфигурационного файла
```
{
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TS_FILE": "./tmp/log_analyzer.ts"
}
```

### Параметры конфигурационного файла

Конфигурационный файл может (но не обязан) содержать следующие параметры:
REPORT_SIZE - количество включаемых в отчёт записей (наиболее "медленных" url-ов)
REPORT_DIR - директория в которую будет записан отчёт (ожидается имя логов в формате nginx-access-ui.log-YYYYMMDD, анализируется самый последний по YYYYMMDD) 
LOG_DIR - директория в которой утилита будет искать файлы логов для последующего анализа
SELF_LOG_FILE - путь до лог-файла создаваемого утилитой
TS_FILE - путь до файла с временной меткой, указывающей на последний успешный запуск утилиты
REPORT_TEMPLATE - путь до файла c HTML-шаблоном генерируемого отчёта

## Unit-тесты
Unit-тесты запускаются при помощи команды:
```
test_log_anlyzer.py
```