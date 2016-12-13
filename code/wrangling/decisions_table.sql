drop table decisions;

create table decisions
as
	/*
	--------------------------
	contract_number_queries
	These are virtual tables we can plug into the 'where in(virtual_table)' statement to filter down to only some contracts. 
	--------------------------*/
	WITH

	contracts_earliest100 AS (
	SELECT contract_number
		FROM contracts
		GROUP BY contract_number
		ORDER BY MIN(tracs_overall_expiration_date) ASC
		LIMIT 100
	)

	, contracts_latest100 AS (
	SELECT contract_number		--, MIN(tracs_overall_expiration_date) 
		FROM contracts
		GROUP BY contract_number
		ORDER BY MIN(tracs_overall_expiration_date) DESC
		LIMIT 100
	)

	, contracts_random200 AS (
	SELECT contract_number
	FROM	(
		SELECT contract_number, MIN(tracs_overall_expiration_date) AS earliest_expiration
			FROM contracts
			GROUP BY contract_number
			LIMIT 200
		) as random_unsorted
	ORDER BY earliest_expiration
	)

	--This one can't be used by itself b/c of the select date
	, all_contracts_sorted AS (
	SELECT    contract_number 
		, MIN(tracs_overall_expiration_date) AS earliest_expiration
	FROM contracts
	GROUP BY contract_number
	ORDER BY MIN(tracs_overall_expiration_date) ASC
)

	--This is a way to paginate our results so that we can split our contracts into multiple files
	, contracts_500_1 AS (
	SELECT contract_number
	FROM (
		SELECT  ROW_NUMBER() OVER ( ORDER BY earliest_expiration ) AS rownum
			, contract_number
			, earliest_expiration
		FROM all_contracts_sorted
		) AS row_number_added
	WHERE   rownum >= 1
	    AND rownum <= 500 
	ORDER BY RowNum
	)

	, contracts_500_2 AS (
	SELECT contract_number
	FROM (
		SELECT  ROW_NUMBER() OVER ( ORDER BY earliest_expiration ) AS rownum
			, contract_number
			, earliest_expiration
		FROM all_contracts_sorted
		) AS row_number_added
	WHERE   rownum >= 501
	    AND rownum <= 1000 
	ORDER BY RowNum
	)

	/*
	--------------------------
	end of contract_number_queries
	--------------------------*/

--Query to view the decision_tests table
/*
SELECT * 
FROM decisions_tests
WHERE contract_number IN ( select * from contracts_random100)
*/


------------------
--This is the query that returns decisions
------------------
--Choose which tests we want to use to create decisions
select count( dec1 ) over ( partition by contract_number ) as previous_churn_decisions, d.* from (
select case when lag ( max_d ) over ( partition by contract_number order by snapshot_id ) = 1 and max_d = 2 then 'X' end as dec1, 
first_value (lag_qty) over (partition by contract_number, contract_term_months_qty, cnt_d order by snapshot_id RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING ) as previous_contract_term_months_qty, c.*
from (
select max (dec) over ( partition by contract_number, x_cnt order by snapshot_id ) max_d, 
       count (qty_diff) over (partition by contract_number order by snapshot_id) as cnt_d, b.*
from (
select count( case decision when 'out' then 1 
                            when 'in'  then 2 
							else null
			end ) over ( partition by contract_number order by snapshot_id ) as x_cnt,
              case decision when 'out' then 1 
                            when 'in'  then 2 
							else null
			end as dec, 
       case when lag_qty != contract_term_months_qty then 'X' else null end as qty_diff, a.*
  from (
SELECT 	  
	--Compare tests to decide the decision
	CASE 
		WHEN (expiration_extended_test = 'extended' 
		  AND status_test = 'no change'
		  AND TRIM(c.tracs_status_name) = 'Active')
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
	, expiration_extended_test
	, status_test
	, expiration_passed_test
	--useful data for QA on decisions
	, tracs_overall_expiration_date
	, previous_expiration_date
	, time_diff
	, tracs_status_name
	, previous_status
--   , cast (null as integer) previous_churn_decisions
    , null churn_decisions_per_year
--    , null previous_contract_term_months_qty
    , lag(c.contract_term_months_qty,1) over (partition by c.contract_number order by c.snapshot_id) lag_qty
    , c.contract_term_months_qty
    , c.assisted_units_count
    , c.is_hud_administered_ind
    , c.is_acc_old_ind
    , c.is_acc_performance_based_ind
    , c.program_type_name
    , c.program_type_group_name
    , c.rent_to_FMR_ratio
    , null rent_gross_amount_per_unit
    , c."0br_fmr" br0_fmr
    , c."1br_fmr" br1_fmr
    , c."2br_fmr" br2_fmr
    , c."3br_fmr" br3_fmr
    , c."4br_fmr" br4_fmr
/*    , null 0BR_FMR_fmr
    , null 1BR_FMR_fmr
    , null 2BR_FMR_fmr
    , null 3BR_FMR_fmr
    , null 4BR_FMR_fmr
    */
    , c."0br_count" br0_count
    , c."1br_count" br1_count
    , c."2br_count" br2_count
    , c."3br_count" br3_count
    , c."4br_count" br4_count
    , c."5plusbr_count" br5_count
/*
    , null 0BR_PERC
    , null 1BR_PERC
    , null 2BR_PERC
    , null 3BR_PERC
    , null 4BR_PERC
    , null 5BR_PERC
*/
    , null average_bedroom_count
    , null neighborhood_median_rent
    , null neighborhood_lower_quartile_rent
    , null neighbohood_upper_quartile_rent
    , null percent_increase_neighborhood_median_rent
    , null percent_increase_neighborhood_upper_rent
    , null percent_increase_neighborhood_lower_rent
    , null ratio_neighborhood_median_to_gross_rent
    , null ratio_neighborhood_lower_to_gross_rent
    , null ratio_neighborhood_upper_to_gross_rent

FROM decisions_tests
INNER JOIN contracts c
ON decisions_tests.contract_number = c.contract_number
  AND decisions_tests.snapshot_id = c.snapshot_id

--Optionally, filter the decisions results
--WHERE expiration_test = 'in' 
--	OR status_test = 'out'

--Optionally, get just a subset of contract_numbers. This sorts by earliest expiration for each contract. 
WHERE decisions_tests.contract_number 
IN ( 	select * from
	contracts_random200

	--Options for filtering, from contract_number_queries section above:
	--contracts_earliest100
	--contracts_latest100
	--contracts_random100
	--contracts_500_1
	--contracts_500_2
	--'012063NISUP' 
	--'OH16Q921001'
	)
) a ) b ) c ) d
--where dec1 = 'X'
--where contract_number = 'AK06S031001'
order by contract_number, snapshot_id;

