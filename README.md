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
pip install -r requirements.txt

# usage python3 covid-producer.py topic myconfig.json
python3 covid-producer.py covid19 aws.json
```

## Confluent Cloud KSQLDB access

ccreate an api-key to the ksqldb application

```bash
ccloud api-key create --resource lksqlc-XXXX

```

output

```txt
It may take a couple of minutes for the API key to be ready.
Save the API key and secret. The secret is not retrievable later.
+---------+------------------------------------------------------------------+
| API Key | xxxxxxxxxxxxxxxx                                                 |
| Secret  | XXXXXX                                                           |
+---------+------------------------------------------------------------------+
```

run curl

```bash
curl -u xxxxx:XXXXXXXXX\
    -X "POST" "https://pksqlc-436o0.us-east-1.aws.confluent.cloud:443/ksql" \
    -H "Accept: application/vnd.ksql.v1+json" \
    -d $'{
    "ksql": "LIST STREAMS;",
    "streamsProperties": {}
}'
```
