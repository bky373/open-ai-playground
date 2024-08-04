# https://developers.upstage.ai/docs/apis/translation
import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)

stream = client.chat.completions.create(
    model="solar-1-mini-translate-koen",
    messages=[
        {
            "role": "user",
            "content": "아버지가방에들어가셨다"
        },
        {
            "role": "assistant",
            "content": "Father went into his room"
        },
        {
            "role": "user",
            "content": "엄마도들어가셨다"
        }
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Use with stream=False
# print(stream.choices[0].message.content)

##################################################
# Mom went in too
##################################################
