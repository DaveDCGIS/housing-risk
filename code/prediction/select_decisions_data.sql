
/*
select
	expiration_extended_test
	, status_test
	, expiration_passed_test
	--useful data for QA on decisions
	, tracs_overall_expiration_date
	, previous_expiration_date
	, time_diff
	, tracs_status_name
	, previous_status
    , null churn_decisions_per_year
    , c.assisted_units_count
    , c.is_hud_administered_ind
    , c.is_acc_old_ind
    , c.is_acc_performance_based_ind
    , c.program_type_name
    , c.program_type_group_name
    , c.rent_to_FMR_ratio
    , c."0br_count" br0_count
    , c."1br_count" br1_count
    , c."2br_count" br2_count
    , c."3br_count" br3_count
    , c."4br_count" br4_count
    , c."5plusbr_count" br5_count
FROM decisions_tests
INNER JOIN contracts c
ON decisions_tests.contract_number = c.contract_number
AND decisions_tests.snapshot_id = c.snapshot_id
*/

-------------------------------------
SELECT
        d.decision
        --Extra identifying information for troubeshooting, not training
        , EXTRACT(YEAR FROM manifest.date) AS decision_data_year
        , rent.snapshot_id
        , c.snapshot_id
        , c.contract_number
        
        --Data we want
        , rent.hd01_vd01 AS median_rent
        , c.contract_term_months_qty
        , c.assisted_units_count
        , c.is_hud_administered_ind
        , TRIM(c.program_type_group_name) AS program_type_group_name
        , c.rent_to_FMR_ratio
        , c."0br_count" br0_count
        , c."1br_count" br1_count
        , c."2br_count" br2_count
        , c."3br_count" br3_count
        , c."4br_count" br4_count
        , c."5plusbr_count" br5_count

FROM decisions AS d
LEFT JOIN contracts AS c
ON c.contract_number = d.contract_number AND c.snapshot_id = d.snapshot_id

LEFT JOIN geocode AS g
ON c.property_id = g.property_id

LEFT JOIN manifest 
ON manifest.snapshot_id = c.snapshot_id


LEFT JOIN acs_rent_median AS rent
ON g.geoid::TEXT = rent.geo_id2::TEXT AND (EXTRACT(YEAR FROM manifest.date)::INTEGER) = 
    (CASE WHEN rent.snapshot_id = 	'ACS_09_5YR_B25058_with_ann.csv' THEN 2009
   					WHEN rent.snapshot_id = 'ACS_10_5YR_B25058_with_ann.csv' THEN 2010
   					WHEN rent.snapshot_id = 'ACS_11_5YR_B25058_with_ann.csv' THEN 2011
   					WHEN rent.snapshot_id = 'ACS_12_5YR_B25058_with_ann.csv' THEN 2012
   					WHEN rent.snapshot_id = 'ACS_13_5YR_B25058_with_ann.csv' THEN 2013
   					WHEN rent.snapshot_id = 'ACS_14_5YR_B25058_with_ann.csv' THEN 2014
   			  END
)::INTEGER

WHERE d.decision IN ('in', 'out')
AND d.churn_flag IS NULL

