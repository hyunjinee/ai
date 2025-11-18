from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
  "microsoft/Phi-3-mini-4k-instruct",
  device_map="mps" if torch.backends.mps.is_available() else "cpu",
  torch_dtype="auto",
  trust_remote_code=True,
  attn_implementation="eager",  # flash-attention 경고 해결
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

from transformers import pipeline
# Create a pipeline
generator = pipeline(
  "text-generation",
  model=model,
  tokenizer=tokenizer,
  return_full_text=False,
  max_new_tokens=500,
  do_sample=False
)
# 프롬프트 (사용자 입력 / 쿼리)
messages = [
{"role": "user", "content": "Create a funny joke about chickens."}
]
# 출력 생성
output = generator(messages)
print(output[0]["generated_text"])