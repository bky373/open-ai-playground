# https://cookbook.openai.com/examples/batch_processing

import json

import dotenv
from openai import OpenAI
import pandas as pd
from IPython.display import Image, display

dotenv.load_dotenv()

client = OpenAI()

dataset_path = "data/imdb_top_1000.csv"

df = pd.read_csv(dataset_path)
print(df.head())

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
for _, row in df[:5].iterrows():
    description = row['Overview']
    title = row['Series_Title']
    result = get_categories(description)
    print(f"TITLE: {title}\nOVERVIEW: {description}\n\nRESULT: {result}")
    print("\n\n----------------------------\n\n")
