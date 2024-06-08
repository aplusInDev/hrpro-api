from api.celery_app import app
from time import sleep


@app.task
def test_task():
    sleep(20)
    print("Task 2 start")
    # calling test_task2
    test_task2.delay()
    print("Task 1 completed")
    return "Task 1 completed"

@app.task
def test_task2():
    sleep(2)
    print("Task 2 completed")
    return "Task 2 completed"
