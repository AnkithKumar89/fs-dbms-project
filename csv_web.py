import csv
import shutil
from app import db
from app.models import Students
import os 
basedir = os.path.abspath('./instance/')
csv_dir = os.path.join(basedir, 'csv_files')
if not os.path.exists(csv_dir):
        print('File not found')
        exit()
for filename in os.listdir(csv_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(csv_dir, filename)
        with open(filepath) as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = Students(
                    usn=row['usn'],
                    name=row['name'],
                    age=row['age'],
                    address=row['address'],
                    phone=row['phone'],
                    email=row['email'],
                    yoa =row['yoa'], 
                    specialization = row['specialization'],
                    semester = row['semester'],
                    section=row['section'],
                    )
                db.session.add(data)
            db.session.commit()
        os.makedirs(os.path.join(basedir, 'processed_csv_files'), exist_ok=True)
        shutil.move(filepath, os.path.join(basedir, 'processed_csv_files', filename))
        print(f'Data has been imported successfully from {filename}. CSV files moved to processed_csv_files directory.')