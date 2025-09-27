from transformers import pipeline

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=0)
generator.tokenizer.pad_token_id = generator.tokenizer.eos_token_id

N = 1000
story_prompts = ["Deep in the Amazon rainforest, "] * N

for s in story_prompts:
  out = generator(s, max_length = 50, batch_size = 100)

  print(out)