from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# 예시 데이터 생성
data = {
    'text': [
        '이 영화는 정말 재미있었어요',
        '시간 낭비였습니다',
        '훌륭한 작품입니다',
        '실망스러운 내용이네요',
        # 더 많은 데이터 추가 가능
    ],
    'label': [1, 0, 1, 0]  # 1: 긍정, 0: 부정
}

# DataFrame을 데이터셋으로 변환
df = pd.DataFrame(data)
train_dataset = Dataset.from_pandas(df)


# 토크나이징 함수
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)


# 사전 학습된 모델과 토크나이저 로드
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 학습 데이터셋 로드
train_dataset = train_dataset.map(tokenize_function, batched=True)

# 학습 설정
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
)

# Trainer 초기화 및 학습 시작
trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset)
trainer.train()
