from google import genai

client = genai.Client()

# Delete a batch job
client.batches.delete(name=batch_job_to_delete.name)
