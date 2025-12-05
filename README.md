# Gemini Batching



Files: 
- `data.jsonl`: Our json data file
- `req.py` : Request file
- `res.py` : Resopnse file
---

The Gemini Batch API is designed to process large volumes of requests asynchronously at 50% of the standard cost. The target turnaround time is 24 hours, but in majority of cases, it is much quicker.


- Creating a batch job
  - Input File<br>
      A JSON Lines (JSONL) file where each line contains a complete GenerateContentRequest object. This method is recommended for larger requests. The output returned from the model is a JSONL file where each line is either a GenerateContentResponse or a status object.
    
- Retrieving results
  - Response
  - Cancelling a batch job
  - deleting a batch job


Input File
- For larger datasets
- prepare a JSONL file
- Each line must be a **user-defined key** and a *request object*

```jsonl
{"key": "request-1", "request": {"contents": [{"parts": [{"text": "Describe the process of photosynthesis."}]}], "generation_config": {"temperature": 0.7}}}
{"key": "request-2", "request": {"contents": [{"parts": [{"text": "What are the main ingredients in a Margherita pizza?"}]}]}}
```
