### Running the Market Data Download Pipeline
######
- This guide will walk you through the steps to run the Python code `market_data_download.py`, which orchestrates a DAG creation and crating a data pipeline workflow using Apache Airflow. 
- The pipeline downloads market data for specific stocks using Yahoo Finance's Python library (pre-requisite) and orchestrates the process using multiple Airflow operators.
- This project orchestrates setting up order of operation of each task in the python code. This project helped me gain familiarity with how to use Apache Airflow to automate data pipelining tasks.

#### Prerequisites

1. **Install Apache Airflow:** Follow the [official installation guide](http://airflow.apache.org/docs/stable/installation.html) to install Apache Airflow on your local machine.

2. **Install Required Python Libraries:**
   - Install Yahoo Finance library:
     ```bash
     pip install yfinance
     ```
   - Install pandas library:
     ```bash
     pip install pandas
     ```
#### Setup Steps

1. **Activate Virtual Environment (Optional):**
   If you're using a virtual environment to run Airflow, activate it using the following command:
   ```bash
   source ~/install/airflow-tutorial/airflow_venv/bin/activate

2. **Create Storage Directories:**
   Create the necessary storage directories for Airflow:
   ```bash
   mkdir -p ~/install/airflow-tutorial/airflow
3. **Set Environment Variables:**
   Set the AIRFLOW_HOME environment variable to the Airflow storage directory:
   ``` bash
   export AIRFLOW_HOME=~/install/airflow-tutorial/airflow

4. **Initialize Metadata:**
   Navigate to the Airflow storage directory and initialize the metadata:
   ```bash
   cd ${AIRFLOW_HOME}
   airflow db init
5. **Start Airflow Scheduler and Webserver:**
   Start the Airflow scheduler and webserver processes.
   The scheduler process will run in the background, while the webserver process will serve the Airflow UI.
   ```bash
   airflow scheduler -D
   sudo airflow webserver --port 8080 -D
   ```
   Replace 8080 with the desired port number. Ensure that the port is not already in use.
  
6. **Access Airflow UI:**

     Open a web browser and navigate to http://localhost:8080/ to access the Airflow UI. Log in using your Airflow username and password.
   
8. **Run the Pipeline:**
  - Place the market_data_download.py file in the Airflow DAGs directory (usually ${AIRFLOW_HOME}/dags).
  - After logging in to the Airflow UI, you should see the market_data_download DAG listed. Toggle the DAG to ON to start scheduling it.
  - Once the DAG is triggered, Airflow will execute the tasks defined in the DAG, orchestrating the market data download process.

**Notes:**
  - Ensure that you have configured Airflow correctly and have the necessary permissions to run the DAGs.
  - Modify the file paths and environment variables as needed to match your setup.
  - Make sure to replace placeholder values (such as <username> and <repository_name>) with your actual values.
  
