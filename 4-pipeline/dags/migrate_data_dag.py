from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'John Jairo Martinez',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 12),
    'email': ['notification@mycompany.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('migrate_data_to_redshift',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          catchup=False
          )

start_operator = DummyOperator(task_id='begin_execution', dag=dag)

# copy data to staging tables

stage_country = StageToRedshiftOperator(
    task_id='stage_country',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_country",
    s3_bucket="dend-jjmb",
    s3_key="Country.csv",
    file_type="csv"
)

stage_indicators_by_country = StageToRedshiftOperator(
    task_id='stage_indicators_by_country',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_indicators_by_country",
    s3_bucket="dend-jjmb",
    s3_key="Indicators.csv",
    file_type="csv"
)

stage_suicide_rates = StageToRedshiftOperator(
    task_id='stage_suicide_rates',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_suicide_rates",
    s3_bucket="dend-jjmb",
    s3_key="suicide_rates.csv",
    file_type="csv"
)

stage_global_land_temperatures_by_country = StageToRedshiftOperator(
    task_id='stage_global_land_temperatures_by_country',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_global_land_temperatures_by_country",
    s3_bucket="dend-jjmb",
    s3_key="GlobalLandTemperaturesByCountry.csv",
    file_type="csv"
)

stage_global_land_temperatures_by_city = StageToRedshiftOperator(
    task_id='stage_global_land_temperatures_by_city',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_global_land_temperatures_by_city",
    s3_bucket="dend-jjmb",
    s3_key="GlobalLandTemperaturesByCity.csv",
    file_type="csv"
)

stage_world_happiness = StageToRedshiftOperator(
    task_id='stage_world_happiness',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_world_happiness",
    s3_bucket="dend-jjmb",
    s3_key="world-happiness-report.json",
    file_type="json"
)

# move data to dimension tables

start_dimension_tables = DummyOperator(task_id='start_dimension_tables', dag=dag)

load_dim_country = LoadDimensionOperator(
    task_id='load_dim_country_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="dim_country",
    columns="(country_code, alpha2_code, short_name, long_name, region, income_group)",
    source_sql_command=SqlQueries.insert_dim_country
)

load_dim_date = LoadDimensionOperator(
    task_id='load_dim_date_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="dim_date",
    columns="(full_date, year, month, day)",
    source_sql_command=SqlQueries.insert_dim_date
)

# move data to fact tables

start_fact_tables = DummyOperator(task_id='start_fact_tables', dag=dag)

load_fact_temp_by_country = LoadFactOperator(
    task_id='load_fact_temp_by_country',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_temperatures_by_country",
    columns="(country_code, full_date, avg_temperature, avg_uncertainty)",
    source_sql_command=SqlQueries.insert_fact_temp_by_country,
    delete_data=True
)

load_fact_temp_by_city = LoadFactOperator(
    task_id='load_fact_temp_by_city',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_temperatures_by_city",
    columns="(city, country_code, full_date, avg_temperature, avg_uncertainty)",
    source_sql_command=SqlQueries.insert_fact_temp_by_city,
    delete_data=True
)

load_fact_indicators = LoadFactOperator(
    task_id='load_fact_indicators',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_indicators",
    columns="(country_code, indicator_name, indicator_code, value, year)",
    source_sql_command=SqlQueries.insert_fact_indicators,
    delete_data=True
)

load_fact_indicators_with_happiness_data = LoadFactOperator(
    task_id='load_fact_indicators_with_happiness_data',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_indicators",
    columns="(country_code, indicator_name, indicator_code, value, year)",
    source_sql_command=SqlQueries.insert_fact_indicators_with_happiness,
    delete_data=True
)

load_fact_indicators_with_suicide_data = LoadFactOperator(
    task_id='load_fact_indicators_with_suicide_data',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_indicators",
    columns="(country_code, indicator_name, indicator_code, value, year)",
    source_sql_command=SqlQueries.insert_fact_indicators_with_suicides,
    delete_data=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=["dim_country", "dim_date", "fact_temperatures_by_country",
            "fact_temperatures_by_city", "fact_indicators"]
)

end_operator = DummyOperator(task_id='end_execution', dag=dag)

# DAG Definition

start_operator >> stage_country
start_operator >> stage_indicators_by_country
start_operator >> stage_suicide_rates
start_operator >> stage_global_land_temperatures_by_country
start_operator >> stage_global_land_temperatures_by_city
start_operator >> stage_world_happiness

stage_country >> start_dimension_tables
stage_indicators_by_country >> start_dimension_tables
stage_suicide_rates >> start_dimension_tables
stage_global_land_temperatures_by_country >> start_dimension_tables
stage_global_land_temperatures_by_city >> start_dimension_tables
stage_world_happiness >> start_dimension_tables

start_dimension_tables >> load_dim_country
start_dimension_tables >> load_dim_date

load_dim_country >> start_fact_tables
load_dim_date >> start_fact_tables

start_fact_tables >> load_fact_temp_by_country
start_fact_tables >> load_fact_temp_by_city
start_fact_tables >> load_fact_indicators
start_fact_tables >> load_fact_indicators_with_happiness_data
start_fact_tables >> load_fact_indicators_with_suicide_data

load_fact_temp_by_country >> run_quality_checks
load_fact_temp_by_city >> run_quality_checks
load_fact_indicators >> run_quality_checks
load_fact_indicators_with_happiness_data >> run_quality_checks
load_fact_indicators_with_suicide_data >> run_quality_checks

run_quality_checks >> end_operator
