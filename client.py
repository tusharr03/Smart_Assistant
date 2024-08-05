from openai import OpenAI

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in General Tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding"}
    ]
)

print(completion.choices[0].message)
