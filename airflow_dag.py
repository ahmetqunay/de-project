from airflow import DAG
import pendulum
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator


#change
PROJE_AD = "caramel-slice-395008"
DB_AD = "db"


with DAG(
    dag_id="bq",
    schedule="@daily",
    start_date=pendulum.datetime(2023,8,21,tz="UTC")
    ) as dag:


#change
    query =f"SELECT firma,ROUND(acilis, 2) AS acilis,ROUND(en_yuksek, 2) AS en_yuksek,ROUND(en_dusuk, 2) AS en_dusuk,ROUND(kapanis, 2) AS kapanis,tarih FROM  {PROJE_AD}.{DB_AD}.project1" 

    create_new_table = BigQueryExecuteQueryOperator(
        task_id = "create_new_table",
        sql=query,
        destination_dataset_table=f"{PROJE_AD}.{DB_AD}.airflow1",
        create_disposition="CREATE_IF_NEEDED", 
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="google_cloud"
    )


    create_new_table
