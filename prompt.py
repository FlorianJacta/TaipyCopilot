import requests

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


PROMPT = """# Plot sales according to date\r\npage = \"<|{data}|chart|mode=lines|x=date|y[1]=sales|>\"\r\n# Plot sales and revenue according to date\r\npage = \"<|{data}|chart|mode=lines|x=date|y[1]=sales|y[2]=revenue|>\"\r\n# Plot sales in a blue dashed line\r\npage = \"<|{data}|chart|mode=lines|x=date|y[1]=sales|color[1]=blue|line[1]=dash|>\"\r\n# Plot sales in a blue dashed line and revenue in a red solid line\r\npage = \"<|{data}|chart|mode=lines|x=date|y[1]=sales|color[1]=blue|line[1]=dash|y[2]=revenue|color[2]=red|line[2]=solid|>\"\r\n# Plot revenue in a blue dashed line\r\npage"""


output = query(
    {
        "inputs": PROMPT,
        "parameters": {
            "return_full_text": False,
        },
    }
)

print(output[0]["generated_text"])
