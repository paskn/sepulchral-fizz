import llm
import json
from pathlib import Path
from datetime import datetime


def conf_model(model_name):
    if model_name == "gemma":
        model = llm.get_model("gemma2:latest")
        return model, "gemma"
    else:
        raise ValueError(f"Unsupported model: {model_name}")


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def chunk_text(text, chunk_size=8000):
    """Split text into chunks of approximately chunk_size characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks


def structure_llama_prompt(instruction_prompt,
                           text_content,
                           chunk_num=None,
                           total_chunks=None):
    """Structure the prompt while preserving the original formatting requirements."""
    chunk_info = ""
    if chunk_num is not None:
        chunk_info = f"\n\n[Processing part {chunk_num} of {total_chunks}]"
    
    return f"""{instruction_prompt}{chunk_info}

TEXT TO ANALYZE:
{text_content}

REMEMBER: Output only in format: Name | Age Group | Gender
"""


def safe_get_metadata(response, attr):
    """Safely get metadata from response object."""
    try:
        value = getattr(response, attr)
        if callable(value):
            return value()
        return value
    except (AttributeError, TypeError):
        return None


def prompt_novel(model, model_name, prompt, file):
    if model_name == "gemini":
        response = model.prompt(
            prompt,
            attachments=[
                llm.Attachment(path=file),
            ],
        )
        return response
    else:
        text_content = read_text_file(file)
        print(f"Total text length: {len(text_content)} characters")
        
        # Split into chunks
        chunks = chunk_text(text_content)
        print(f"Split into {len(chunks)} chunks")
        
        all_responses = []
        all_texts = []
        for i, chunk in enumerate(chunks, 1):
            print(f"\nProcessing chunk {i}/{len(chunks)}")
            combined_prompt = structure_llama_prompt(prompt, chunk, i, len(chunks))
            response = model.prompt(combined_prompt)
            all_responses.append(response)
            all_texts.append(response.text())
            print(f"Chunk {i} response:")
            print(response.text())
        
        # Create a combined response dictionary with safe metadata handling
        combined_text = "\n".join(all_texts)
        
        response_data = {
            "prompt": combined_prompt,
            "text": combined_text,
            "input_tokens": None,  # Set to None since we can't reliably combine these
            "output_tokens": None,
            "duration_ms": None,
            "datetime_utc": datetime.utcnow().isoformat()
        }
        
        return response_data


def get_prompt(prompt_file):
    with open(f"./_prompt/{prompt_file}", "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt


def resp_to_json(resp, novel_file, storage="./_responses"):
    responses_dir = Path(storage)
    responses_dir.mkdir(exist_ok=True)
    out_fname = responses_dir / f"{novel_file}.json"

    if isinstance(resp, dict):
        resp_data = resp
    else:
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
    
    print("\nFinal Response:")
    print(resp_data["text"] if isinstance(resp, dict) else resp.text())
    print(f"\nResponse saved to {out_fname}")


if __name__ == "__main__":
    model, model_name = conf_model("gemma")
    novel = "ourmutualfriend-2chaps.txt"
    res = prompt_novel(model,
                      model_name,
                      get_prompt("classify_chars-llama"),
                       novel)
    resp_to_json(res, novel)
