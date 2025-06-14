import json
import string
import unicodedata

def add_scream_index(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for obj in data:
        text = obj['message']
        letters = [c for c in text if unicodedata.category(c).startswith('L')]
        if letters:
            scream_index = sum(1 for c in letters if c.isupper()) / len(letters)
        else:
            scream_index = 0.0
        obj['scream_index'] = scream_index
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scream_index_calc.py <json_file_path>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    add_scream_index(json_file_path)
    print(f"Scream index added to {json_file_path}")
