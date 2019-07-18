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
3. A data-pipeline is built on Apache Airflow to move data from S3 to Redshift
4. Some analysis of the Redshift data is performed

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
