

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
SELECT 	  decisions_tests.snapshot_id
	, decisions_tests.contract_number

	--Compare tests to decide the decision
	, CASE 
		WHEN (expiration_extended_test = 'extended' 
		  AND status_test = 'no change'
		  AND TRIM(contracts.tracs_status_name) = 'Active')
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

	--status tests
	, expiration_extended_test
	, status_test
	, expiration_passed_test

	--useful data for QA on decisions
	, tracs_overall_expiration_date
	, previous_expiration_date
	, time_diff
	, contract_term_months_qty
	, tracs_status_name
	, previous_status

FROM decisions_tests
INNER JOIN contracts
ON decisions_tests.contract_number = contracts.contract_number
  AND decisions_tests.snapshot_id = contracts.snapshot_id

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
order by decisions_tests.contract_number, snapshot_id
;
