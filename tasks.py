from celery import Celery
import os
from db_tasks import create_file_entry,update_file_entry
from celery.utils.log import get_task_logger
from excel_processing import process_csv
from s3_uploads import upload_file_from_device

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task(bind=True)
def longtime_add(self, filename):
    try:
        isExist = os.path.exists(filename)

        if not isExist:
            logger.error("File not found")
            return "File not found"
        
        task_id = self.request.id
        
        create_file_entry(task_id, filename, "processing")

        result = process_csv(filename, task_id, "./temp/updated_data_with_processed_urls.csv")

        if result != True:
            update_file_entry(task_id, filename, "failed")
            return result
        
        result1 = upload_file_from_device("./temp/updated_data_with_processed_urls.csv", "mahesh-mens-touch", f"{task_id}.csv")

        if result1 is None:
            update_file_entry(task_id, filename, "failed")
            return "Error in uploading file to S3"
        
        update_file_entry(task_id, result1, "processed")
        
        return result1
    except Exception as e:
        logger.error("Error in longtime_add method: " + str(e))
        return "Error in longtime_add method: " + str(e)
