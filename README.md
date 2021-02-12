# Covid demo with aws lambda & ksqlDB

Python producer sending COVID 19 stats from covid19api.com. 

Config

```json
{
    "bootstrap.servers": "your-confluent-cloud-bootstrap-server:9092",
    "sasl.mechanisms":"PLAIN",
    "security.protocol":"SASL_SSL",
    "sasl.username":"key",
    "sasl.password":"secret",
    "schema.registry.url":"https://your-schema-registry.confluent.cloud",
    "basic.auth.credentials.source":"USER_INFO",
    "basic.auth.user.info":"sr-key:sr-secret"
}
```

```bash
pip install requirements.txt

# usage python3 covid-producer.py topic myconfig.json
python3 covid-producer.py covid19 aws.json
```
