# app.py
from flask import Flask, jsonify
from tasks import send_email

app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello, World!'

@app.route('/send-email/<email>')
def send_async_email(email):
	# Trigger the Celery task
	task = send_email.delay(email, 'Hello', 'This is a test email.')
	# Respond immediately without waiting for the task to complete
	return jsonify({'status': 'Email sending initiated', 'task_id': task.id})


@app.route('/check-status/<task_id>')
def check_status(task_id):
	# Check the status of the Celery task
	task = send_email.AsyncResult(task_id)
	return jsonify({'status': task.status})


@app.route('/get-result/<task_id>')
def get_result(task_id):
	# Get the result of the Celery task
	task = send_email.AsyncResult(task_id)
	return jsonify({'result': task.result})

if __name__ == '__main__':
	app.run(debug=True, port=5001)
