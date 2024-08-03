# https://cookbook.openai.com/examples/batch_processing

import json

import dotenv
from openai import OpenAI
import pandas as pd

# from IPython.display import Image, display

dotenv.load_dotenv()

client = OpenAI()

# dataset_path = "data/imdb_top_1000.csv"
dataset_path = "data/imdb_top_10.csv"

df = pd.read_csv(dataset_path)
# print(df.head())

############################################################
categorize_system_prompt = '''
Your goal is to extract movie categories from movie descriptions, as well as a 1-sentence summary for these movies.
You will be provided with a movie description, and you will output a json object containing the following information:

{
    categories: string[] // Array of categories based on the movie description,
    summary: string // 1-sentence summary of the movie based on the movie description
}

Categories refer to the genre or type of the movie, like "action", "romance", "comedy", etc. Keep category names simple and use only lower case letters.
Movies can have several categories, but try to keep it under 3-4. Only mention the categories that are the most obvious based on the description.
'''


def get_categories(description):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        # This is to enable JSON mode, making sure responses are valid json objects
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": categorize_system_prompt
            },
            {
                "role": "user",
                "content": description
            }
        ],
    )

    return response.choices[0].message.content


# Testing on a few examples
# for _, row in df[:5].iterrows():
#     description = row['Overview']
#     title = row['Series_Title']
#     result = get_categories(description)
#     print(f"TITLE: {title}\nOVERVIEW: {description}\n\nRESULT: {result}")
#     print("\n\n----------------------------\n\n")

############################################################
# Creating an array of json tasks

tasks = []

for index, row in df.iterrows():
    description = row['Overview']

    task = {
        "custom_id": f"task-{index}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "temperature": 0.1,
            "response_format": {
                "type": "json_object"
            },
            "messages": [
                {
                    "role": "system",
                    "content": categorize_system_prompt
                },
                {
                    "role": "user",
                    "content": description
                }
            ],
        }
    }

    tasks.append(task)

############################################################
# Creating the file

file_name = "data/batch_tasks_movies.jsonl"

with open(file_name, 'w') as file:
    for obj in tasks:
        file.write(json.dumps(obj) + '\n')

############################################################
# Uploading the file
batch_file = client.files.create(
    file=open(file_name, "rb"),
    purpose="batch"
)
print(batch_file)
# FileObject(id='file-veuFAsHCFuXgoYVYyo94zGMJ', bytes=11216, created_at=1722699373, filename='batch_tasks_movies.jsonl', object='file', purpose='batch', status='processed', status_details=None)

############################################################
# Creating the batch job
batch_job = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

############################################################
# Checking batch status
batch_job_id = batch_job.id
batch_job_id = 'batch_kLGaMWz14MPhSjcPiGCVtjil'
batch_job = client.batches.retrieve(batch_job_id)
print(batch_job)
# Batch(id='batch_kLGaMWz14MPhSjcPiGCVtjil', completion_window='24h', created_at=1722699374, endpoint='/v1/chat/completions', input_file_id='file-veuFAsHCFuXgoYVYyo94zGMJ', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1722785774, failed_at=None, finalizing_at=None, in_progress_at=None, metadata=None, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))

############################################################
# Retrieving results
# result_file_id = batch_job.output_file_id
result_file_id = 'file-ubefvmXWcZX2QCrJG23yAsN2'
print(f'result_file_id: {result_file_id}')

result = client.files.content(result_file_id).content

result_file_name = "data/batch_job_results_movies.jsonl"

with open(result_file_name, 'wb') as file:
    file.write(result)

############################################################
# Loading data from saved file
results = []
with open(result_file_name, 'r') as file:
    for line in file:
        # Parsing the JSON string into a dict and appending to the list of results
        json_object = json.loads(line.strip())
        results.append(json_object)

############################################################
# Reading only the first results
for res in results[:5]:
    task_id = res['custom_id']
    # Getting index from task id
    index = task_id.split('-')[-1]
    result = res['response']['body']['choices'][0]['message']['content']
    movie = df.iloc[int(index)]
    description = movie['Overview']
    title = movie['Series_Title']
    print(f"TITLE: {title}\nOVERVIEW: {description}\n\nRESULT: {result}")
    print("\n\n----------------------------\n\n")
