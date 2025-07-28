import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

model_name = "distilbert-base-uncased-finetuned-sst-2-english"

model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
results = classifier(["We are very happy to show you the 🤗 Transformers library.",
                     "We hope you don't hate it."])

for result in results:
    print(result)

tokens = tokenizer.tokenize("We are very happy to show you the 🤗 Transformers library.")
token_ids = tokenizer.convert_tokens_to_ids(tokens)
input_ids = tokenizer("We are very happy to show you the 🤗 Transformers library.")

print(f'tokens: {tokens}')
print(f'token_ids: {token_ids}')
print(f'input_ids: {input_ids}')

X_train = ["We are very happy to show you the 🤗 Transformers library.",
              "We hope you don't hate it."]
batch = tokenizer(X_train, padding=True, truncation=True, return_tensors="pt", max_length=512)

with torch.no_grad():
    outputs = model(**batch)
    # logits = outputs.logits