---------------------------------------
-- Dimension Tables
---------------------------------------

drop table if exists dim_country;

create table if not exists dim_country(
  country_code varchar(3) primary key,
  alpha2_code varchar(2),
  short_name varchar(128),
  long_name varchar(512),
  region varchar(256),
  income_group varchar(256)
);

drop table if exists dim_date;

create table if not exists dim_date(
  full_date varchar(10) primary key,
  year int not null,
  month int not null,
  day int not null
);

---------------------------------------
-- Fact Tables
---------------------------------------

drop table if exists fact_temperatures_by_country;

create table if not exists fact_temperatures_by_country(
  id bigint identity(1, 1) primary key,
  country_code varchar(3) not null references dim_country(country_code),
  full_date varchar(10) not null references dim_date(full_date),
  avg_temperature float not null,
  avg_uncertainty float not null
);

drop table if exists fact_temperatures_by_city;

create table if not exists fact_temperatures_by_city(
  id bigint identity(1, 1) primary key,
  city varchar(128) not null,
  country_code varchar(3) not null references dim_country(country_code),
  full_date varchar(10) not null references dim_date(full_date),
  avg_temperature float not null,
  avg_uncertainty float not null
);

drop table if exists fact_indicators;

create table if not exists fact_indicators(
  id bigint identity(1, 1) primary key,
  country_code varchar(3) not null references dim_country(country_code),
  indicator_name varchar(1024) not null,
  indicator_code varchar(64),
  value float not null,
  year int not null
);
