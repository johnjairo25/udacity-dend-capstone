---------------------------------------
-- World Development Indicators
---------------------------------------

COPY staging_country
FROM 's3://dend-jjmb/Country.csv'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
CSV QUOTE AS '"'
IGNOREHEADER 1
DELIMITER ','
TRUNCATECOLUMNS;

COPY staging_indicators_by_country
FROM 's3://dend-jjmb/Indicators.csv'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
CSV QUOTE AS '"'
IGNOREHEADER 1
DELIMITER ','
TRUNCATECOLUMNS;

---------------------------------------
-- Suicide Rates
---------------------------------------

COPY staging_suicide_rates
FROM 's3://dend-jjmb/suicide_rates.csv'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
CSV QUOTE AS '"'
IGNOREHEADER 1
DELIMITER ','
TRUNCATECOLUMNS;

---------------------------------------
-- Global Temperatures
---------------------------------------

COPY staging_global_land_temperatures_by_country
FROM 's3://dend-jjmb/GlobalLandTemperaturesByCountry.csv'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
CSV QUOTE AS '"'
IGNOREHEADER 1
DELIMITER ','
TRUNCATECOLUMNS;

COPY staging_global_land_temperatures_by_city
FROM 's3://dend-jjmb/GlobalLandTemperaturesByCity.csv'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
CSV QUOTE AS '"'
IGNOREHEADER 1
DELIMITER ','
TRUNCATECOLUMNS;

---------------------------------------
-- World Happiness Report
---------------------------------------

COPY staging_world_happiness
FROM 's3://dend-jjmb/world-happiness-report.json'
ACCESS_KEY_ID 'YOUR-KEY-ID'
SECRET_ACCESS_KEY 'YOUR-SECRET-ID'
FORMAT AS JSON 'auto';
