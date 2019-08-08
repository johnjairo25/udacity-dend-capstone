---------------------------------------
-- World Development Indicators
---------------------------------------

drop table if exists staging_country;

create table if not exists staging_country(
  country_code varchar(3),
  short_name varchar(128),
  table_name varchar(128),
  long_name varchar(512),
  alpha_2_code varchar(2),
  currency_unit varchar(128),
  special_notes varchar(512),
  region varchar(256),
  income_group varchar(256),
  wb_2_code varchar(2),
  national_accounts_base_year varchar(128),
  national_accounts_reference_year varchar(256),
  sna_price_valuation varchar(512),
  lending_category varchar(32),
  other_groups varchar(32),
  system_of_national_accounts varchar(512),
  alternative_conversion_factor varchar(256),
  ppp_survey_year varchar(128),
  balance_of_payments_manual_in_use varchar(512),
  external_debt_reporting_status varchar(128),
  system_of_trade varchar(128),
  government_accounting_concept varchar(256),
  imf_data_dissemination_standard varchar(256),
  latest_population_census varchar(128),
  latest_household_survey varchar(512),
  source_of_most_recent_income_and_expenditure_data varchar(128),
  vital_registration_complete varchar(512),
  latest_agricultural_census varchar(1024),
  latest_industrial_data varchar(128),
  latest_trade_data varchar(128),
  latest_water_withdrawal_data varchar(128)
);


drop table if exists staging_indicators_by_country;

create table if not exists staging_indicators_by_country(
  country_name varchar(512),
  country_code varchar(3),
  indicator_name varchar(1024),
  indicator_code varchar(64),
  year int,
  value float
);

---------------------------------------
-- Suicide Rates
---------------------------------------

drop table if exists staging_suicide_rates;

create table if not exists staging_suicide_rates(
  idx int,
  country varchar(128),
  year int,
  sex varchar(16),
  age_range varchar(128),
  suicides_no int,
  population int,
  suicides_100k float,
  country_year varchar(128),
  hdi_for_year varchar(128),
  gdp_for_year varchar(128),
  gdp_per_capita int,
  generation varchar(128)
);

---------------------------------------
-- Global Temperatures
---------------------------------------

drop table if exists staging_global_land_temperatures_by_country;

create table if not exists staging_global_land_temperatures_by_country(
  year_month_day varchar(128),
  average_temperature float,
  average_temperature_uncertainty float,
  country varchar(128)
);

drop table if exists staging_global_land_temperatures_by_city;

create table if not exists staging_global_land_temperatures_by_city(
  year_month_day varchar(128),
  average_temperature float,
  average_temperature_uncertainty float,
  city varchar(128),
  country varchar(128),
  latitude varchar(128),
  longitude varchar(128)
);

---------------------------------------
-- World Happiness Report
---------------------------------------

drop table if exists staging_world_happiness;

create table if not exists staging_world_happiness(
  country varchar(128),
  region varchar(256),
  happiness_score float,
  year int
);


