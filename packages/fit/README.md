# Fine-tuning 프로젝트

OpenAI 모델 파인튜닝 및 머신러닝 실험을 위한 프로젝트입니다.

## 설치

```bash
cd fit
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

## 프로젝트 구조

- `jobs.ipynb` - 파인튜닝 작업 예제 노트북

## 사용 방법

1. `.env` 파일에 OpenAI API 키 설정:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

2. Jupyter 노트북 실행:
   ```bash
   jupyter notebook
   ```
