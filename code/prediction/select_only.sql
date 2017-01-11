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
  --, c."0br_fmr" br0_fmr
  --, c."1br_fmr" br1_fmr
  --, c."2br_fmr" br2_fmr
  --, c."3br_fmr" br3_fmr
  --, c."4br_fmr" br4_fmr
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
