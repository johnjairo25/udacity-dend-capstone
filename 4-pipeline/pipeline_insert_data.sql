---------------------------------------
-- Dimension Tables
---------------------------------------

insert into dim_country(country_code, alpha2_code, short_name, long_name, region, income_group)
  select sc.country_code, sc.alpha_2_code, sc.short_name, sc.long_name, sc.region, sc.income_group
  from staging_country sc
  where sc.country_code is not null;


insert into dim_date(full_date, year, month, day)
  select distinct *
  from (
    select year_month_day,
           cast(substring(year_month_day from 1 for 4) as integer) as year,
           cast(substring(year_month_day from 6 for 2) as integer) as month,
           cast(substring(year_month_day from 9 for 2) as integer) as day
    from staging_global_land_temperatures_by_country coun
    where coun.year_month_day is not null
    union
    select year_month_day,
           cast(substring(year_month_day from 1 for 4) as integer) as year,
           cast(substring(year_month_day from 6 for 2) as integer) as month,
           cast(substring(year_month_day from 9 for 2) as integer) as day
    from staging_global_land_temperatures_by_city city
    where city.year_month_day is not null
  );

---------------------------------------
-- Fact Tables
---------------------------------------

insert into fact_temperatures_by_country(country_code, full_date, avg_temperature, avg_uncertainty)
  select co.country_code, tmp.year_month_day, tmp.average_temperature, tmp.average_temperature_uncertainty
  from staging_global_land_temperatures_by_country tmp
      join dim_country co on (co.short_name = tmp.country)
  where tmp.year_month_day is not null
    and tmp.average_temperature is not null
    and tmp.average_temperature_uncertainty is not null;

insert into fact_temperatures_by_city(city, country_code, full_date, avg_temperature, avg_uncertainty)
  select tmp.city, co.country_code, tmp.year_month_day, tmp.average_temperature, tmp.average_temperature_uncertainty
  from staging_global_land_temperatures_by_city tmp
      join dim_country co on (co.short_name = tmp.country)
  where tmp.year_month_day is not null
    and tmp.average_temperature is not null
    and tmp.average_temperature_uncertainty is not null;

insert into fact_indicators(country_code, indicator_name, indicator_code, value, year)
  select co.country_code, ind.indicator_name, ind.indicator_code, ind.value, ind.year
  from staging_indicators_by_country ind
    join dim_country co on (ind.country_code = co.country_code)
  where ind.indicator_name is not null
    and ind.indicator_code is not null
    and ind.value is not null
    and ind.year is not null;

insert into fact_indicators(country_code, indicator_name, indicator_code, value, year)
  select co.country_code, 'Happiness Score', 'HAP.SCORE', hap.happiness_score, hap.year
  from staging_world_happiness hap
    join dim_country co on (hap.country = co.country_code)
  where hap.year is not null and hap.happiness_score is not null;

insert into fact_indicators(country_code, indicator_name, indicator_code, value, year)
  select co.country_code,
         'Suicides 100k ' || rates.sex || rates.age_range as indicator_name,
         'SUICIDE.100K' as indicator_code,
         rates.suicides_100k as value,
         rates.year
  from staging_suicide_rates rates
    join dim_country co on (rates.country = co.country_code)
  where rates.year is not null and rates.suicides_100k is not null;