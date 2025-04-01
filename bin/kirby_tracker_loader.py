#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""This program is used to read, transform and load data from google sheet to local postgresql database"""
# connect to excel spreadsheet and read data
# connect to postgresql and incrementally load data to postgresql


# In[7]:


import os.path
from datetime import datetime
import logging
import configparser
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import warnings

root_dir = r'/Users/yi-ninghuang/Documents/Python_Project/'

# set up a global logger
ts = datetime.now().strftime('%Y%m%d')
log_file = os.path.join(root_dir, "log", f"kirby_tracker_loader_{ts}.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Capture system-generated warnings
logging.captureWarnings(True)
if not logger.hasHandlers():
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    logger.addHandler(fh)
    formatter = logging.Formatter(
                "{asctime} - {name} - {levelname} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M"
                )
    fh.setFormatter(formatter)

# In[8]:


def read_from_excel_sheet():
    """
    This function is used to extract all activity data from the excel sheet
    """
    dat_path = os.path.join(root_dir, 'dat', 'Kirby_Tracker.xlsx')
    df = pd.read_excel(dat_path, sheet_name = 'activity_tracker', usecols="A:D")
    return df


# In[9]:


def get_postgresql_credential():
    config = configparser.ConfigParser()
    config.read(os.path.join(root_dir, 'config', 'postgresql.ini'))

    db_host = config['default']['host']
    db_port = config['default']['port']
    db_name = config['credentials']['dbname']
    db_user = config['credentials']['username']
    db_password = config['credentials']['password']
    db_schema = 'kirby'
    db_table = 'activity'
    
    return db_host, db_port, db_name, db_user, db_password, db_schema, db_table

# In[10]:
def get_postgresql_credential():
    """
    This function is used to extract the login credentials of postgresql database from config file for security
    """
    config = configparser.ConfigParser()
    config.read(os.path.join(root_dir, 'config', 'postgresql.ini'))

    db_host = config['default']['host']
    db_port = config['default']['port']
    db_name = config['credentials']['dbname']
    db_user = config['credentials']['username']
    db_password = config['credentials']['password']
    db_schema = 'kirby'
    db_table = 'fact_activity'
    
    return db_host, db_port, db_name, db_user, db_password, db_schema, db_table


# In[11]:
def transform_load_to_postgresql(df, db_host, db_port, db_name, db_user, db_password, db_schema, db_table):
    """
    This function is used to connect to postgresql database and perform etl to target table
    """
    
    # connect to postgres db
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    query = f"select max(act_datetime) as max_act_datetime from postgres.kirby.fact_activity;"

    with engine.connect() as conn:
        result = conn.execute(query).scalar()

    max_act_datetime_tgt = pd.to_datetime(result)
    logger.info("Max Datetime from PostgreSQL:  {}".format(max_act_datetime_tgt))
    
    df = df.dropna(subset=["start_time"])
    df["act_dt"] = pd.to_datetime(df["date"].astype(str) + " " + df["start_time"].astype(str))
    max_act_datetime_src = df["act_dt"].max()
    logger.info("Max Datetime from Excel Sheet: {}".format(max_act_datetime_src))
    inc_df = df[df["act_dt"] > max_act_datetime_tgt]
    inc_df = inc_df[["activity", "act_dt", "note"]]

    inc_df = inc_df.rename(columns={"act_dt":"act_datetime"})
    inc_df["insert_datetime"] = datetime.now()
    inc_df["insert_process"] = "kirby_tracker_loader.py"
    
    if inc_df.empty:
        logger.info(f"No new data is found.")
    else:
        logger.info(str(inc_df.shape[0]) + " new rows identified")
        inc_df.to_sql(db_table, engine, schema="kirby", if_exists="append", index=False)
        logger.info(f"Data loaded into PostgreSQL table '{db_table}' successfully.")
        
        logger.info(f"Starting to populate indicators...")
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            result = session.execute("CALL kirby.sp_update_potty_indicators()")
            session.commit()
            logger.info(f"Potty indicators are updated successfully.")
        except Exception as e:
            logger.error(f"Error: {e}")
            session.rollback()
        finally:
            session.close()
        

# In[ ]:
def get_today_run_count():
    if not os.path.exists(log_file):
        return 1
    with open(log_file, "r") as f:
        lines = f.readlines()
    run_count = sum("Run #" in line for line in lines)
    return run_count + 1

# In[ ]:


def main():
    # main
    run_count = get_today_run_count()
    logger.info(f"===================== Run # {run_count} ====================")
    logger.info("Starting to fetch config")
    # config
    db_host, db_port, db_name, db_user, db_password, db_schema, db_table = get_postgresql_credential()
    logger.info("The config is fetched")
    # read
    logger.info("Starting the read process")
    df = read_from_excel_sheet()
    logger.info("The read process is complete")
    # load
    logger.info("Starting the load process")
    transform_load_to_postgresql(df, db_host, db_port, db_name, db_user, db_password, db_schema, db_table)
    logger.info("The load process is complete")


# In[ ]:


if __name__ == "__main__":
    main()

