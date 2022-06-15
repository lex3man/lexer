import redis
from sys import argv

if argv[1] == 'dev':
    red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 0)
    red_env.mset({
        'API_HOST':'dev.fountcore.tech/lexer',
        'PROJ_PATH':'/home/master/www/www.fountcore.tech/dev/lexer_v2',
        'AUTH_NAME':'lex3man',
        'AUTH_PASS':'Admin@192168'
    })
elif argv[1] == 'test':
    red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 1)
    red_env.mset({
        'API_HOST':'',
        'PROJ_PATH':'',
        'AUTH_NAME':'',
        'AUTH_PASS':''
    })
elif argv[1] == 'prod':
    red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 2)
    red_env.mset({
        'API_HOST':'',
        'PROJ_PATH':'',
        'AUTH_NAME':'',
        'AUTH_PASS':''
    })
else:
    red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True, db = 0)
    red_env.mset({
        'API_HOST':'',
        'PROJ_PATH':'',
        'AUTH_NAME':'',
        'AUTH_PASS':''
    })

print('API_HOST: ' + red_env.get('API_HOST'))
print('PROJ_PATH: ' + red_env.get('PROJ_PATH'))
print('AUTH_NAME: ' + red_env.get('AUTH_NAME'))
print('AUTH_PASS: ' + red_env.get('AUTH_PASS'))