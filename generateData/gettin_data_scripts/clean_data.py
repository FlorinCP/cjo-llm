import json
import unicodedata
from collections import Counter
import re


def clean_text(text):
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)

    # Remove specific codes and numbers related to cases
    text = re.sub(r"DOSAR NR\..*? ", "", text)
    text = re.sub(r"NR\.\s+\d+", "", text)

    # Replace dates with a standard format (this example assumes dates are already in DD.MM.YYYY format)
    text = re.sub(r"(\d{2})\.(\d{2})\.(\d{4})", r"\3-\2-\1", text)

    # Remove any remaining digits
    text = re.sub(r"\d+", "", text)

    # Remove words with more than one capital letter
    text = re.sub(r"\b\w*[A-Z]\w*[A-Z]\w*\b", "", text)

    # Remove standalone capital letters
    text = re.sub(r"\b[A-Z]\b", "", text)

    # Remove city names (you can add more city names to this list as needed)
    city_regex = r"\b(Sibiu|Bucuresti|Timisoara|Cluj|Brasov)\b"
    text = re.sub(city_regex, "", text, flags=re.IGNORECASE)

    # Remove any remaining non-standard characters and extra spaces
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        for key in item:
            if isinstance(item[key], str):
                item[key] = clean_text(item[key])

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# process_json_file('all_raw_data.json', 'cleaned_output.json')


def count_occurrences(data):
    speta_counts = {}
    domeniu_counts = {}

    for item in data:
        speta = item.get("speta", "")
        domeniu = item.get("domeniu", "")

        if speta in speta_counts:
            speta_counts[speta] += 1
        else:
            speta_counts[speta] = 1

        if domeniu in domeniu_counts:
            domeniu_counts[domeniu] += 1
        else:
            domeniu_counts[domeniu] = 1

    speta_list = sorted([(key, value) for key, value in speta_counts.items()], key=lambda x: x[1], reverse=True)
    domeniu_list = sorted([(key, value) for key, value in domeniu_counts.items()], key=lambda x: x[1], reverse=True)

    return speta_list, domeniu_list


def write_occurrences(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    speta_list, domeniu_list = count_occurrences(data)
    results = {
        "speta_occurrences": speta_list,
        "domeniu_occurrences": domeniu_list
    }
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4, ensure_ascii=False)


# write_occurrences('cleaned_output.json', 'occurrences.json')


def find_top_n_words(n, occurrences):
    word_counts = Counter()

    for item in occurrences:
        if not isinstance(item, list) or len(item) != 2 or not isinstance(item[1], int):
            print(f"Skipping malformed entry: {item}")
            continue

        phrase = item[0]

        words = re.findall(r'\w+', phrase.lower())

        for word in words:
            if len(word) > 3:
                word_counts[word] += 1

    return word_counts.most_common(n)


with open("domain.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

print(find_top_n_words(20, data))
