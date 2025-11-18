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

# 프롬프트 (사용자 입력 / 쿼리)
messages = [
    {"role": "user", "content": "Create a funny joke about chickens."}
]

# chat template을 사용해서 토큰화
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

# 출력 생성
outputs = model.generate(
    inputs,
    max_new_tokens=500,
    do_sample=False,
    pad_token_id=tokenizer.eos_token_id
)

# 디코딩
response = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
print(response)