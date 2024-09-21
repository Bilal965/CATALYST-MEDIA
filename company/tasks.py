from celery import shared_task
from .models import Company
import csv
import io

@shared_task
def process_csv(file_content):
    for chunk in file_content.chunks():
            text_file = io.StringIO(chunk.decode('utf-8'))
            reader = csv.reader(text_file)
            next(reader)  # Skip header row
            for row in reader:
                Company.objects.bulk_create(
                    name=row[0],
                    founded_year=int(row[1]),
                    industry=row[2],
                    country=row[3],
                    domain=row[4],
                    linkedin_url=row[5],
                    locality=row[6],
                    current_employee_estimate=int(row[7]),
                    total_employee_estimate=int(row[8]),
                )
            return "File processed successfully!"
