/*
First get rid of the current version of the decisions_test table
*/
DROP TABLE public.decisions_tests;


/*
-------------------------
The 'decisions_tests' table compares each snapshot to the previous one,
and returns the results of the various tests. It is then necessary to 
decide which tests we want to use to create the actual 'decisions' table.
-------------------------
*/
WITH decisions_tests AS (
	--This is our full report of decision tests
	SELECT 
		contract_number
		, snapshot_id
		
		--Has the expiration been extended?
		, CASE WHEN EXTRACT(epoch FROM time_diff)/3600 > 0 
		       THEN 'extended'
		     WHEN EXTRACT(epoch FROM time_diff)/3600 = 0 
		       THEN 'no change'
		     WHEN time_diff IS NULL
		       THEN 'first'
		     ELSE 'reduced'
		  END AS expiration_extended_test

		--Did it change from Active to one of the cancelled statuses?
		, CASE 	WHEN tracs_status_name IN ('Terminated', 'Expired', 'Cancelled', 'Suspended')
			  AND previous_status = 'Active'
			  THEN 'out'
			WHEN tracs_status_name = 'Active'
			  AND previous_status IN ('Terminated', 'Expired', 'Cancelled', 'Suspended')
			  THEN 'restored'
			WHEN tracs_status_name = previous_status
			  THEN 'no change'
			WHEN previous_status IS NULL
			  THEN 'first'
			ELSE 'not handled'
		  END AS status_test

		--Has the contract expired as of the day the snapshot was downloaded?
		, CASE 	WHEN expiration_passed_check = 'expired'
			  AND previous_expiration_passed_check = 'Ok'
			  THEN 'expired'
			WHEN expiration_passed_check = 'expired'
			  AND previous_expiration_passed_check IS NULL
			  THEN 'expired'
			WHEN expiration_passed_check = 'ok'
			  AND previous_expiration_passed_check IS NULL
			  THEN 'ok'
			WHEN expiration_passed_check = previous_expiration_passed_check
			  THEN 'no change'
			ELSE 'flag'
		  END AS expiration_passed_test

		, previous_status
		, previous_expiration_date
		, previous_snapshot_id
		, time_diff
		 
	FROM (
		SELECT 
		
		  
		  TRIM(LAG(expiration_passed_check,1) 
			    OVER (partition by contract_number order by snapshot_id)) as previous_expiration_passed_check
		, expiration_passed_check
		, TRIM(tracs_status_name) as tracs_status_name
		, TRIM(LAG(tracs_status_name,1) 
			    OVER (partition by contract_number order by snapshot_id)) as previous_status
		, (tracs_overall_expiration_date - previous_expiration_date) as time_diff
		, contract_number
		, snapshot_id
		, previous_snapshot_id
		, snapshot_date
		, contract_term_months_qty
		, tracs_effective_date
		, tracs_overall_expiration_date
		, previous_expiration_date
		, tracs_overall_exp_fiscal_year
		, tracs_overall_expire_quarter
		
		FROM (
			SELECT contract_number
			, property_id, property_name_text
				, contracts.snapshot_id AS snapshot_id
				, lag(contracts.snapshot_id, 1) OVER (partition by contract_number order by public.contracts.snapshot_id) as previous_snapshot_id
				, tracs_effective_date
				, tracs_overall_expiration_date
				, lag(tracs_overall_expiration_date, 1) OVER (partition by contract_number order by public.contracts.snapshot_id) as previous_expiration_date
				, tracs_overall_exp_fiscal_year
				, tracs_overall_expire_quarter
				, tracs_current_expiration_date
				, tracs_status_name
				, contract_term_months_qty
				, manifest.date AS snapshot_date

				, CASE 	WHEN manifest.date > tracs_overall_expiration_date 
					THEN 'expired'
					ELSE 'ok'
				  END AS expiration_passed_check
				  
			  FROM public.contracts
			  LEFT JOIN public.manifest
			  ON public.contracts.snapshot_id = public.manifest.snapshot_id
		  ) as subtable
	) AS decision_table
) 


--Make a new table with the data
SELECT *
INTO decisions_tests
FROM decisions_tests;