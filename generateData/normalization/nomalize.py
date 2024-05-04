import json
import unicodedata
from collections import Counter
import re


def extract_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def extract_title_domain(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    filtered_data = []
    for item in data:
        filtered_item = {
            "titlu": unicodedata.normalize("NFKD", item.get("titlu", "")).strip(),
            "domeniu": unicodedata.normalize("NFKD", item.get("domeniu", "")).strip()
        }
        filtered_data.append(filtered_item)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)


# extract_title_domain("./all_raw_data.json", "titlu_domeniu.json")

# title_domain_text = extract_data("titlu_domeniu.json")


def clean_text(text):
    text.lower()
    # Remove specific codes and numbers related to cases
    text = re.sub(r"DOSAR NR\..*? ", "", text)
    text = re.sub(r"NR\.\s+\d+", "", text)
    # Remove any remaining digits
    text = re.sub(r"\d+", "", text)
    # Remove city names (you can add more city names to this list as needed)
    city_regex = r"\b(Sibiu|Bucuresti|Timisoara|Cluj|Brasov)\b"
    text = re.sub(city_regex, "", text, flags=re.IGNORECASE)

    # Remove any remaining non-standard characters and extra spaces
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# def clean_title_domain(title_domain_text_data):
#     for item in title_domain_text_data:
#         for key in item:
#             if isinstance(item[key], str):
#                 item[key] = clean_text(item[key])
#
#     with open("titlu_domeniu_clean.json", 'w', encoding='utf-8') as file:
#         json.dump(title_domain_text, file, indent=4, ensure_ascii=False)
#
#
# clean_title_domain(title_domain_text)

def remove_short_words(phrase):
    # Split the phrase into words, filter words with length less than 4, and join them back into a string
    return ' '.join(word for word in phrase.split() if len(word) >= 4)


# shortened_items = []
#
# for item in title_domain_text_clean:
#
#     old_domain = item.get("domeniu")
#     new_domain = remove_short_words(old_domain).lower()
#
#     shortened_item = {
#         "titlu": item.get("titlu").lower(),
#         "domeniu": new_domain
#     }
#
#     shortened_items.append(shortened_item)
#
#
# with open("titlu_domeniu_shortened.json", 'w', encoding='utf-8') as file:
#     json.dump(shortened_items, file, indent=4, ensure_ascii=False)

#
# title_domain_text_clean_shortend = extract_data("titlu_domeniu_shortened.json")
#
# print(len(title_domain_text_clean_shortend))
#
# for item in title_domain_text_clean_shortend:
#     if len(item.get("titlu")) < len(item.get("domeniu")):
#         title_domain_text_clean_shortend.remove(item)
#     if len(item.get("domeniu")) < 4:
#         title_domain_text_clean_shortend.remove(item)
#
# print(len(title_domain_text_clean_shortend))
#
#
# with open("titlu_domeniu_shortened.json", 'w', encoding='utf-8') as file:
#     json.dump(title_domain_text_clean_shortend, file, indent=4, ensure_ascii=False)


# def count_occurrences(data):
#     domeniu_counts = {}
#
#     for item in data:
#         domeniu = item.get("domeniu", "")
#
#         if domeniu in domeniu_counts:
#             domeniu_counts[domeniu] += 1
#         else:
#             domeniu_counts[domeniu] = 1
#
#     return sorted([(key, value) for key, value in domeniu_counts.items()], key=lambda x: x[1], reverse=True)
#
#
# def write_occurrences(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     domeniu_list = count_occurrences(data)
#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(domeniu_list, file, indent=4, ensure_ascii=False)
#
#
# write_occurrences('titlu_domeniu_shortened.json', 'occurrences.json')

with open("./occurrences.json", 'r', encoding='utf-8') as file:
    occurences = json.load(file)

with open("./titlu_domeniu_shortened.json", 'r', encoding='utf-8') as file:
    working_data = json.load(file)


def has_more_than_ten_occurrences(data, search_domain):
    for item in data:
        domain = item[0]
        count = item[1]
        if domain == search_domain and count > 99:
            return True
    return False


new_working_data = []

for item in working_data:
    should_remove = False  # Flag to determine if the item should be removed

    for occurrence in occurences:
        domain = occurrence[0]
        if domain == item.get("domeniu") and occurrence[1] < 100:
            should_remove = True
            break  # No need to check further occurrences if one matches the criteria

    if not should_remove:
        new_working_data.append(item)  # Only keep items that don't match the removal criteria

# Now 'new_working_data' contains the items you want to keep
working_data = new_working_data

with open("working_data.json", 'w', encoding='utf-8') as file:
    json.dump(new_working_data, file, indent=4, ensure_ascii=False)
