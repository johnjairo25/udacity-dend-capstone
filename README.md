# Udacity's DEND Capstone Project

This project builds a data-pipeline using _Apache Airflow_ based on
public datasets.

The main technologies used are:

1. _Apache Airflow_ to build the data-pipeline.
2. _Jupyter Notebooks_ to explore and pre-processed the datasets.
3. _Amazon S3_ to store the pre-processed data.
4. _Amazon Redshift_ as data-warehouse to hold the final data.
5. _Docker_ to run Apache Airflow.

The steps taken in these project are:

1. Data exploration and pre-processing of all datasets with Jupyter notebooks
2. Processed datasets are uploaded to S3 using python scripts
3. The infrastructure is created by code
4. A data-pipeline is built on Apache Airflow to move data from S3 to Redshift
5. Some analysis of the Redshift data is performed

## Project Datasets

All the datasets of this project were obtained from
[Kaggle's website](https://www.kaggle.com):

- [World development indicators by the World Bank](https://www.kaggle.com/worldbank/world-development-indicators)
- [Climate change by Berkeley Earth](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
- [Suicide rates overview](https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016)
- [World Happiness Report](https://www.kaggle.com/unsdsn/world-happiness)

These datasets can be downloaded directly from Kaggle's website, or they can
also be downloaded using the `download-dataset.sh` file found in the root
folder of this project.

One of the requirements of this project was to handle at least two different
file formats. **Given that the datasets had just `csv` files, I addressed this
issue in the data-exploration and pre-processing part**. Some of the pre-processed
files were exported as `json`. In particular the `World Happiness Report` dataset
was uploaded to Amazon S3 as `json`.

## Files and Folder Structure

Each step of the project is contained in a specific folder. Inside each folder
there's a README file with the description of its contents.

## Scoping the project

The goal of this project is to build a data-model that allows users to create
queries that can relate information about different indicators with information
about temperature.

Questions like:

- Is the education quality related to the suicide rate?
- Is the increase in world land temperature related to the economic growth of a country?

## Tool Selection

Before defining the storage tool, a data-exploration step needed to be
performed. The easiest way to do this was using `Jupyter Notebooks`, because
they gave me the flexibility to explore the data and get relevant insights
of each dataset. I also used these Notebooks to pre-process the information
in each dataset and get rid of information that I did not want to consider
in the scope of the project.

Once the data-exploration and pre-processing was done, I discovered that
the information of all the datasets is structured. Therefore, the most reasonable
decision was to use a relational data store. In particular, `Amazon Redshift`
was used due to its capacity to process large amounts of data
and to store information in a columnar format, allowing faster queries.

To move the data to Redshift, two steps were taken. The first one was to
upload the pre-processed files to `Amazon S3`. These pre-processed files
became the data source of the pipeline process. The second step was
to implement a solution that can implement the pipeline. For this,
I chose `Apache Airflow`. Airflow allows creating workflows as DAGs
(Direct Acyclic Graphs), and each DAG has tasks that can be retried,
monitored and logged. These and all the other features of Airflow
make it perfect for the data pipeline process.

## Data model

Considering the different data sources, the following diagram shows the final
data-model:

![Final Data Model](4-pipeline/images/fact-dimension-tables.png)

I divided the model in dimension and fact tables:

### Dimension tables

1. `dim_country`: Contains information about the countries used in the indicators
and temperatures tables.
    - `country_code`: alpha3 code of the country.
    - `alpha2_code`: alpha2 code of the country.
    - `short_name`: the name of the country in short format.
    - `long_name`: the name of the country in long format.
    - `region`: the region to which the country belongs to.
    - `income_group`: the income group to which the country belongs to.
2. `dim_date`: Contains information related to the date of a temperature
measurement.
    - `full_date`: the full date in the format `yyyy-mm-dd`.
    - `year`: the year of the date.
    - `month`: the month of the date (number between 1 and 12).
    - `day`: the day of the month.

### Fact tables

1. `fact_temperatures_by_country`:
    - `id`: Auto-generated identifier for the table.
    - `country_code`: the alpha3 code of the country associated to this
    measurement.
    - `full_date`: the full date in the format `yyyy-mm-dd` associated to this
    measurement.
    - `avg_temperature`: the average temperature measured.
    - `avg_uncertainty`: the uncertainty of the measurement.
2. `fact_temperatures_by_city`:
    - `id`: Auto-generated identifier for the table.
    - `city`: the name of the city of this measurement.
    - `country_code`: the alpha3 code of the country associated to this
    measurement.
    - `full_date`: the full date in the format `yyyy-mm-dd` associated to this
    measurement.
    - `avg_temperature`: the average temperature measured.
    - `avg_uncertainty`: the uncertainty of the measurement.
3. `fact_indicators`:
    - `id`: Auto-generated identifier for the table.
    - `country_code`: the alpha3 code of the country associated to this
    indicator.
    - `indicator_name`: the name of the indicator.
    - `indicator_code`: an identifier for the indicator.
    - `value`: the value associated to the identifier.
    - `year`: the year of the measurement.

## Addressing Other Scenarios

This pipeline address some basic concerns of the whole process, but if
we moved this pipeline to production there would be a number of issues
that we would have to address:

### The data was increased by 100x

If the data increased by 100x, we would need to consider a number of
technical issues: storage options, data ingestion options, data partition
alternatives.

**Storage options**:

- Most likely the hard drives of our Redshift cluster would run out
of memory. If we wanted to stay using Redshift we could scale out or
up our cluster to increase the storage capacity.
- Another alternative would be to use S3 with `parquet` files
and `Apache Spark` instead of Redshift. This alternative would make
the usage of our data a little bit more restrictive, since we would
require that our users know `Spark` to query the data.

**Data ingestion options**:

The data ingestion process would be a lot heavier and would take more
time. It sounds reasonable to break the ingestion process in batches.
According to our dataset, the field that we would most likely use is
the `date` of our measurements in the fact tables.

Depending on the frequency of the generated data, we could schedule
the import pipeline process to run various times during the day,
making the process lighter.

Another alternative would be to change the approach to `stream processing`,
with a tool like `Spark Streaming`, `Kafka Streams`, `Apache Storm`,
`Apache Flink`, among others. This would allow us to save micro-batches
to Redshift constantly, and would reduce the lag that we have in
our Data Warehouse.

**Data partitioning**:

If the data is so big that the queries become slow, one of the options
is to partition the data in different tables. The `date` field of
our fact tables looks like one of the best options, because most likely
the analysis are going to be restricted to a specific period of time.

### The pipelines would be run on a daily basis by 7 am every day

First of all, in this pipeline we are not concerned with _DAG scheduling_.
If we ran this process on a daily basis, we would need to schedule the
DAG properly.

To guarantee that our DAG executes successfully, we would need to
implement task retries and notifications. The interested parties, technical
staff and final users should be notified if the pipeline fails. Also,
the failure scenario would need to be handled in some way. This definition
would need the input of the users to handle the error case in a graceful
manner.

If the same instance of `Apache Airflow` is shared among many pipelines,
we would need to pay attention to the Task Scheduler, because we must
guarantee that our worker instances have enough resources to process the
tasks. According to my research in Airflow, the Kubernetes executor
could help by creating new pods to process tasks in isolated instances.

### The database needed to be accessed by 100+ people

First of all, with an increase on the number of users we enter into the
concurrency problem. This means that we have to handle multiple requests
at the same time. But, since this is a DWH where users don't generate
new data, the most likely problem would be the load we impose to our Redshift
instance. To handle the increase of the load we can again scale out or up
our cluster.

Another problem is the access control to our database. In this example,
it sounds like we don't need restrictions by table, but in some cases
we might need to do it. For those cases we could have different alternatives:
one would be to create database users with specific privileges restricting
the access to the required tables, other one would be creating an application
that implements some sort of Access Control Layer between the users
and the Redshift instance, and this application would restrict access
to the resources.
