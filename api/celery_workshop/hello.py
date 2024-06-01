#!/usr/bin/env python3

from celery import Celery
from time import sleep


""" important commands:
celery -A myapp worker --loglevel=info
# check if redis is running
redis-cli
# start redis-server
redis-server
"""

# app = Celery('task',
#              broker='redis://localhost:6379/0',
#              backend='db+sqlite:///results.db'
# )

# @app.task
# def say_hello(name='there'):
#     sleep(5)
#     return f'Hello {name}!'

# # say_hello.delay('world')

# result = say_hello.delay('world')
# print (result)
# print('#' * 20)
# print (dir(result))
# print('#' * 20)
# print(result.status)
# print('#' * 20)
# print(result.get())
# print('#' * 20)
