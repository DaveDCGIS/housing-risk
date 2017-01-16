/*

Very similar to select_decisions_data.sql - should be rebuilt from there instead of modifying this one



*/

-------------------------------------
SELECT
        --d.decision


        --remove this stuff from the query before training (just for debugging)
         EXTRACT(YEAR FROM manifest.date) AS decision_data_year
         ,case when (EXTRACT(YEAR FROM manifest.date)::INTEGER) = 2016 then 2015
          else (EXTRACT(YEAR FROM manifest.date)::INTEGER)
         end as altered_decision_data_year
        , rent.snapshot_id as rent_snapshot_id
        , c.snapshot_id as contract_snapshot_id
        , c.contract_number
        , p.property_name_text
        , p.owner_organization_name
        , p.address_line1_text as address
        , p.city_name_text as city
        , p.state_code as state

        , g.geoid
        , rent.geo_id2


        --Data we want
        , rent.hd01_vd01 AS median_rent
        , c.contract_term_months_qty
        --, d.term_mths_lag as previous_contract_term_months
        , 154 as previous_contract_term_months   --alternate since can't get decisions table data for previous contract_term now.
        , c.assisted_units_count
        , c.is_hud_administered_ind
        , TRIM(c.program_type_group_name) AS program_type_group_name
        , c.rent_to_FMR_ratio
        , c.is_acc_old_ind
        , c.is_acc_performance_based_ind
        , c.rent_to_FMR_ratio

        , c."0br_count" br0_count
        , c."1br_count" br1_count
        , c."2br_count" br2_count
        , c."3br_count" br3_count
        , c."4br_count" br4_count
        , c."5plusbr_count" br5_count

        , p.is_hud_owned_ind
        , p.owner_company_type
        , p.mgmt_agent_company_type
        --these are in the 'decisions' table because they are calculated, even though they do not change per contract.
        /*excluding for now because we need to keep these out of the test data so that we can get all DC buildings regardless of whether they have had a decision
        , d.br0_perc
        , d.br1_perc
        , d.br2_perc
        , d.br3_perc
        , d.br4_perc
        , d.br5_perc
        */

/*
--primary opening FROM statement, for use when making train/test data
FROM decisions AS d
LEFT JOIN
contracts AS c
ON c.contract_number = d.contract_number AND c.snapshot_id = d.snapshot_id
*/

--Alternative opening from statement when using to pull test data
FROM contracts AS c

LEFT JOIN properties AS p
ON c.property_id = p.property_id AND SUBSTRING(c.snapshot_id FROM 2) = SUBSTRING(p.snapshot_id FROM 2)

LEFT JOIN geocode AS g
ON c.property_id = g.property_id

LEFT JOIN manifest
ON manifest.snapshot_id = c.snapshot_id


LEFT JOIN acs_rent_median AS rent
ON g.geoid::TEXT = rent.geo_id2::TEXT
    AND
    --match the timing of the contract snapshot to the relevant year of rent data. Allow 2016 to use the most recently available data.
    (CASE WHEN (EXTRACT(YEAR FROM manifest.date)::INTEGER) = 2016 THEN 2015 --TODO change this to 2015 when new data is uploaded
          ELSE (EXTRACT(YEAR FROM manifest.date)::INTEGER)
     END)
    =
    (CASE WHEN rent.snapshot_id = 	'ACS_09_5YR_B25058_with_ann.csv' THEN 2009
   					WHEN rent.snapshot_id = 'ACS_10_5YR_B25058_with_ann.csv' THEN 2010
   					WHEN rent.snapshot_id = 'ACS_11_5YR_B25058_with_ann.csv' THEN 2011
   					WHEN rent.snapshot_id = 'ACS_12_5YR_B25058_with_ann.csv' THEN 2012
   					WHEN rent.snapshot_id = 'ACS_13_5YR_B25058_with_ann.csv' THEN 2013
   					WHEN rent.snapshot_id = 'ACS_14_5YR_B25058_with_ann.csv' THEN 2014
   					WHEN rent.snapshot_id = 'ACS_15_5YR_B25058_with_ann.csv' THEN 2015
   			  END
)::INTEGER

/*
WHERE d.decision IN ('in', 'out')
AND d.churn_flag IS NULL
AND rent.snapshot_id IS NOT NULL --skip years with no rent data
*/

--Alternate where statement to use when just getting current DC data
where p.state_code ILIKE 'DC'
AND c.snapshot_id = 'c2016-08'
AND rent.snapshot_id is not null
order by g.geoid
