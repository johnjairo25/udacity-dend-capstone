# Infrastructure as Code (iac)

In this part of the project the infrastructure used in this project is created.
Two components are initialized:

1. Redshift Cluster
2. Apache Airflow

## Redshift Cluster

The Redshift Cluster is created using the Python's `boto3` library. In this file
the IAM (Identity and Access Management) is set up and then a Redshift cluster is
started. All the configuration values for this script should be configured in the
`aws.cfg` file located in this folder.

```bash
python create_redshift_cluster.py
```

## Apache Airflow

For the Airflow instance, Docker was used as a tool to start the service. Given
that to start Apache Airflow, a minimum of two containers are required (Postgres and
Airflow), we created a `docker-compose` file that sets this things up.

The `docker-compose` file points to the `4-pipeline` folder for dags and plugins.

```bash
docker-compose up -d
```
