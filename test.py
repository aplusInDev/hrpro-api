#!/usr/bin/env python3
""" try async view """

from flask import Flask, jsonify
import asyncio
from time import perf_counter
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

mysql_user = 'root'
mysql_pwd = 'rootroot'
mysql_host = 'localhost'
mysql_db = 'mysql'

Base = declarative_base()
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(mysql_user, mysql_pwd,
                                             mysql_host, mysql_db),
                                      pool_pre_ping=True)


class TestAsync(Base):
    __tablename__ = 'test_async'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)

@app.route('/async_test', methods=['GET'])
async def async_test():
    """ async test """
    s = perf_counter()
    # await asyncio.gather(insertion_handler())
    # await asyncio.gather(*[insertion_handler() for _ in range(1000)])
    asyncio.create_task(async_handler())
    elapsed = perf_counter() - s
    return jsonify({"time": f"{elapsed:0.2f} seconds"})

async def async_handler():
    asyncio.sleep(20)
    Session = sessionmaker(bind=engine)
    session = Session()
    new_instance = TestAsync(name="test")
    session.add(new_instance)
    session.commit()

@app.route('/sync_test', methods=['GET'])
def sync_test():
    """ async test """
    s = perf_counter()
    sync_handler()
    elapsed = perf_counter() - s
    return jsonify({"time": f"{elapsed:0.2f} seconds"})

def sync_handler():
    asyncio.sleep(20)
    Session = sessionmaker(bind=engine)
    session = Session()
    new_instance = TestAsync(name="test")
    session.add(new_instance)
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5001, debug=True)


# import asyncio

# async def count():
#     print("One")
#     await asyncio.sleep(1)
#     print("Two")

# async def count2():
#     print("One2")
#     await asyncio.sleep(1)
#     print("Two2")

# async def main():
#     await asyncio.gather(count(), count2(), count())

# if __name__ == "__main__":
#     import time
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
