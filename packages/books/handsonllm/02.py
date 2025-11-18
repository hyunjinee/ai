from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="mps" if torch.backends.mps.is_available() else "cpu",
    torch_dtype="auto",
    trust_remote_code=True,
    attn_implementation="eager",
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

prompt = """Write an email apologizing to Sarah for the tragic gardening mishap.
Explain how it happened.<|assistant|>"""
# Tokenize the input prompt
device = "mps" if torch.backends.mps.is_available() else "cpu"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
# Generate the text
generation_output = model.generate(
    input_ids=input_ids,
    max_new_tokens=20,
    use_cache=False,
    pad_token_id=tokenizer.eos_token_id
)

print(input_ids)
# Print the output
print(tokenizer.decode(generation_output[0]))