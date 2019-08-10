class SqlQueries:
    """
    Class that defines all the SQL operations to perform data transformation.
    """
    create_staging_country = ("""
        create table staging_country(
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
        )
    """)

    create_staging_indicators_by_country = ("""
        create table staging_indicators_by_country(
          country_name varchar(512),
          country_code varchar(3),
          indicator_name varchar(1024),
          indicator_code varchar(64),
          year int,
          value float
        )
    """)

    create_staging_suicide_rates = ("""
        create table staging_suicide_rates(
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
        )
    """)

    create_staging_global_land_temperatures_by_country = ("""
        create table staging_global_land_temperatures_by_country(
          year_month_day varchar(128),
          average_temperature float,
          average_temperature_uncertainty float,
          country varchar(128)
        )
    """)

    create_staging_global_land_temperatures_by_city = ("""
        create table staging_global_land_temperatures_by_city(
          year_month_day varchar(128),
          average_temperature float,
          average_temperature_uncertainty float,
          city varchar(128),
          country varchar(128),
          latitude varchar(128),
          longitude varchar(128)
        )
    """)

    create_staging_world_happiness = ("""
        create table staging_world_happiness(
          country varchar(128),
          region varchar(256),
          happiness_score float,
          year int
        )
    """)

    create_dim_country = ("""
        create table dim_country(
          country_code varchar(3) primary key,
          alpha2_code varchar(2),
          short_name varchar(128),
          long_name varchar(512),
          region varchar(256),
          income_group varchar(256)
        )
    """)

    create_dim_date = ("""
        create table dim_date(
          full_date varchar(10) primary key,
          year int not null,
          month int not null,
          day int not null
        )
    """)

    create_fact_temperatures_by_country = ("""
        create table if not exists fact_temperatures_by_country(
          id bigint identity(1, 1) primary key,
          country_code varchar(3) not null references dim_country(country_code),
          full_date varchar(10) not null references dim_date(full_date),
          avg_temperature float not null,
          avg_uncertainty float not null
        )
    """)

    create_fact_temperatures_by_city = ("""
        create table if not exists fact_temperatures_by_city(
          id bigint identity(1, 1) primary key,
          city varchar(128) not null,
          country_code varchar(3) not null references dim_country(country_code),
          full_date varchar(10) not null references dim_date(full_date),
          avg_temperature float not null,
          avg_uncertainty float not null
        )
    """)

    create_fact_indicators = ("""
        create table if not exists fact_indicators(
          id bigint identity(1, 1) primary key,
          country_code varchar(3) not null references dim_country(country_code),
          indicator_name varchar(1024) not null,
          indicator_code varchar(64),
          value float not null,
          year int not null
        )
    """)

    insert_dim_country = ("""
        select sc.country_code, sc.alpha_2_code, sc.short_name, sc.long_name, sc.region, sc.income_group
        from staging_country sc
        where sc.country_code is not null
    """)

    insert_dim_date = ("""
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
        )
    """)

    insert_fact_temp_by_country = ("""
        select co.country_code, tmp.year_month_day, tmp.average_temperature, tmp.average_temperature_uncertainty
        from staging_global_land_temperatures_by_country tmp
          join dim_country co on (co.short_name = tmp.country)
        where tmp.year_month_day is not null
        and tmp.average_temperature is not null
        and tmp.average_temperature_uncertainty is not null
    """)

    insert_fact_temp_by_city = ("""
        select tmp.city, co.country_code, tmp.year_month_day, tmp.average_temperature, tmp.average_temperature_uncertainty
        from staging_global_land_temperatures_by_city tmp
          join dim_country co on (co.short_name = tmp.country)
        where tmp.year_month_day is not null
        and tmp.average_temperature is not null
        and tmp.average_temperature_uncertainty is not null
    """)

    insert_fact_indicators = ("""
        select co.country_code, ind.indicator_name, ind.indicator_code, ind.value, ind.year
        from staging_indicators_by_country ind
            join dim_country co on (ind.country_code = co.country_code)
        where ind.indicator_name is not null
            and ind.indicator_code is not null
            and ind.value is not null
            and ind.year is not null
    """)

    insert_fact_indicators_with_happiness = ("""
        select co.country_code, 'Happiness Score', 'HAP.SCORE', hap.happiness_score, hap.year
        from staging_world_happiness hap
            join dim_country co on (hap.country = co.country_code)
        where hap.year is not null and hap.happiness_score is not null
    """)

    insert_fact_indicators_with_suicides = ("""
        select co.country_code,
             'Suicides 100k ' || rates.sex || rates.age_range as indicator_name,
             'SUICIDE.100K' as indicator_code,
             rates.suicides_100k as value,
             rates.year
        from staging_suicide_rates rates
            join dim_country co on (rates.country = co.country_code)
        where rates.year is not null and rates.suicides_100k is not null
    """)
