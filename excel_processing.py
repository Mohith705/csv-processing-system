import pandas as pd
import sqlite3
from image_processing import download_and_compress_image
from s3_uploads import upload_file_from_device

conn = sqlite3.connect('application.db', check_same_thread=False)
c = conn.cursor()

def upload_data(task_id, s_no, product_name, image_url, a):
    try:
        print("Inserting data")
        compress_status = download_and_compress_image(image_url, "./temp/test.png", 50)

        if not compress_status:
            return None
        
        file_url = upload_file_from_device("./temp/test.png", "mahesh-mens-touch", f"{task_id}/{s_no}/{product_name}/{a}.png")

        if file_url is None:
            return None 
        
        c.execute('''
            INSERT INTO images(taskId, originalUrl, processedUrl, sNo, productName) VALUES(?, ?, ?, ?, ?)
        ''', (task_id, image_url, file_url, s_no, product_name))
        conn.commit()

        print("Data inserted successfully")
        return file_url
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_csv(file_path, task_id, output_csv_path):
    try:
        df = pd.read_csv(file_path)

        if "S. No." not in df.columns:
            return "S.No column not found in the CSV file."
        elif "Product Name" not in df.columns:
            return "Product Name column not found in the CSV file."
        elif "Input Image Urls" not in df.columns:
            return "Product Images column not found in the CSV file."

        df['Processed Image URLs'] = ""

        list_df = df.values.tolist()

        for i in list_df:
            s_no = i[0]
            product_name = i[1]
            product_images = i[2].split(",")

            processed_urls = []
            a = 0
            for j in product_images:
                processed_url = upload_data(task_id, s_no, product_name, j, a)
                if processed_url:
                    processed_urls.append(processed_url)
                a += 1
            
            df.loc[df['S. No.'] == s_no, 'Processed Image URLs'] = ",".join(processed_urls)

        df.to_csv(output_csv_path, index=False)
        print(f"Updated CSV file has been created successfully at {output_csv_path}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
