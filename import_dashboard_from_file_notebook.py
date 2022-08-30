# Databricks notebook source
import argparse
from utils import clone_dashboard
from utils.load_dashboard import load_dashboard
from utils.client import Client
import json

# COMMAND ----------

def get_client(config_file,pat_token):
    with open(config_file, "r") as r:
        config = json.loads(r.read())
        targets = []
        for target in config["targets"]:
            print("Token ->("+pat_token+")")
            client = Client(target["url"], pat_token, permissions=target["permissions"])
            if "endpoint_id" in target:
                client.endpoint_id = target["endpoint_id"]
            if "sql_database_name" in target:
                client.sql_database_name = target["sql_database_name"]
            targets.append(client)
        return  targets,config["dashboard_id"],  config["dashboard_folder"]




# COMMAND ----------

target_clients, dashboard_id_to_load,dashboard_folder  = get_client("config_import.json", dbutils.secrets.get('swat_masterscp', 'sat_token'))
workspace_state = {}
load_dashboard(target_clients[0], dashboard_id_to_load, workspace_state, dashboard_folder)
