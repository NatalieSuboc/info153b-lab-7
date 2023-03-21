from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery.result import AsyncResult
from worker import count_word_task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/tasks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/count', methods=['POST'])
def count():
    text = request.get_json().get('text')
    if not text:
        return jsonify({ "error": "json body does not contain text field or text field is empty"})
    # add to async task queue
    count_async_task = count_word_task.delay(text)
    task_id = count_async_task.id
    # returns: job ID
    return task_id

@app.route('/status/<id>', methods=['GET'])
def get_status(id):
    # async result - takes in job id -> finds result 
    result = count_word_task.AsyncResult(id)
    if not result:
        return jsonify({ "error": "task id not found"})
    return result.status
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)