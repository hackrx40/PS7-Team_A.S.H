import openai
import os

openai.api_key = "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"

def get_sentiment(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Sentiment analysis of the following text:\n{text}\n",
        temperature=0.5,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    sentiment = response.choices[0].text.strip()
    return sentiment

get_sentiment("I love pizza")