import json
import torch
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import DataLoader
from transformers import DefaultDataCollator
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

device = 'cpu'
logger.info(f"Using device: {device}")
model_path = './my_multilingual_model'

# Load the tokenizer and model with detailed error logging
try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()
    logger.info("Tokenizer and model loaded successfully.")
except Exception as e:
    logger.exception("Failed to load tokenizer and model. Ensure that the model_path is correct and all required files are present.")

# Load data with detailed error logging
try:
    with open("./normalization/working_data_labeled.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    test_df = pd.DataFrame(data)
    test_dataset = Dataset.from_pandas(test_df)
    logger.info("Data loaded and converted to pandas DataFrame.")
except Exception as e:
    logger.exception("Failed to load or process the test data.")

# Tokenization function as defined in your training script
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

# Apply tokenization with detailed error logging
try:
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    logger.info("Tokenization applied to test data.")
except Exception as e:
    logger.exception("Failed to tokenize the test data.")

# Setup DataLoader
data_collator = DefaultDataCollator(return_tensors="pt")
test_dataloader = DataLoader(tokenized_test, batch_size=16, collate_fn=data_collator)

# Make predictions with detailed error logging
try:
    for batch in test_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.no_grad():
            outputs = model(**batch)
            predictions = torch.argmax(outputs.logits, dim=-1)
            logger.info(f"Predictions: {predictions.tolist()}")
except Exception as e:
    logger.exception("Failed during model prediction.")
