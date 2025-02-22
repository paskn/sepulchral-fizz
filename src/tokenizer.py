from dotenv import dotenv_values
from tokenizers import Tokenizer

from char_desc_gemma import read_text_file, get_instruction, construct_promt

hf_key = dotenv_values(".env")["hugging_face_auth"]

def count_tokens(doc, hf_key=hf_key):
    tokenizer = Tokenizer.from_pretrained("google/gemma-2-9b", token=hf_key)
    doc_encoded = tokenizer.encode(doc)
    return len(doc_encoded.ids)

if __name__ == "__main__":
    # doc = construct_promt(get_instruction("classify_chars"),
                          # read_text_file("./data/ourmutualfriend-2chaps.txt"))
    # doc = read_text_file("./_responses/test.txt")
    doc = """<|im_start|>system
<|im_end|>
<|im_start|>user
<|im_end|>
<|im_start|>assistant"""
    print(count_tokens(doc))
    
