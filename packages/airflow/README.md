# Airflow 데이터 파이프라인

Apache Airflow를 사용한 데이터 파이프라인 프로젝트입니다.

## 설치

```bash
cd airflow
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

## 프로젝트 구조

```
airflow/
├── dags/           # Airflow DAG 파일들
├── plugins/        # 커스텀 플러그인
├── logs/           # 실행 로그
└── config/         # 설정 파일
```

## Airflow 초기화 및 실행

1. Airflow 데이터베이스 초기화:

   ```bash
   airflow db init
   ```

2. 관리자 계정 생성:

   ```bash
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com
   ```

3. 웹서버 실행 (터미널 1):

   ```bash
   airflow webserver --port 8080
   ```

4. 스케줄러 실행 (터미널 2):
   ```bash
   airflow scheduler
   ```

## 환경 변수 설정

`.env` 파일 생성:

```
AIRFLOW_HOME=/path/to/airflow
```
