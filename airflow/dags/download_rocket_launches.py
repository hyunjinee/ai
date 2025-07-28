"""
로켓 발사 정보를 다운로드하는 DAG
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import requests
import json
import pandas as pd


def download_rocket_launches(**context):
    """Space Launch Now API에서 로켓 발사 정보를 다운로드합니다."""
    
    # API 엔드포인트
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
    
    # API 호출
    response = requests.get(url)
    data = response.json()
    
    # 결과를 JSON 파일로 저장
    execution_date = context['execution_date'].strftime('%Y%m%d')
    filename = f'/tmp/rocket_launches_{execution_date}.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"다운로드 완료: {len(data.get('results', []))}개의 발사 정보")
    return filename


def process_launch_data(**context):
    """다운로드한 데이터를 처리합니다."""
    
    # 이전 태스크에서 파일명 가져오기
    filename = context['task_instance'].xcom_pull(task_ids='download_launches')
    
    # JSON 파일 읽기
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # 데이터 처리
    launches = []
    for launch in data.get('results', []):
        launches.append({
            'name': launch.get('name'),
            'net': launch.get('net'),
            'status': launch.get('status', {}).get('name'),
            'rocket': launch.get('rocket', {}).get('configuration', {}).get('name'),
            'provider': launch.get('launch_service_provider', {}).get('name'),
            'location': launch.get('pad', {}).get('location', {}).get('name')
        })
    
    # DataFrame으로 변환
    df = pd.DataFrame(launches)
    
    # CSV로 저장
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    
    print(f"처리 완료: {len(df)}개의 레코드를 CSV로 저장")
    return csv_filename


# 기본 DAG 인자
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
dag = DAG(
    'download_rocket_launches',
    default_args=default_args,
    description='로켓 발사 정보를 다운로드하고 처리하는 DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# 태스크 정의
download_task = PythonOperator(
    task_id='download_launches',
    python_callable=download_rocket_launches,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_launches',
    python_callable=process_launch_data,
    dag=dag,
)

cleanup_task = BashOperator(
    task_id='cleanup_temp_files',
    bash_command='rm -f /tmp/rocket_launches_*.json /tmp/rocket_launches_*.csv',
    dag=dag,
)

# 태스크 의존성 설정
download_task >> process_task >> cleanup_task 