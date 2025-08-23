from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-5")

result = model.invoke("카카오엔터테인먼트 베리즈에 대해서 알려줘")

print("Full response:")
print(result)
print("Content Only:")
print(result.content)
