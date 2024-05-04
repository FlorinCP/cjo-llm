import json
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import logging
import torch

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
logger.debug("Tokenizer loaded successfully.")
tokenizer.save_pretrained("my_multilingual_model")
with open("./normalization/working_data_labeled.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
logger.debug(f"Data loaded successfully with {len(data)} records.")

df = pd.DataFrame(data)
dataset = Dataset.from_pandas(df)

logger.debug("Data converted to Hugging Face Dataset format.")

train_test_split = dataset.train_test_split(test_size=0.3)
train_dataset = train_test_split["train"]
eval_dataset = train_test_split["test"]
logger.debug(f"Data split into {len(train_dataset)} training and {len(eval_dataset)} evaluation records.")


def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)


tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_eval = eval_dataset.map(tokenize_function, batched=True)
logger.debug("Tokenization applied to both training and evaluation datasets.")

model = AutoModelForSequenceClassification.from_pretrained('./my_multilingual_model', num_labels=5).to(device)
logger.debug("Model loaded and initialized.")

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    warmup_steps=1000,
    weight_decay=0.05,
    logging_dir='./logs',
    logging_steps=50,
    learning_rate=5e-5,
    evaluation_strategy='steps',
    eval_steps=500,
    save_strategy='steps',
    save_steps=500
)
logger.debug("Training arguments set.")

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval
)
logger.debug("Trainer initialized.")

logger.info("Starting model training.")
trainer.train()
logger.info("Model training completed.")

model.save_pretrained('my_multilingual_model2')
logger.debug("Model saved successfully.")
