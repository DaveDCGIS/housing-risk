
--These are just the fields we want to load as our decision table
SELECT 	
	
	  snapshot_id
	, contract_number
	--This is a temporary approach to choosing among our various tests
	, CASE WHEN expiration_extended_test = 'in' THEN 'in'
		WHEN status_test = 'out' THEN 'out'
		WHEN expiration_extended_test = 'no change' then 'no change'
		ELSE 'other'
	  END AS decision
	, tracs_overall_expiration_date
	, time_diff
	, contract_term_months_qty
	, tracs_status_name
	, previous_status
	  
FROM(
	--This is our full report of decision tests
	SELECT 
		--Has the expiration been extended?
		  CASE WHEN EXTRACT(epoch FROM time_diff)/3600 > 0 
		       THEN 'in'
		     WHEN EXTRACT(epoch FROM time_diff)/3600 = 0 
		       THEN 'no change'
		     WHEN time_diff IS NULL
		       THEN 'first'
		     ELSE 'flag'
		  END AS expiration_extended_test

		--Did it change from Active to one of the cancelled statuses?
		, CASE 	WHEN tracs_status_name IN ('Terminated', 'Expired', 'Cancelled', 'Suspended')
			  AND previous_status = 'Active'
			  THEN 'out'
			WHEN tracs_status_name = previous_status
			  THEN 'no change'
			WHEN previous_status IS NULL
			  THEN 'first'
			ELSE 'not handled'
		  END AS status_test

		--Has the contract expired as of the day the snapshot was downloaded?
		, CASE 	WHEN expiration_passed_check = 'Expired'
			  AND previous_expiration_passed_check = 'Ok'
			  THEN 'out'
			WHEN expiration_passed_check = previous_expiration_passed_check
			  THEN 'no change'
			WHEN previous_expiration_passed_check IS NULL
			  THEN 'first'
			ELSE 'flag'
		  END AS expiration_passed_test
		, *
	FROM (
		SELECT 
		
		  
		  TRIM(LAG(expiration_passed_check,1) 
			    OVER (partition by contract_number order by snapshot_id)) as previous_expiration_passed_check
		, expiration_passed_check
		, TRIM(tracs_status_name) as tracs_status_name
		, TRIM(LAG(tracs_status_name,1) 
			    OVER (partition by contract_number order by snapshot_id)) as previous_status
		, (tracs_overall_expiration_date - lag(tracs_overall_expiration_date, 1) OVER (partition by contract_number order by snapshot_id)) as time_diff
		, contract_number
		, snapshot_id
		, snapshot_date
		, contract_term_months_qty
		, tracs_effective_date
		, tracs_overall_expiration_date
		, tracs_overall_exp_fiscal_year
		, tracs_overall_expire_quarter
		
		FROM (
			SELECT contract_number
			, property_id, property_name_text
				, contracts.snapshot_id AS snapshot_id
				, tracs_effective_date
				, tracs_overall_expiration_date
				, tracs_overall_exp_fiscal_year
				, tracs_overall_expire_quarter
				, tracs_current_expiration_date
				, tracs_status_name
				, contract_term_months_qty
				, manifest.date AS snapshot_date

				, CASE 	WHEN manifest.date > tracs_overall_expiration_date 
					THEN 'Expired'
					ELSE 'Ok'
				  END AS expiration_passed_check
				  
			  FROM public.contracts
			  LEFT JOIN public.manifest
			  ON public.contracts.snapshot_id = public.manifest.snapshot_id
			  --WHERE contract_number = '012063NISUP' --'OH16Q921001' --
		  ) as subtable
	) AS decision_table
) AS final_table
--Optionally, filter the results
--WHERE expiration_test = 'in' 
--	OR status_test = 'out'

--Optionally, get just a subset of contract_numbers
WHERE contract_number 
IN (
	SELECT DISTINCT contract_number
	FROM contracts
	LIMIT 200
	)
--LIMIT 1000


;