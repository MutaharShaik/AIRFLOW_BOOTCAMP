"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""


# Importing the required libraries
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta                          #schedule interval,start date, end date,

#defining the default arguments dictionary
default_args = {                                 # dictonary of arguemnts applicable to all operators that are defined in the DAG
    "owner": "airflow",                                 #owner name
    "depends_on_past": False,                           #it is a key , depends_on_past=is a boolean field that specifies whether a task in current DAG <depends on the corresponding task> in older DAG runs.
    "start_date": datetime(2022, 7, 22),                 # if it is set to true then it will not allow templated task from getting triggered today if it is faied yesterday.
    "email": ["airflow@airflow.com"],                     # if it is false then there is no such task succeed dependency.
    "email_on_failure": False,                              # to send the notifications of ststus of task if its failed.
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),               # tme gap betwwen the retry
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

# Instantiate a DAG object
dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(1))        # Instatntiating a DAG object: import DAG is used here and nest our tasks in to this DAG object.
# "tutorial"----- DAG ID (unique identifier for the DAG)   default_args=default_args---- pass all the are default args dict to each task constructor.        schedule_interval=timedelta(1)-----it means tutoril DAG run everyday.

# task creation part
# t1, t2 and t3 are examples of tasks created by instantiating operators( ex: bash operator)
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)    # taskID is 1st mandatory arg , bash_command="date"= command or script that are going to run as part of this task, last arg is the instantitated dag itself

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)          # retries=3 this will override the <"retries": 1> defined in the default dictionary

templated_command = """                           # Here we using Ginja template. Airflow leveraged the power of jinja templating for passing dynamic info in to task instances at runtime.
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)
# setting the dependecies among the task is pending
# since our tasks has no dependencies
# this is crucial in ETL pipeline, we  set task dependencies  where we run Extraction task first, then transformation task and then loading task
# there ar 2 types of dependecies 1. Upstream {syntax:task2.set_upstream(t1)}
#                             and 2. Downstream  {syntax:task2.set_downstream(t1)}
# or using  python bitshift operators<<,>>
t2.set_upstream(t1)
t3.set_upstream(t1)
