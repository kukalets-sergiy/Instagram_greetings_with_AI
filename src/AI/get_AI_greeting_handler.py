from openai import OpenAI
import os
from dotenv import load_dotenv

"""
This function takes an AI description of an image and sends it to the OpenAI API to generate a greeting message.

The message is then returned to the caller.

The function will print the response from the OpenAI API to the console for debugging purposes.
"""

load_dotenv()
ai_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=ai_key)


def get_AI_greeting_handler(ai_description: str):
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": f"{ai_description} Given the preceding information, create a greeting message."
                                     f"Please analyze the context and craft a appropriate opening message. For example,"
                                     f"if the conversation is about a person with a Dalmatian, the first message could"
                                     f"be: 'Wow, I love Dalmatians, what's his name?' What is a suitable greeting"
                                     f"message for a similar scenario?"},
          ],
        }
      ],
      max_tokens=300,
    )

    print(response.choices[0])
    print(response)
    return response.choices[0].message.content

