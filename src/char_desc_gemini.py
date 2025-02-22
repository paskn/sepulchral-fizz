# TODO: rewrite to use gemini only
import llm
from dotenv import dotenv_values
import json
from pathlib import Path


def conf_model(model_name):
    if model_name == "gemini":
        model = llm.get_model("gemini-1.5-flash-latest")
        model.key = dotenv_values(".env")["GEMINI_API_KEY"]
        return model, "gemini"


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def prompt_novel(model, model_name, prompt, file):

    # Use attachments for Gemini
    response = model.prompt(
        prompt,
        attachments=[
            llm.Attachment(path=file),
        ],
    )
        
    return response


def get_prompt(prompt_file):
    with open(f"./_prompt/{prompt_file}", "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt


def resp_to_json(resp, novel_file, storage="./_responses"):
    responses_dir = Path(storage)
    responses_dir.mkdir(exist_ok=True)
    out_fname = responses_dir / f"{novel_file}.json"

    resp_data = {
        "file": novel_file,
        "prompt": str(resp.prompt),
        "response": resp.text(),
        "input_tokens": resp.input_tokens,
        "output_tokens": resp.output_tokens,
        "duration_ms": resp.duration_ms(),
        "datetime_utc": resp.datetime_utc(),
    }

    with out_fname.open("w", encoding="utf-8") as f:
        json.dump(resp_data, f, indent=2, ensure_ascii=False)

    print(f"Response saved to {out_fname}")


if __name__ == "__main__":
    # Get both the model and model name
    model, model_name = conf_model("gemini")
    res = prompt_novel(model,
                       model_name,
                       get_prompt("classify_chars"),
                       "./data/ourmutualfriend-2chaps.txt")
    resp_to_json(res, "friend-two-ch-test.txt")
