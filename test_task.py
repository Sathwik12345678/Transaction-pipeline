from app.worker.tasks import process_job
result = process_job.delay(1)
print("Task ID:", result.id)