import llm
import json
from pathlib import Path


def conf_model(model_name):
    if model_name == "gemma":
        model = llm.get_model("gguf/gemma-2-9b-it-Q4_K_M")
        return model, "gemma"


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def prompt_novel(model, prompt):
    # response = model.prompt(prompt, num_ctx=8192)
    response = model.prompt(prompt)
        
    return response


def get_instruction(prompt_file):
    with open(f"./_prompt/{prompt_file}", "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt


def construct_promt(instruction, attachment):
    prompt = f"{instruction}\n{attachment}"
    return prompt


def safe_get_metadata(response, attr):
    """Safely get metadata from response object."""
    try:
        value = getattr(response, attr)
        if callable(value):
            return value()
        return value
    except (AttributeError, TypeError):
        return None


def resp_to_json(resp, novel_file, storage="./_responses"):
    responses_dir = Path(storage)
    responses_dir.mkdir(exist_ok=True)
    out_fname = responses_dir / f"{novel_file}.json"

    resp_data = {
        "file": novel_file,
        "prompt": str(resp.prompt),
        "response": resp.text(),
        "input_tokens": safe_get_metadata(resp, 'input_tokens'),
        "output_tokens": safe_get_metadata(resp, 'output_tokens'),
        "duration_ms": safe_get_metadata(resp, 'duration_ms'),
        "datetime_utc": safe_get_metadata(resp, 'datetime_utc')
    }

    with out_fname.open("w", encoding="utf-8") as f:
        json.dump(resp_data, f, indent=2, ensure_ascii=False)

    print(f"Response saved to {out_fname}")


if __name__ == "__main__":
    # Get both the model and model name
    model, model_name = conf_model("gemma")
    prompt = construct_promt(get_instruction("classify_chars"),
                             read_text_file("./data/mutual-friend-small.txt"))
    res = prompt_novel(model,                       
                       prompt)
    resp_to_json(res, "friend-two-ch-gemma-test.txt")
