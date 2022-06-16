import redis, os
from sys import argv

try:
    with open('lexer.ini', 'x') as inifile:
        inifile.write('[uwsgi]')
    try:
        for my_arg in argv:
            if my_arg == '-case':

                # Проверка аргумента для определения среды развертывания ('dev', 'test', 'prod')
                match argv[argv.index(my_arg) + 1]:

                # Параметры среды для РАЗРАБОТКИ
                    case 'dev':
                        red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 0)
                        red_env.mset({
                            'API_HOST':'dev.fountcore.tech/lexer',
                            'PROJ_PATH':'/home/master/www/www.fountcore.tech/dev/lexer_v2',
                            'AUTH_NAME':'lex3man',
                            'AUTH_PASS':'Admin@192168'
                        })
                        with open('lexer.ini', 'a') as inifile:
                            inifile.write('''
env = STATE=dev
env = API_HOST=dev.fountcore.tech/lexer
socket = 0.0.0.0:5000
protocol = http''')

                # Параметры среды для АЛЬФАТЕСТИРОВАНИЕ
                    case 'test':
                        red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 1)
                        red_env.mset({
                            'API_HOST':'alpha.lexer.fountcore.tech',
                            'PROJ_PATH':'',
                            'AUTH_NAME':'',
                            'AUTH_PASS':''
                        })
                        with open('lexer.ini', 'a') as inifile:
                            inifile.write('''
env = STATE=test
env = API_HOST=alpha.lexer.fountcore.tech
socket = /run/lexer.sock''')

                # Параметры среды для ПРОДАКШНА
                    case 'prod':
                        red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 2)
                        red_env.mset({
                            'API_HOST':'lexer.fountcore.tech',
                            'PROJ_PATH':'',
                            'AUTH_NAME':'',
                            'AUTH_PASS':''
                        })
                        with open('lexer.ini', 'a') as inifile:
                            inifile.write('''
env = STATE=prod
env = API_HOST=lexer.fountcore.tech
socket = /run/lexer.sock''')
                
                with open('lexer.ini', 'a') as inifile:
                    inifile.write('''
strict = true
module = wsgi:app
master = true
uid = master
gid = master
processes = 5
enable-threads = true
need-app = true
chmod-socket = 660
vacuum = true
die-on-term = true
virtualenv = ../server
max-requests = 1000                  ; Перезапуск workers после указанного количества запросов
max-worker-lifetime = 3600           ; Перезапуск workers после указанного времени в сек
reload-on-rss = 512                 ; Перезапуск workers после потребления указанного количества памяти
worker-reload-mercy = 60             ; Время ожидания перед уничтожение процессов workers
cheaper-algo = busyness              
processes = 500                      ; Максимально допустимое количество workers
cheaper = 8                          ; Минимально допустимое количество workers
cheaper-initial = 16                 ; workers, созданные при запуске
cheaper-overload = 1                 ; Продолжительность цикла в секундах
cheaper-step = 16                    ; Сколько workers на spawn за один раз

cheaper-busyness-multiplier = 30     ; Сколько циклов ждать, прежде чем убивать workers
cheaper-busyness-min = 20            ; Ниже этого порога убивает workers (если стабильно для множителя циклов)
cheaper-busyness-max = 70            ; Выше этого порога порождаются новые workers
cheaper-busyness-backlog-alert = 16  ; Порождает аварийных workers, если в очереди ожидает больше этого количества запросов 
cheaper-busyness-backlog-step = 2    ; Сколько аварийных workers будет создано, если в очереди слишком много запросов''')

                print('API_HOST: ' + red_env.get('API_HOST'))
                print('PROJ_PATH: ' + red_env.get('PROJ_PATH'))
                print('AUTH_NAME: ' + red_env.get('AUTH_NAME'))
                print('AUTH_PASS: ' + red_env.get('AUTH_PASS'))

    except: 
        print("Используй флаг '-case' для проверки аргумента среды развертывания ('dev', 'test', 'prod')")
        os.remove('lexer.ini')
except: 
    print('Среда уже сконфигурирована. Для новой конфигурации удалите файл lexer.ini')