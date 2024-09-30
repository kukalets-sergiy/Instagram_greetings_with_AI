from openai import OpenAI
import os
from dotenv import load_dotenv

"""
This function takes an image source URL and asks the GPT-4O-MINI model to describe what is in the image.
It returns the description as a string.
"""

load_dotenv()
ai_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=ai_key)


def get_image_description(image_source: str):
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": image_source,
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )

    print(response.choices[0])
    print(response)
    return response.choices[0].message.content

