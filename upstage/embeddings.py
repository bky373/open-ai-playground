# https://developers.upstage.ai/docs/apis/embeddings
import os

import dotenv
import numpy as np
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)

query_result = client.embeddings.create(
    model="solar-embedding-1-large-query",
    input="What makes Solar LLM small yet effective?"
).data[0].embedding

document_result = client.embeddings.create(
    model="solar-embedding-1-large-passage",
    input="SOLAR 10.7B: Scaling Large Language Models with Simple yet Effective Depth Up-Scaling. DUS is simple yet "
          "effective in scaling up high performance LLMs from small ones."
).data[0].embedding

similarity = np.dot(np.array(query_result), np.array(document_result))
print(f"Similarity between query and document: {similarity}")
