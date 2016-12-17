
WITH
contracts_random200 AS (
SELECT contract_number
FROM	(
  SELECT contract_number, MIN(tracs_overall_expiration_date) AS earliest_expiration
    FROM contracts
    GROUP BY contract_number
    LIMIT 200
  ) AS random_unsorted
ORDER BY earliest_expiration
)

/*
, contracts_earliest100 AS (
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
*/
SELECT *

FROM decisions
WHERE
contract_number
IN ( 	SELECT  * FROM
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
 ORDER BY contract_number, snapshot_id
