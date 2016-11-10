# Data Summary

This documents all the data sources included in the 'data' folder for this project.
* Be sure to update this document whenever a new data source is added or modified
* When possible, keep the filename the same as it was named on the website it was downloaded from - this makes it easier to find the original source if needed. Use subfolders, and this document, to keep track of what things are called
* Delete the zip files after unzipping (i.e. one copy of the data in total)


-----------------

# Data Folders
*******************
## `202_loans`
* `202directloans09242015.xls`
   From here: http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/mfh/202directloan  
   A bit out of date - 2015.  

*******************
## `census`
* 2010 Census
  * Summary File 1: Goes down to census tract level (and below), best bet for general demographic data: http://www2.census.gov/census_2010/04-Summary_File_1/, docs: http://www.census.gov/prod/cen2010/doc/sf1.pdf
  * Summary File 2: contains more detailed subcategories of data. http://www2.census.gov/census_2010/05-Summary_File_2/United_States/

*******************
## `cdbg` - *Community Development Block Grants*. Unlikely we will get national level data on this, because each locality can use funds how they want and set their own terms.


*******************
##  `fair_market_rents`
set by HUD each year for each city.

* `FMR_All_1983_2017.xslx`
   Has fair market rents for each bedroom type for each year for each city. Note, specific buildings may have a different negotiated rent level rather than the FMR for their city.
   From: "FMR History 1983 - Present: All Bedroom Unit data in MS EXCEL (*.xls, 8.32 MB)."  
   https://www.huduser.gov/portal/datasets/fmr.html
* `fmrover_071707R2.doc` - Fair Market Rents: Overview from the same page

*******************
## `hud_mortages`
### `insured`
* `rm-a-07_31_2016.xlsx`
   Covers multiple HUD insured mortage programs - section 223, 241, 207. Not all are housing.  
   All loans that still have a balance. Downloaded from http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/comp/rpts/mfh/mf_f47

### `terminated`
* `rm_t_07_31_2016.xls`  
   Loans paid off or otherwise ended since 1939 to today. Downladed from http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/comp/rpts/mfh/mf_f47t



*******************
## `lihtc`
Low Income Housing Tax Credit.

* `LIHTCPUB.ACCDB` and `LIHTC Data Dictionary 2014.pdf` and `LIHTCPUB.DBF`
   Database revised as of 5/15/16. Includes projects placed in service through 2014. Data accessed here: http://lihtc.huduser.gov/ Duplicate available here: https://www.huduser.gov/portal/datasets/lihtc.html#about

### `states`
The national database is not updated regularly. States usually manage the process of awarding who gets the credits (based on a quota and an application process annually). Some states may publish their lists more frequently, if we want to try to compile more recent data.

#### `VA`
* `Existing TC Property List 010816.xlsx`
   No data on status, just a list of properties. Should corroborate national list. from http://www.vhda.com/BusinessPartners/MFDevelopers/LIHTCProgram/Pages/LIHTCProgram.aspx#.V8gdiJgrKUk  
   Other Sources of Virginia Data:  
   Sourcebook - lots of calculated info. Contact them for access to their data?  http://www.housingvirginia.org/sourcebook/  



********************
## `nationalHousingPreservationDatabase`
We probably won't want to use this 3rd party database, which compiles HUD data sources but may be a bit old. See individual readme for more about versions of this data that have been downloaded. From http://www.preservationdatabase.org/


*********************
## `pha`
Public Housing Authority. So far have not identified a national database of public housing buildings. Some misc. links to look for info:
http://portal.hud.gov/hudportal/HUD?src=/program_offices/public_indian_housing/pha
http://portal.hud.gov/hudportal/HUD?src=/program_offices/public_indian_housing/systems/pic/haprofiles
http://data.hud.gov/data_sets.html
http://affordablehousingonline.com/affordable-housing-data



*********************
## `physical_inspection_scores`
HUD inspects each building every few years. huduser.gov looks like it's likely the more complete dataset.

### `huduser.gov`
Everything in this folder is downloaded from https://www.huduser.gov/portal/datasets/pis.html
	* Current as of 8/17/2016
	* 4 partially(?) overlapping datasets covering inspections starting in late 90's through today.
	* each record is an inspection
	* The text files in 2011 folder appear to have all the pre-2011 data in them as well

