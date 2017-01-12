
SELECT
    CASE
        WHEN decision='restored' THEN 'churn'
        WHEN next_decision = 'restored' THEN 'churn'
        ELSE 'use'
    END AS churn_flag
    , *
 FROM (
    SELECT
          decisions_old.decision AS decision_copy
          ,LEAD(decisions_old.decision) OVER (PARTITION BY contract_number ORDER BY snapshot_id) AS next_decision
          , count(decision) OVER (PARTITION BY contract_number ORDER BY snapshot_id ROWS UNBOUNDED PRECEDING) AS num_previous_snapshots
          , *
    FROM decisions_old
) AS decisions_portion

WHERE contract_number IN (
--Random list of contracts
SELECT contract_number
FROM	(
  SELECT contract_number, MIN(tracs_overall_expiration_date) AS earliest_expiration
    FROM contracts
    GROUP BY contract_number
    LIMIT 2000
  ) AS random_unsorted
ORDER BY earliest_expiration
)
ORDER BY contract_number, snapshot_id
