from taipy import Gui

import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": "Bearer ENTER YOU API KEY HERE"}

DATA_PATH = "data.csv"

df = pd.read_csv(DATA_PATH, sep="\t")
data = pd.DataFrame(
    {
        "Date": pd.to_datetime(
            [
                "2020-01-01",
                "2020-01-02",
                "2020-01-03",
                "2020-01-04",
                "2020-01-05",
                "2020-01-06",
                "2020-01-07",
            ]
        ),
        "Sales": [100, 250, 500, 400, 450, 600, 650],
        "Revenue": [150, 200, 600, 800, 850, 900, 950],
    }
)
context = ""
for instruction, code in zip(df["instruction"], df["code"]):
    context += f"{instruction}\n{code}\n"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def prompt(instruction: str) -> str:
    """
    Prompts StarCoder to generate Taipy GUI code

    Args:
        instuction (str): Instruction for StarCoder

    Returns:
        str: Taipy GUI code
    """
    prompt = f"{context}\n{instruction}\n"
    output = ""
    result = ""

    timeout = 0
    while ">" not in output and timeout < 10:
        output = query(
            {
                "inputs": prompt + output,
                "parameters": {
                    "return_full_text": False,
                },
            }
        )[0]["generated_text"]
        timeout += 1
        result += output

    code = f"""<{result.split("<")[1].split(">")[0]}>"""
    return code


def on_button_action(state):
    state.result = prompt(state.instruction)
    state.p.update_content(state, state.result)
    print(state.result)


instruction = ""
result = ""


page = """
Enter your instruction here:
<|{instruction}|input|on_action=on_button_action|class_name=fullwidth|>

<|Data|expandable|
<|{data}|table|width=100%|>
|>

<|part|partial={p}|>
"""

gui = Gui(page)
p = gui.add_partial("""<|{data}|chart|mode=lines|x=Date|y=Sales|>""")
gui.run()
