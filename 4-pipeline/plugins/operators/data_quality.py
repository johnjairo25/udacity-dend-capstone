from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    """
    Operator used to perform quality checks of a set of tables.
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):
        """
        Initializes the data quality operator
        :param redshift_conn_id: identifier of the redshift Connection in Airflow
        :param tables: array of tables to verify
        :param args: Airflow's args
        :param kwargs: Airflow's kwargs
        """

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        """
        Executes the data quality validation. Verifies that the table exists and has at least one row.
        :param context: Airflow's context
        """
        redshift = PostgresHook(self.redshift_conn_id)

        for table in self.tables:
            records = redshift.get_records(f"SELECT COUNT(1) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {table} contained 0 rows")
            self.log.info(f"Data quality on table {table} check passed with {records[0][0]} records")

        self.log.info("All data quality checks passed")
