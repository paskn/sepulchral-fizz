import os
import gutenbergpy.textget

def fetch_by_id(id):
    # This gets a book by its gutenberg id number
    raw_book = gutenbergpy.textget.get_text_by_id(id) # with headers
    clean_book = gutenbergpy.textget.strip_headers(raw_book) # without headers
    return clean_book, raw_book

if __name__ == '__main__':
    save_path = "./data/novels/"
    dickens_friend = 883        # id from https://www.gutenberg.org/ebooks/883
    cleaned_book, raw_book = fetch_by_id(dickens_friend)

    with open(os.path.join(save_path, "mutual_friend_cleaned.txt"), 'wb') as f:
        f.write(cleaned_book)
