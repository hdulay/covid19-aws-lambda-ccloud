import requests
import json
import time
import sys
import traceback
from confluent_kafka import Producer
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

def delivery_report(self, msg = None, err = None):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send(p, js, topic):
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0.0)
    # Generate Key
    key = "{country}".format(country=js['Country'])
    print(key)
    # json
    value = json.dumps(js)
    print(value)
    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce(topic=topic, value=js, on_delivery=delivery_report, key=key)
    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    p.flush()

def poll(url, topic, p):
    response = requests.get(url)
    try:
        results = json.loads(response.text)
        for j in results['Countries']:
            print(j)
            send(p, j, topic)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()

def main():
    config_file = sys.argv[2]
    url = 'https://api.covid19api.com/summary'
    topic = sys.argv[1]
    with open(config_file) as f:
        config = json.load(f)
    p = MyProducer(config)

    while True:
        poll(url, topic, p)
        time.sleep(5)

# generate producer
def MyProducer(config):
    schema_str = """
    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "covid",
        "type": "object",
        "properties": {
            "ID": {
                "type": "string"
            },
            "Country": {
                "type": "string"
            },
            "CountryCode": {
                "type": "string"
            },
            "Slug": {
                "type": "string"
            },
            "NewConfirmed": {
                "type": "integer"
            },
            "TotalConfirmed": {
                "type": "integer"
            },
            "NewDeaths": {
                "type": "integer"
            },
            "TotalDeaths": {
                "type": "integer"
            },
            "NewRecovered": {
                "type": "integer"
            },
            "TotalRecovered": {
                "type": "integer"
            },
            "Date": {
                "type": "string"
            },
            "Premium": {
                "type": "object"
            }
        },
        "required": [
            "ID",
            "Country",
            "CountryCode",
            "Slug",
            "NewConfirmed",
            "TotalConfirmed",
            "NewDeaths",
            "TotalDeaths",
            "NewRecovered",
            "TotalRecovered",
            "Date",
            "Premium"
        ]
    }
    """
    schema_registry_conf = {
        'url': config["schema.registry.url"],
        'basic.auth.user.info': config['basic.auth.user.info']
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    jsons = JSONSerializer(schema_str, schema_registry_client, lambda f,ctx:f)

    producer_conf = {
        'bootstrap.servers': config['bootstrap.servers'],
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': jsons,
        'security.protocol': config["security.protocol"],
        "sasl.mechanisms":config["sasl.mechanisms"],
        "sasl.username":config["sasl.username"],
        "sasl.password":config["sasl.password"]
    }

    return SerializingProducer(producer_conf)

if __name__== "__main__":
    main()