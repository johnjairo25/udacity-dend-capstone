--------------------------------------------------------------------------
-- Average temperature by country in 2010
--------------------------------------------------------------------------

select co.short_name, co.alpha2_code, co.region, avg(tem.avg_temperature) as temperature
from dim_country co
  join fact_temperatures_by_country tem on co.country_code = tem.country_code
  join dim_date da on tem.full_date = da.full_date
where da.year = 2010
group by co.short_name, co.alpha2_code, co.region
order by temperature desc;


--------------------------------------------------------------------------
-- Temperatures in Colombia
--------------------------------------------------------------------------

select co.short_name, da.year, avg(tem.avg_temperature) as temperature
from dim_country co
  join fact_temperatures_by_country tem on co.country_code = tem.country_code
  join dim_date da on tem.full_date = da.full_date
where co.short_name = 'Colombia'
group by co.short_name, da.year
order by da.year desc;

--------------------------------------------------------------------------
-- Hottest Cities in Colombia in 2010
--------------------------------------------------------------------------

select tem.city, avg(tem.avg_temperature) as temperature
from fact_temperatures_by_city tem
  join dim_date da on tem.full_date = da.full_date
where tem.country_code = 'COL' and da.year = 2010
group by tem.city
order by temperature desc
limit 20;

--------------------------------------------------------------------------
-- Coldest Cities in Colombia in 2010
--------------------------------------------------------------------------

select tem.city, avg(tem.avg_temperature) as temperature
from fact_temperatures_by_city tem
  join dim_date da on tem.full_date = da.full_date
where tem.country_code = 'COL' and da.year = 2010
group by tem.city
order by temperature
limit 20;

--------------------------------------------------------------------------
-- Coldest City in Colombia each Year
--------------------------------------------------------------------------

select t1.year, t2.city, t1.min_temp
from
  (select year, min(yearly_temperature) as min_temp
  from
    (select tem.city, da.year,
           avg(tem.avg_temperature) as yearly_temperature
    from fact_temperatures_by_city tem
      join dim_date da on tem.full_date = da.full_date
    where tem.country_code = 'COL'
    group by tem.city, da.year) as temp_by_city_year
  group by year) as t1
join
    (select tem.city, da.year,
           avg(tem.avg_temperature) as yearly_temperature
    from fact_temperatures_by_city tem
      join dim_date da on tem.full_date = da.full_date
    where tem.country_code = 'COL'
    group by tem.city, da.year) as t2
on (t1.year = t2.year and t1.min_temp = t2.yearly_temperature);


--------------------------------------------------------------------------
-- Hottest City in Colombia each Year
--------------------------------------------------------------------------

select t1.year, t2.city, t1.max_temp
from
  (select year, max(yearly_temperature) as max_temp
  from
    (select tem.city, da.year,
           avg(tem.avg_temperature) as yearly_temperature
    from fact_temperatures_by_city tem
      join dim_date da on tem.full_date = da.full_date
    where tem.country_code = 'COL'
    group by tem.city, da.year) as temp_by_city_year
  group by year) as t1
join
    (select tem.city, da.year,
           avg(tem.avg_temperature) as yearly_temperature
    from fact_temperatures_by_city tem
      join dim_date da on tem.full_date = da.full_date
    where tem.country_code = 'COL'
    group by tem.city, da.year) as t2
on (t1.year = t2.year and t1.max_temp = t2.yearly_temperature);

--------------------------------------------------------------------------
-- Which was the happiest country in the world in 2017
--------------------------------------------------------------------------

select dc.short_name, ind.value
from fact_indicators ind
  join dim_country dc on ind.country_code = dc.country_code
where ind.indicator_name = 'Happiness Score' and ind.year = 2017
order by ind.value desc;

--------------------------------------------------------------------------
-- Is the happiness score related to the suicide rate?
--------------------------------------------------------------------------

select happinness_score.year, happinness_score.short_name,
       rate as suicide_rate, score as happiness_score
from
  (select dc.short_name, ind.year, avg(ind.value) as rate
  from fact_indicators ind
    join dim_country dc on ind.country_code = dc.country_code
  where ind.indicator_name like 'Suicides 100k%'
  group by dc.short_name, ind.year) as suicide_rate
join
  (select dc.short_name, ind.year, ind.value as score
  from fact_indicators ind
    join dim_country dc on ind.country_code = dc.country_code
  where ind.indicator_name = 'Happiness Score') as happinness_score
on (suicide_rate.short_name = happinness_score.short_name
      and suicide_rate.year = happinness_score.year)
order by happinness_score.year, happinness_score.score desc;

