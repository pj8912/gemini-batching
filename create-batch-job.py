"""
EXAMPLE OF SENDING & RETRIVING BATCH REQUEST VIA GEMINI API
"""

import json
from google import genai
from google.genai import types
import time


client = genai.Client()


"""
For larger sets of requests, prepare a JSON Lines (JSONL) file. Each line in this file must be a JSON object containing a user-defined key and a request object, where the request is a valid GenerateContentRequest object. The user-defined key is used in the response to indicate which output is the result of which request.

"""


# Create a sample JSONL file
with open("my-batch-requests.jsonl", "w") as f:
    requests = [
        {"key": "request-1", "request": {"contents": [{"parts": [{"text": "Describe the process of photosynthesis."}]}]}},
        {"key": "request-2", "request": {"contents": [{"parts": [{"text": "What are the main ingredients in a Margherita pizza?"}]}]}}
    ]
    for req in requests:
        f.write(json.dumps(req) + "\n")

#  ================== Upload the file to the File API ======================
uploaded_file = client.files.upload(
    file='my-batch-requests.jsonl',
    config=types.UploadFileConfig(display_name='my-batch-requests', mime_type='jsonl')
)

print(f"Uploaded file: {uploaded_file.name}")

# ==================== CREATE BATCH JOB =============================

# Assumes `uploaded_file` is the file object from the previous step
file_batch_job = client.batches.create(
    model="gemini-2.5-flash",
    src=uploaded_file.name,
    config={
        'display_name': "file-upload-job-1",
    },
)


print(f"Created batch job: {file_batch_job.name}") # get batch job name
# example : Created batch job from file: batches/123456789


# =========================== Monitoring job status ========================================
job_name  = "bacthes/123456789"

batch_job = client.batches.get(name=job_name)

completed_states = set([
    'JOB_STATE_SUCCEEDED',
    'JOB_STATE_FAILED',
    'JOB_STATE_CANCELLED',
    'JOB_STATE_EXPIRED',
])
print(f"Polling status for job: {job_name}")
batch_job = client.batches.get(name=job_name) # Initial get
while batch_job.state.name not in completed_states:
  print(f"Current state: {batch_job.state.name}")
  time.sleep(30) # Wait for 30 seconds before polling again
  batch_job = client.batches.get(name=job_name)

print(f"Job finished with state: {batch_job.state.name}")
if batch_job.state.name == 'JOB_STATE_FAILED':
    print(f"Error: {batch_job.error}")


# ============= Retrieving results ========================

if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
  # If batch job was created with a file
    if batch_job.dest and batch_job.dest.file_name:
        # Results are in a file
        result_file_name = batch_job.dest.file_name
        print(f"Results are in file: {result_file_name}")

        print("Downloading result file content...")
        file_content = client.files.download(file=result_file_name)
        # Process file_content (bytes) as needed
        print(file_content.decode('utf-8'))
    else:
        print("No results found (neither file nor inline).")
else:
    print(f"Job did not succeed. Final state: {batch_job.state.name}")
    if batch_job.error:
        print(f"Error: {batch_job.error}")

