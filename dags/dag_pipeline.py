# dag_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.DataExtraction import main as extractMain
from scripts.TransformData import main as transformMain
from scripts.StoreData import main as storeMain

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Data Handling',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extractMain,
        op_kwargs={'python_callable': 'extract.main'}
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transformMain,
        op_kwargs={'python_callable': 'transform.main'}
    )

    store_task = PythonOperator(
        task_id='store_data',
        python_callable=storeMain,
        op_kwargs={'python_callable': 'store.main'}
    )

    extract_task >> transform_task >> store_task
