from flask import Flask ,request, jsonify
import os
from werkzeug.utils import secure_filename
from flask import Flask
from celery import Celery
import uuid
import sqlite3

app = Flask(__name__)
simple_app = Celery('simple_worker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

conn = sqlite3.connect('application.db', check_same_thread=False)
c = conn.cursor()

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        app.logger.info("Invoking Method ")

        if request.method=="POST":

            if 'file' not in request.files:
                return "No file part"

            file = request.files['file']
            filename = secure_filename(file.filename)
            task_id = str(uuid.uuid4())

            if (filename.split(".")[-1] != "csv"):
                return "File format is not supported. Please upload a csv file."

            filename = filename.split(".")[0] + "_" + task_id + "." + filename.split(".")[1]

            isExist = os.path.exists("./uploads")
            if(isExist==False):
                os.makedirs("./uploads")

            file.save(os.path.join("./uploads/", filename))

            r = simple_app.send_task('tasks.longtime_add', kwargs={'filename':'./uploads/'+filename},task_id=task_id)
            app.logger.info(r.backend)
            return r.id
        else:
            return "get"
    except Exception as e:
        app.logger.error("Error in upload_file method : " + str(e))
        return "Error in upload_file method : " + str(e)
    
@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    try:
        print("Invoking Method ")
        status = simple_app.AsyncResult(task_id, app=simple_app)

        if status.state == 'PENDING':
            return "Task is pending"
        if status.state == 'FAILURE':
            return "Task failed"
        
        c.execute('''
            SELECT processedFilePath FROM files_path WHERE taskId=?
        ''', (task_id,))  

        result_url = c.fetchone()

        conn.commit()

        if result_url:
            print(result_url)
            return jsonify({'processedFilePath': result_url[0]})
        else:
            return "No result found for the given task_id"

    except Exception as e:
        app.logger.error("Error in get_status method: " + str(e))
        return "Error in get_status method: " + str(e)