/*Only run when using from SQL editor, drop is done separately when run from Python*/
--drop table decisions;

create table decisions
as
------------------
--This is the query that returns decisions
------------------
--Choose which tests we want to use to create decisions
/*
previous_churn_decisions:  Number of times there was previously an 'out' decision that was reverted
churn_flag, 	 When previous most_recent_decision was out (1) and current most_recent_decision is in (2), add an 'X'
previous_contract_term_months_qty, variable name explains it
most_recent_decision, ???
cnt_d, Total count of the number of times the contract duration has changed
in_out_dec_cnt, Total count of decisions that have occurred, either direction, over the whole life of the contract
in_out_dec_flg, 1='out', 2='in' in the decision column
term_mths_diff_flg, 'X' when the previous contract term is not the same as current
decision, 'in', 'out', 'suspicious', or 'first' depending on the decision_tests
*/

select count( churn_flag ) over ( partition by contract_number ) as previous_churn_decisions
       , d.*
       from (
            select
              case when
                --'X' is an indicator of a churn decision
                  lag ( most_recent_decision ) over ( partition by contract_number order by snapshot_id ) = 1
                  and most_recent_decision = 2 then 'X'
                  end as churn_flag

              , first_value (term_mths_lag)
                    over ( partition by contract_number, contract_term_months_qty, cnt_d
                          order by snapshot_id RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING )
                as previous_contract_term_months_qty
       , c.*
          from (
          select max ( in_out_dec_flg)
          over ( partition by contract_number, in_out_dec_cnt order by snapshot_id )
          most_recent_decision
          ,
--Count the number of instances where there.
       count (term_mths_diff_flg) over (partition by contract_number order by snapshot_id) as cnt_d, b.*
from (
--Flag the 'out' and 'in' decisions as 1 and 2 respectively. All other fields will be left blank.
--Count the number of 'out' and 'in' instances per contract_number. The count increments each time a new instance of 'out' or 'in' is encountered.
--This count also is an easy way to create partitions by count that can be used further above.
select count( case decision when 'out' then 1
                            when 'in'  then 2
							else null
			end ) over ( partition by contract_number order by snapshot_id ) as in_out_dec_cnt,
              case decision when 'out' then 1
                            when 'in'  then 2
							else null
			end as in_out_dec_flg,
-- if the prior contract term months does not equal the current contract term months, flag that record. This flag will be used
-- in the outer query above this one to count the number of records up to the point that a 'X' is encountered.
--When the 'X' is encountered, the count will go up.
			case when term_mths_lag != contract_term_months_qty then 'X' else null end as term_mths_diff_flg, a.*
  from (
SELECT
	--Compare tests to decide the decision
	CASE
		WHEN (expiration_extended_test = 'extended'
		  AND status_test = 'no change'
		  AND TRIM(c.tracs_status_name) = 'Active')
		  THEN 'in'
		WHEN status_test = 'restored'
		  AND TRIM(c.tracs_status_name) = 'Active'
		  THEN 'in'
		WHEN status_test = 'out' THEN 'out'
		WHEN expiration_extended_test = 'no change'
		  AND status_test = 'no change'
		  THEN 'no change'
		WHEN expiration_extended_test = 'first'
		  and status_test = 'first'
		  THEN 'first'
		ELSE 'suspicious'
	  END AS decision
 	, decisions_tests.snapshot_id
	, decisions_tests.contract_number
    , c.property_id	--status tests
-- get the previous contract term months within a contract ordered by the snapshot id
    , lag(c.contract_term_months_qty,1) over (partition by c.contract_number order by c.snapshot_id) term_mths_lag
    , c.contract_term_months_qty
    , null rent_gross_amount_per_unit
    , coalesce (case when c.assisted_units_count = 0 then null else (c."0br_count" / c.assisted_units_count) end, 0) as br0_perc
    , coalesce (case when c.assisted_units_count = 0 then null else (c."1br_count" / c.assisted_units_count) end, 0) as br1_perc
    , coalesce (case when c.assisted_units_count = 0 then null else (c."2br_count" / c.assisted_units_count) end, 0) as br2_perc
    , coalesce (case when c.assisted_units_count = 0 then null else (c."3br_count" / c.assisted_units_count) end, 0) as br3_perc
    , coalesce (case when c.assisted_units_count = 0 then null else (c."4br_count" / c.assisted_units_count) end, 0) as br4_perc
    , coalesce (case when c.assisted_units_count = 0 then null else (c."5plusbr_count" / c.assisted_units_count) end, 0) as br5_perc

--     , ( select round ( ( first_value (est_rent) over ( partition by geo_id2 order by year desc)
--              - first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent)
-- 			 over ( partition by geo_id2 order by year asc)*100, 2) as diff
--   from (
-- 		select
--          case when c.snapshot_id = 	'ACS_09_5YR_B25058_with_ann.csv' then 2009
  -- 					when c.snapshot_id = 'ACS_10_5YR_B25058_with_ann.csv' then 2010
  -- 					when c.snapshot_id = 'ACS_11_5YR_B25058_with_ann.csv' then 2011
  -- 					when c.snapshot_id = 'ACS_12_5YR_B25058_with_ann.csv' then 2012
  -- 					when c.snapshot_id = 'ACS_13_5YR_B25058_with_ann.csv' then 2013
  -- 					when c.snapshot_id = 'ACS_14_5YR_B25058_with_ann.csv' then 2014
  -- 			  end as year
--        , a.geo_id2
--        , a."geo_display-label" as display
--        , cast (a.hd01_vd01 as numeric) est_rent
--        , hd02_vd01 margin_of_error
-- 		 from acs_rent_median a, geocode g
-- 		 where a.geo_id2 = trim (cast (g.geoid as text))
-- 		   and g.property_id = c.property_id limit 1 --Needs to be changed!!!!! Join to geocode.
--         ) b )
--      as percent_increase_neighborhood_median_rent


--     , ( select round (( first_value (est_rent) over ( partition by geo_id2 order by year desc)
--              - first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent)
-- 			 over ( partition by geo_id2 order by year asc)*100, 2) as diff
--   from (
-- 		select case when snapshot_id = 	'ACS_09_5YR_B25059_with_ann.csv' then 2009
-- 					when snapshot_id = 'ACS_10_5YR_B25059_with_ann.csv' then 2010
-- 					when snapshot_id = 'ACS_11_5YR_B25059_with_ann.csv' then 2011
-- 					when snapshot_id = 'ACS_12_5YR_B25059_with_ann.csv' then 2012
-- 					when snapshot_id = 'ACS_13_5YR_B25059_with_ann.csv' then 2013
-- 					when snapshot_id = 'ACS_14_5YR_B25059_with_ann.csv' then 2014
-- 			   end as year, a.geo_id2, a."geo_display-label" as display, cast (a.hd01_vd01 as numeric) est_rent, hd02_vd01 margin_of_error, snapshot_id
-- 		  from acs_rent_upper a
-- 		 where geo_Id2 = '01001020100'
-- 		) b )

--    , null as percent_increase_neighborhood_upper_rent
--     , ( select round (( first_value (est_rent) over ( partition by geo_id2 order by year desc)
--                - first_value (est_rent) over ( partition by geo_id2 order by year asc) ) / first_value (est_rent)
-- 			   over ( partition by geo_id2 order by year asc)*100, 2) as diff
--   from (
-- 		select case when snapshot_id = 	'ACS_09_5YR_B25057_with_ann.csv' then 2009
-- 					when snapshot_id = 'ACS_10_5YR_B25057_with_ann.csv' then 2010
-- 					when snapshot_id = 'ACS_11_5YR_B25057_with_ann.csv' then 2011
-- 					when snapshot_id = 'ACS_12_5YR_B25057_with_ann.csv' then 2012
-- 					when snapshot_id = 'ACS_13_5YR_B25057_with_ann.csv' then 2013
-- 					when snapshot_id = 'ACS_14_5YR_B25057_with_ann.csv' then 2014
-- 			   end as year, a.geo_id2, a."geo_display-label" as display, cast (a.hd01_vd01 as numeric) est_rent, hd02_vd01 margin_of_error, snapshot_id
-- 		  from acs_rent_lower a
-- 		 where geo_Id2 = '01001020100'
-- 		) b )
--     , null as percent_increase_neighborhood_lower_rent

--     , null ratio_neighborhood_median_to_gross_rent
--     , null ratio_neighborhood_lower_to_gross_rent
--     , null ratio_neighborhood_upper_to_gross_rent

FROM decisions_tests
INNER JOIN contracts c
ON decisions_tests.contract_number = c.contract_number
  AND decisions_tests.snapshot_id = c.snapshot_id
) a ) b ) c ) d
where decision != 'no change'
