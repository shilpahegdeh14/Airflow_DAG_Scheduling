from airflow import DAG
from datetime import timedelta, datetime, date
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import yfinance as yf
import pandas as pd

default_args ={
    'owner':'airflow',
    'start_date': datetime(2024, 5, 2)
}

# Creating DAG object
dag = DAG(dag_id='marketvol',
          default_args=default_args,
          description='A simple DAG',
          schedule=timedelta(days=1))

# Creating a BashOperator task to initialize a temporary directory for data download (t0)
t0 = BashOperator(
    task_id='t0',
    bash_command='mkdir -p /Documents/Data_Engineer_BootCamp_Projects/apache_airflow/{{ execution_date.strftime("%Y-%m-%d") }}',  # Use execution_date to get the date
    dag=dag
)

# Define the function to download market data
def download_market_data(stock_symbol, **kwargs):
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    df = yf.download(stock_symbol, start=start_date, end=end_date, interval='1m')
    df.to_csv(f"{stock_symbol}_data.csv", header=False)

# Define the PythonOperator tasks to download market data for AAPL and TSLA
t1 = PythonOperator(
    task_id='download_AAPL_data',
    python_callable=download_market_data,
    op_args=['AAPL'],
    dag=dag
)

t2 = PythonOperator(
    task_id='download_TSLA_data',
    python_callable=download_market_data,
    op_args=['TSLA'],
    dag=dag
)

# Create BashOperator tasks to move the downloaded files to the designated location
# mv [source_file_name][destination_file_name]
t3 = BashOperator(
    task_id='move_AAPL_file',
    bash_command='mv /Documents/Data_Engineer_BootCamp_Projects/apache_airflow/{{ execution_date.strftime("%Y-%m-%d") }}/AAPL_data.csv /Documents/Data_Engineer_BootCamp_Projects/apache_airflow/AAPL',
    dag=dag
)

t4 = BashOperator(
    task_id='move_TSLA_file',
    bash_command='mv /Documents/Data_Engineer_BootCamp_Projects/apache_airflow/{{ execution_date.strftime("%Y-%m-%d") }}/TSLA_data.csv /Documents/Data_Engineer_BootCamp_Projects/apache_airflow/TSLA',
    dag=dag
)

def run_query(**kwargs):
    # use pandas to read the CSV files and perform the query
    AAPL_data = pd.read_csv('/Documents/Data_Engineer_BootCamp_Projects/apache_airflow/AAPL/AAPL_data.csv')
    TSLA_data = pd.read_csv('/Documents/Data_Engineer_BootCamp_Projects/apache_airflow/TSLA/TSLA_data.csv')
    
    # Perform your query
    # For example, reading the head
    AAPL_head = AAPL_data.head()
    TSLA_head = TSLA_data.head()
    
    # Print the results or do further processing
    print("AAPL first n rows:", AAPL_head)
    print("TSLA first n rows:", TSLA_head)

# Define the PythonOperator task to run the query
t5 = PythonOperator(
    task_id='run_query',
    python_callable=run_query,
    dag=dag
)
# Set the task dependencies
t0 >> [t1, t2]
t1 >> t3
t2 >> t4
[t3, t4] >> t5