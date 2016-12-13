--example query to get rent data
SELECT * 
FROM acs_rent_median AS mrent
INNER JOIN manifest AS m
	ON m.snapshot_id = mrent.snapshot_id
where geo_id2 = '11001004400'


--TODO - we can join to the decisions table using the combo of geo_id2 AND where the absolute value of the date difference between the contract date and manifest.date is the smallest (e.g. closest date)
