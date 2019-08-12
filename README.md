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

# Project Datasets

All the datasets of this project were obtained from 
[Kaggle's website](https://www.kaggle.com):

- [World development indicators by the World Bank](https://www.kaggle.com/worldbank/world-development-indicators)
- [Climate change by Berkeley Earth](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
- [Suicide rates overview](https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016)
- [World Happiness Report](https://www.kaggle.com/unsdsn/world-happiness)

These datasets can be downloaded directly from Kaggle's website, or they can 
also be downloaded using the `download-dataset.sh` file found in the root 
folder of this project.

# Files and Folder Structure

Each step of the project is contained in a specific folder. Inside of each folder 
there's a README file with the description of its contents.

## Final Thoughts

Given that we have only one pipeline and is run only once, there are some 
considerations that were left out:

- There's no special configuration for retries of tasks, which would be
very important in a production setting.
- There are no dependencies between tasks, which is usually a source of
additional complexity in the pipeline.
- If the data were bigger, we would need to partition the data in different
tables based on a specific field. In this datasets the `date` seems like a
reasonable key to split the data.
- Notifications for failures are a most do. Also, user configuration in
Airflow is needed.
- Access control for different users to Redshift is also a concern that
should be addressed.
- Depending on the number of users and type of queries, we may need to scale
out or up the Redshift instance.
- In a production setting, we would probably have different configuration for
Airflow. The basic Dockerfile of this project allowed us to execute the tasks
for one pipeline, but if we have many pipelines, we would need many executors
in parallel. I think the Kubernetes execution option seems better suited for
this task.
