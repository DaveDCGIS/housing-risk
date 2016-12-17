
	/*
	--------------------------
	contract_number_queries
	These are virtual tables we can plug into the 'where in(virtual_table)' statement to filter down to only some contracts.
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

        WHEN status_test = 'restored'
          THEN 'restored'

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

order by decisions_tests.contract_number, snapshot_id
