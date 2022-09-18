import os
import logging
import yaml
from libpurecoollink.dyson import DysonAccount
from elasticsearch import Elasticsearch

print("Starting up environmental data recorder")

logging.basicConfig(level=logging.DEBUG)

# Setup Dyson
# Read configuration from ENV_VARs
dyson_email = os.getenv("DYSON_EMAIL_ADDRESS", "whoever@example.com")
dyson_token = os.getenv("DYSON_TOKEN")

dyson_account = DysonAccount(dyson_email, None, "US")
if dyson_token and dyson_token != '':
    dyson_account.use_authentication_token(dyson_token)

# Setup Elasticsearch
# Elasticsearch configuration
elasticsearch_url = os.getenv("ELASTIC_URL", "https://elasticsearch:9200")
elasticsearch_username = os.getenv("ELASTIC_USERNAME", "elastic")
elasticsearch_password = os.getenv("ELASTIC_PASSWORD", "dontcare")

try:
    # Create connection with Elasticsearch
    es = Elasticsearch(
        elasticsearch_url,
        ca_certs="/app/certs/ca/ca.crt",
        basic_auth=(elasticsearch_username, elasticsearch_password)
    )
except:
    print("Failed to initialize Elasticsearch client, cannot proceed")
    print("Sit here and wait so we don't hammer Elasticsearch")
    for i in range(30):
        time.sleep(1)
    exit(1)

# Read which devices we want to interact with
with open("devices.yml", "r") as stream:
    try:
        device_list = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("Couldn't read YAML config")
        print(exc)
        exit(1)

devices = dyson_account.devices()

print(devices)

for iterator, device in enumerate(device_list["devices"]):
    devices[iterator].connect(device['fqdn'])
    print(devices[iterator].environmental_state)
