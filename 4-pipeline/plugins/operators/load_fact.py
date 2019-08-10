from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):
    """
    Operator used to move data from staging and dimension tables to fact tables.
    """
    ui_color = '#F98866'

    sql_command = """
        INSERT INTO {} {}
        {}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 columns="",
                 source_sql_command="",
                 delete_data=False,
                 *args, **kwargs):
        """
        Initializes the load fact table operator. It moves data from a staging to a fact table in Redshift.
        :param redshift_conn_id: identifier of the Redshift connection in Airflow.
        :param table: the table that we want to load.
        :param source_sql_command: the SQL command used to obtain the data to load.
        :param delete_data: True if we want to delete existing data. False otherwise.
        :param args: Airflow's args.
        :param kwargs: Airflow's kwargs.
        """
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.columns = columns
        self.source_sql_command = source_sql_command
        self.delete_data = delete_data

    def execute(self, context):
        """
        Executes the load fact table operation. It moves the data specified by the source_sql_command to the
        specified fact table.
        :param context: Airflow's context.
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.delete_data:
            self.log.info(f'About to delete all data from: {self.table}')
            redshift.run(f'DELETE FROM {self.table}')

        formatted_sql = LoadFactOperator.sql_command.format(
            self.table,
            self.columns,
            self.source_sql_command
        )

        self.log.info(f'About to execute: {formatted_sql}')
        redshift.run(formatted_sql)
