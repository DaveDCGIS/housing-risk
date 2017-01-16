SELECT avg(contract_term_months_qty) 
FROM contracts AS c
LEFT JOIN properties AS p
ON c.property_id = p.property_id AND SUBSTRING(c.snapshot_id FROM 2) = SUBSTRING(p.snapshot_id FROM 2)

WHERE c.snapshot_id = 'c2016-08'
AND p.state_code ILIKE 'DC'