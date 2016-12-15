--The 3 queries below represent the percent difference in rent when comparing rents from 2014 to 2009, across the median, upper and lower brackets.
--The yoy_pct_diff column in each of the queries below is the year over year difference in rent. At this point we are not planning on using column.
--The diff column is the percent difference when comparing rents in 2014 to rents in 2009. Each of the years from 2009 to 2014 will store the same data.
--Once our properties have the geocoded values, they will be able to join to each of these queries by geo_id2, and pulling this data for each property.

--"percent_increase_neighborhood_median_rent"
select b.*,  --round(cast ((est_rent - lag (est_rent, 1, est_rent) over ( partition by geo_id2 order by year asc))/est_rent*100 as numeric), 2) as yoy_pct_diff,
round (( first_value (est_rent) over ( partition by geo_id2 order by year desc)
- first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent) over ( partition by geo_id2 order by year asc)*100, 2) as diff
  from (
select case when snapshot_id = 	'ACS_09_5YR_B25058_with_ann.csv' then 2009
            when snapshot_id = 'ACS_10_5YR_B25058_with_ann.csv' then 2010
            when snapshot_id = 'ACS_11_5YR_B25058_with_ann.csv' then 2011
            when snapshot_id = 'ACS_12_5YR_B25058_with_ann.csv' then 2012
            when snapshot_id = 'ACS_13_5YR_B25058_with_ann.csv' then 2013
            when snapshot_id = 'ACS_14_5YR_B25058_with_ann.csv' then 2014
       end as year, a.geo_id2, a."geo_display-label" as display, cast (a.hd01_vd01 as numeric) est_rent, hd02_vd01 margin_of_error
  from acs_rent_median a
 where geo_Id2 = '01001020100'
 ) b
order by year asc

--"percent_increase_neighborhood_lower_rent"
select b.*,  --round(cast ((est_rent - lag (est_rent, 1, est_rent) over ( partition by geo_id2 order by year asc))/est_rent*100 as numeric), 2) as yoy_pct_diff,
round (( first_value (est_rent) over ( partition by geo_id2 order by year desc)
- first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent) over ( partition by geo_id2 order by year asc)*100, 2) as diff
  from (
select case when snapshot_id = 	'ACS_09_5YR_B25057_with_ann.csv' then 2009
            when snapshot_id = 'ACS_10_5YR_B25057_with_ann.csv' then 2010
            when snapshot_id = 'ACS_11_5YR_B25057_with_ann.csv' then 2011
            when snapshot_id = 'ACS_12_5YR_B25057_with_ann.csv' then 2012
            when snapshot_id = 'ACS_13_5YR_B25057_with_ann.csv' then 2013
            when snapshot_id = 'ACS_14_5YR_B25057_with_ann.csv' then 2014
       end as year, a.geo_id2, a."geo_display-label" as display, cast (a.hd01_vd01 as numeric) est_rent, hd02_vd01 margin_of_error, snapshot_id
  from acs_rent_lower a
 where geo_Id2 = '01001020100'
 ) b
order by year asc


--"percent_increase_neighborhood_upper_rent"
select b.*,  
--round(cast ((est_rent - lag (est_rent, 1, est_rent) over ( partition by geo_id2 order by year asc))/est_rent*100 as numeric), 2) as yoy_pct_diff,
round (( first_value (est_rent) over ( partition by geo_id2 order by year desc)
- first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent) over ( partition by geo_id2 order by year asc)*100, 2) as diff
  from (
select case when snapshot_id = 	'ACS_09_5YR_B25059_with_ann.csv' then 2009
            when snapshot_id = 'ACS_10_5YR_B25059_with_ann.csv' then 2010
            when snapshot_id = 'ACS_11_5YR_B25059_with_ann.csv' then 2011
            when snapshot_id = 'ACS_12_5YR_B25059_with_ann.csv' then 2012
            when snapshot_id = 'ACS_13_5YR_B25059_with_ann.csv' then 2013
            when snapshot_id = 'ACS_14_5YR_B25059_with_ann.csv' then 2014
       end as year, a.geo_id2, a."geo_display-label" as display, cast (a.hd01_vd01 as numeric) est_rent, hd02_vd01 margin_of_error, snapshot_id
  from acs_rent_upper a
 where geo_Id2 = '01001020100'
 ) b
order by year asc

