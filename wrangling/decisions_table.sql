SELECT *
FROM(

	SELECT *
		, CASE WHEN EXTRACT(epoch FROM time_diff)/3600 > 0 THEN 'in'
		  else null
		  END AS decision
		, CASE WHEN tracs_status_name = 'Expired' 
			AND previous_status = 'Active'
			THEN 'out' 
		  END AS out_decision
	FROM (
		SELECT 
		contract_number
		, (tracs_overall_expiration_date - lag(tracs_overall_expiration_date, 1) OVER (partition by contract_number order by snapshot_id)) as time_diff
		, snapshot_id
		, contract_term_months_qty
		, tracs_effective_date
		, tracs_overall_expiration_date
		, tracs_overall_exp_fiscal_year
		, tracs_overall_expire_quarter
		, TRIM(tracs_status_name) as tracs_status_name
		, TRIM(LAG(tracs_status_name,1) 
			    OVER (partition by contract_number order by snapshot_id)) as previous_status

		FROM (
			SELECT contract_number
			, property_id, property_name_text
				, snapshot_id
				, tracs_effective_date
				, tracs_overall_expiration_date
				, tracs_overall_exp_fiscal_year
				, tracs_overall_expire_quarter
				, tracs_current_expiration_date
				, tracs_status_name
				, contract_term_months_qty
			  FROM public.contracts
			  WHERE contract_number = '012063NISUP' --'OH16Q921001' 
		  ) as subtable
	) AS decision_table
) AS final_table
WHERE decision = 'in' 
	OR out_decision = 'out'
LIMIT 100;