### `alternate_hud.gov`
	* Looks like it is a duplicate of above data, but exported in a different format
	* last updated May 2016
	* each record is a property; different columns for each of the last 3 inspections with score and date.
	* from: http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/mfh/rems/remsinspecscores/remsphysinspscores





**********************
## `PresCat_Export_20160401`
The DC-only Preservation Catalog, which compiles various HUD data sources. We can use this to validate our aggregation of information against the DC records to make sure we agree.


**********************
## `section8`

### `contracts_database`
Expected to be our primary data set. We will need historical copies of this data set from each year. Currently these are coming from a few different places.
* `main-website` - data from the HUD website, current as of 8/2/2016 (updated monthly). from here: http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/mfh/exp/mfhdiscl
* `internetArchive` - Old versions of that same page, from the Wayback Machine Internet Archive.
	* This is the web page before they overhauled their site in 2011: http://www.hud.gov/offices/hsg/mfh/exp/mfhdiscl.cfm
* `urban_institute` - Urban Institute has saved copies every time they download the contracts database. This is our **primary** data source
  * zip file of the original dump from Urban includes zipped or self extracting Access databases, Urban's dump to CSV files (named.txt), and data dictionaries as of the time of the original download.
  * Zip of just the source Access databases, renamed to match their download date.
  * Each folder - text files that should be 'ready to use' csv of the two tables from the access databases. When there was a file already dumped from Access by Urban Institute, Neal copied-pasted in the header row manually. If there was not already a .txt dump, we created one from the corresponding Access database. Small chance of data issues - can go back to the source access database if need be.



### `alternate_portfolio_datasets`
	* Looks like this is an Excel dump of filtered data from the above database??
	* BUT - some data is not available in database. Importantly, the Excel files have a renewal_status field.
	* Current as of 8/2/2016
	* From here: http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/mfh/presrv/mfhpreservation

### `opt-out`
Trying to get a clean, national level list of properties that have opted-out of the Section8 program from HUD.

In the meantime, there is a 'states' folder that contains a few example lists from states that publish their own opt out list. Adding more state-level lists to this is a last resort.


**********************
## `zip_census_crosswalks`
Downloaded from HUD, shows weighting factors to map between zip code and census tract. Only if we need to use it (might use GIS methods instead). Keep in mind weighting factors aren't the same in both directions (i.e. need different factor for zip to census vs. census to zip). https://www.huduser.gov/portal/datasets/usps_crosswalk.html









*******************************

# Places to look for more data
* http://data.hud.gov/data_sets.html


How to Contact HUD:
	* Multifamily Department phone numbers:
	http://portal.hud.gov/hudportal/HUD?src=/program_offices/housing/dirhousi#omam

	* OFfice of Policy Development and Research:
		- "hotline 1-800-245-2691 for help accessing the information you need"
		- Data License Agreement. You can submit an application to get data that has personally identifiable information for research purposes. For our research we won't need PII data (or want it - the requirements are onerous), but maybe we can go through the contact there to request the opt-out list or other data. Lists Dr. Jon Sperling as contact w/ his office phone number. https://www.huduser.gov/portal/research/pdr_data-license.html

Who's collecting Preservation Related Data - state-by-state list of lots of people and what kind of data they have.
http://preservation.shimberg.ufl.edu/


Some examples:
	* California - need to request access. http://chpc.net/advocacy-research/preservation/preservation-database/
	*

----------------------
Authors of Opting Out:
2015 version

'Economic Systems Inc.', Falls Church VA

Shimberg Center for Housing Studies, University of Florida
Anne Ray
Jeongseob Kim
Diep Nguyen
Jongwan Choi

2006 Version
Sponsored by HUD "Office of Policy Development and Research"
'Econometrica, Inc.', Bethesda MD
'Abt Associates, Inc.', Cambridge, Massachusetts

Meryl Finkel
Charles Hanson
Richard Hilton
Ken Lam
Melissa Vandawalker

Thanks to *Steve Martin* and FHA Office of Program Systems Management for providing the list that identified opt-out properties
Dr. Jennifer Stoloff of the Office of Policy Development and Research
