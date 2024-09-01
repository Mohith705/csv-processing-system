import sqlite3

conn = sqlite3.connect('application.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS files_path(
        taskId TEXT NOT NULL UNIQUE,
        originalFilePath TEXT,
        processedFilePath TEXT,
        status TEXT
    )
''')
conn.commit()

def create_file_entry(task_id, original_file_path, status):
    try:
        c.execute('''
            INSERT INTO files_path (taskId, originalFilePath, status)
            VALUES (?, ?, ?)
        ''', (task_id, original_file_path, status))
        conn.commit()
        return "Entry created successfully"
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()


def update_file_entry(task_id, processed_file_path, status):
    try:
        c.execute('''
            UPDATE files_path
            SET processedFilePath = ?, status = ?
            WHERE taskId = ?
        ''', (processed_file_path, status, task_id))
        conn.commit()
        return "Entry updated successfully"
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
