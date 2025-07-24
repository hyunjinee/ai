from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o")

result = model.invoke("81 나누기 9")

print("Full response:")
print(result)
print("Content Only:")
print(result.content)
