import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

from helpers import SqlQueries

dag = DAG(
    'create_tables',
    start_date=datetime.datetime.utcnow()
)

start_task = DummyOperator(task_id='begin_execution', dag=dag)

# Tasks to create staging tables

create_staging_country = PostgresOperator(
    task_id='create_staging_country',
    dag=dag,
    sql=SqlQueries.create_staging_country,
    postgres_conn_id="redshift"
)

create_staging_indicators_by_country = PostgresOperator(
    task_id='create_staging_indicators_by_country',
    dag=dag,
    sql=SqlQueries.create_staging_indicators_by_country,
    postgres_conn_id="redshift"
)

create_staging_suicide_rates = PostgresOperator(
    task_id='create_staging_suicide_rates',
    dag=dag,
    sql=SqlQueries.create_staging_suicide_rates,
    postgres_conn_id="redshift"
)

create_staging_global_land_temperatures_by_country = PostgresOperator(
    task_id='create_staging_global_land_temperatures_by_country',
    dag=dag,
    sql=SqlQueries.create_staging_global_land_temperatures_by_country,
    postgres_conn_id="redshift"
)

create_staging_global_land_temperatures_by_city = PostgresOperator(
    task_id='create_staging_global_land_temperatures_by_city',
    dag=dag,
    sql=SqlQueries.create_staging_global_land_temperatures_by_city,
    postgres_conn_id="redshift"
)

create_staging_world_happiness = PostgresOperator(
    task_id='create_staging_world_happiness',
    dag=dag,
    sql=SqlQueries.create_staging_world_happiness,
    postgres_conn_id="redshift"
)

# Tasks to create dimension tables

start_dimension_task = DummyOperator(task_id='start_dimension_tables', dag=dag)

create_dim_country = PostgresOperator(
    task_id='create_dim_country',
    dag=dag,
    sql=SqlQueries.create_dim_country,
    postgres_conn_id="redshift"
)

create_dim_date = PostgresOperator(
    task_id='create_dim_date',
    dag=dag,
    sql=SqlQueries.create_dim_date,
    postgres_conn_id="redshift"
)

# Tasks to create fact tables

start_fact_task = DummyOperator(task_id='start_fact_tables', dag=dag)

create_fact_temperatures_by_country = PostgresOperator(
    task_id='create_fact_temperatures_by_country',
    dag=dag,
    sql=SqlQueries.create_fact_temperatures_by_country,
    postgres_conn_id="redshift"
)

create_fact_temperatures_by_city = PostgresOperator(
    task_id='create_fact_temperatures_by_city',
    dag=dag,
    sql=SqlQueries.create_fact_temperatures_by_city,
    postgres_conn_id="redshift"
)

create_fact_indicators = PostgresOperator(
    task_id='create_fact_indicators',
    dag=dag,
    sql=SqlQueries.create_fact_indicators,
    postgres_conn_id="redshift"
)

# Ending task

end_task = DummyOperator(task_id='end_execution', dag=dag)

# DAG Definition

start_task >> create_staging_country
start_task >> create_staging_indicators_by_country
start_task >> create_staging_suicide_rates
start_task >> create_staging_global_land_temperatures_by_country
start_task >> create_staging_global_land_temperatures_by_city
start_task >> create_staging_world_happiness

create_staging_country >> start_dimension_task
create_staging_indicators_by_country >> start_dimension_task
create_staging_suicide_rates >> start_dimension_task
create_staging_global_land_temperatures_by_country >> start_dimension_task
create_staging_global_land_temperatures_by_city >> start_dimension_task
create_staging_world_happiness >> start_dimension_task

start_dimension_task >> create_dim_country
start_dimension_task >> create_dim_date

create_dim_country >> start_fact_task
create_dim_date >> start_fact_task

start_fact_task >> create_fact_temperatures_by_country
start_fact_task >> create_fact_temperatures_by_city
start_fact_task >> create_fact_indicators

create_fact_temperatures_by_country >> end_task
create_fact_temperatures_by_city >> end_task
create_fact_indicators >> end_task
