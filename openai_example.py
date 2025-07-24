from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "너는 누구니?\n"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "저는 OpenAI에서 개발한 인공지능 언어 모델인 ChatGPT입니다. 사람들과 자연스러운 대화를 나누기 위해 만들어졌으며, 질문에 답하거나 다양한 주제에 대해 도움을 드릴 수 있습니다. 무엇을 도와드릴까요?"
        }
      ]
    }
  ],
  response_format={
    "type": "text"
  },
  temperature=1,
  max_completion_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
