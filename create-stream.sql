CREATE STREAM COVID_STREAM (
  body STRUCT<
  	payload STRUCT<
      key VARCHAR,
      value STRUCT<
        NewRecovered INT,
        NewDeaths INT,
        TotalRecovere INT,
        TotalConfirmed INT,
        Country VARCHAR,
        Premium STRUCT<
            FOO VARCHAR
        >,
        ID VARCHAR,
        CountryCode VARCHAR,
        Slug VARCHAR,
        NewConfirmed INT,
        TotalDeaths INT,
        Date VARCHAR
      >,
      timestamp INT,
      "topic" VARCHAR,
      "partition" INT,
      offset BIGINT
  	>
  >
)
 WITH (KAFKA_TOPIC='success-lcc-16n7z',
       VALUE_FORMAT='JSON',
       PARTITIONS=1);