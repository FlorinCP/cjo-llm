from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class TextItem(BaseModel):
    text: str


app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("16cosmin/cjo-finetuned-bert-uncased")
model = AutoModelForSequenceClassification.from_pretrained("16cosmin/cjo-finetuned-bert-uncased")
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


@app.post("/classify/")
def classify_text(item: TextItem):
    try:
        encoded_input = tokenizer.encode_plus(
            item.text,
            add_special_tokens=True,
            return_tensors='pt',
            max_length=512,
            padding='max_length',
            truncation=True
        )

        input_ids = encoded_input['input_ids'].to(device)
        attention_mask = encoded_input['attention_mask'].to(device)

        with torch.no_grad():
            output = model(input_ids, attention_mask=attention_mask)

        logits = output.logits.detach().cpu().numpy()
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)

        predicted_label = np.argmax(probabilities, axis=1)[0]
        return {"label": int(predicted_label)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

