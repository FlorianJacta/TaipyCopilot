from taipy import Gui

import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": "Bearer ENTER YOUR API KEY HERE"}

DATA_PATH = "data.csv"

df = pd.read_csv(DATA_PATH, sep=";")
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


def query(payload: dict) -> dict:
    """
    Queries StarCoder API

    Args:
        payload: Payload for StarCoder API

    Returns:
        dict: StarCoder API response
    """
    response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
    return response.json()


def prompt(input_instruction: str) -> str:
    """
    Prompts StarCoder to generate Taipy GUI code

    Args:
        instuction (str): Instruction for StarCoder

    Returns:
        str: Taipy GUI code
    """
    current_prompt = f"{context}\n{input_instruction}\n"
    output = ""
    final_result = ""

    # Re-query until the output contains the closing tag
    timeout = 0
    while ">" not in output and timeout < 10:
        output = query(
            {
                "inputs": current_prompt + output,
                "parameters": {
                    "return_full_text": False,
                },
            }
        )[0]["generated_text"]
        timeout += 1
        final_result += output

    output_code = f"""<{final_result.split("<")[1].split(">")[0]}>"""
    return output_code


def on_enter_press(state) -> None:
    """
    Prompt StarCoder to generate Taipy GUI code when user presses enter

    Args:
        state (State): Taipy GUI state
    """
    state.result = prompt(state.instruction)
    state.p.update_content(state, state.result)
    print(state.result)


instruction = ""
result = ""


page = """
# Taipy**Copilot**{: .color-primary}

Enter your instruction here:
<|{instruction}|input|on_action=on_enter_press|class_name=fullwidth|>

<|Data|expandable|
<|{data}|table|width=100%|>
|>

<|part|partial={p}|>
"""

gui = Gui(page)
p = gui.add_partial("""<|{data}|chart|mode=lines|x=Date|y=Sales|>""")
gui.run()
