# import basic libraries
from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator

from datacleaner import data_cleaner
# define dictionary of default parameters (helps while creating the tasks)
default_args = {
    'owner' : 'Airflow',
    'start_date' : datetime(2022, 7, 31),
    'retries' : 1,
    'retry_delay' : timedelta(seconds=5)
}
# instantiate a DAG object (DAG obj=list of  parameters)
#'store_dag'= unique DAG ID,  @daily= generate daily reports, False= to turn off the back fillings for DAG
dag=DAG('store_dag', default_args=default_args, schedule_interval='@daily',template_searchpath=['/usr/local/airflow/sql_files'], catchup=False)

#design the Tasks for the DAG
#task 1:  to check whether the source file exists in the input directory?
t1 = BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/raw_store_transactions.csv',retries=2,retry_delay=timedelta(seconds=15), dag=dag )
#shasam #returns the shasam value of the file (raw_store_transactions) exists or else get error
# store_files_airflow/raw_store_transactions.csv = this is airflow container path which we mounted in compoase file
#dag=dag becoz we should pass the instantiated dag as a parameter to link the Operator with the dag.

#task 2: Data cleaning using python Operator
t2 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner, dag=dag)


#task 3: Load the Clean file in MYSQL for loading table is created using DDL command
#mysql_conn_id parameter is a string that will hold reference to a specific MySQL DB we interact like DB connection string

t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table.sql", dag=dag)

# for airflow to fetch the path of sql file using template search path in dag object

t1 >> t2 >> t3