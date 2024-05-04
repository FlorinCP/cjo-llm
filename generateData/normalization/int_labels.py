import json

from sklearn.preprocessing import LabelEncoder


def process_and_save_dataset(input_file_path, output_file_path):
    # Load the data from a JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract labels from the data
    labels = [item['label'] for item in data]

    # Initialize the label encoder
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)

    # Replace text labels with encoded labels in the data
    for item, label in zip(data, encoded_labels):
        item['label'] = int(label)  # Convert numpy int to Python int for JSON serialization compatibility

    print(f"Labels encoded successfully. Number of unique labels: {len(set(encoded_labels))}")

    # Save the updated dataset to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    print(f"Dataset processed and saved to {output_file_path}")


# Example usage
input_file = 'working_data.json'
output_file = 'working_data_labeled.json'
process_and_save_dataset(input_file, output_file)
