

* Project:	Germ Defence Study P512
* Program:	GermDefence.do
* Purpose:	Analyse data acording to the study protocol within the OpenSafely system
* Author:	Scott Walter, July 2021

* Note: + indicates sections that need updating before running this program on real data.

*+ how to set the directory for running on real data?
global gd "C:\Users\dy21108\OneDrive - University of Bristol\Documents\GitHub\OpenSafely_SRW"

*send all output to log file
log using "$gd\output\analysis_log.log", replace

*+convert CSV files to .dta files - still need Covid and antibiotic events
import delimited using "$gd\output\measures\measure_RTI_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_RTI_weekly.dta", replace

import delimited using "$gd\output\measures\measure_aRTI_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_aRTI_weekly.dta", replace

import delimited using "$gd\output\measures\measure_gastro_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_gastro_weekly.dta", replace

import delimited using "$gd\output\measures\measure_coviddiag_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_coviddiag_weekly.dta", replace

import delimited using "$gd\output\measures\measure_covidsympsens_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_covidsympsens_weekly.dta", replace

import delimited using "$gd\output\measures\measure_covidsympspec_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_covidsympspec_weekly.dta", replace

import delimited using "$gd\output\measures\measure_antibio_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_antibio_weekly.dta", replace

import delimited using "$gd\output\measures\measure_adm_weekly.csv", clear
drop population value
save "$gd\output\measures\measure_adm_weekly.dta", replace



*get weekly level counts for any type of GP consultation - treat as base dataset
import delimited using "$gd\output\measures\measure_consults_weekly.csv", clear
drop value

*+merge on tables for other outcomes to create single unified dataset
merge 1:1 practice_id date using "$gd\output\measures\measure_RTI_weekly.dta"
drop _merge
merge 1:1 practice_id date using "$gd\output\measures\measure_aRTI_weekly.dta"
drop _merge
merge 1:1 practice_id date using "$gd\output\measures\measure_gastro_weekly.dta"
drop _merge
merge 1:1 practice_id date using "$gd\output\measures\measure_adm_weekly.dta"
drop _merge


*fill in missing counts
replace all_events=0 if all_events==.|all_events<0
replace rti_events=0 if rti_events==.|rti_events<0
replace arti_events=0 if arti_events==.|arti_events<0
replace gastro_events=0 if gastro_events==.|gastro_events<0
replace adm_events=0 if adm_events==.|adm_events<0

*define pre and post intervention periods
generate date2 = date(date, "YMD")
format %td date2
gen period = (date2>=d(10nov2020))

*consecutively number weeks
sort date2 practice_id

gen year = year(date2)
gen week = week(date2)

gen week_date = week - 27
replace week_date = week + 25 if year==2021

 
*save practice x week level data
save "$gd\output\practice_weekly.dta", replace


*** I. Per protocol analysis

*+collapse post-intervention data to one row per practice - sum event counts for each outcome 
drop if period==1
collapse (sum) all_events rti_events arti_events gastro_events adm_events population, by(practice_id)

*+merge on practice covariates
gen intervention = uniform() < .5
*gen population = rpoisson(200)
replace population=1 if population<1

*+Compare event rates between intervention vs. control during post-intervention period: 10/11/20 - 15/03/21
glm all_events i.intervention, family(nb) link(log) exposure(population)
glm rti_events i.intervention, family(nb) link(log) exposure(population)
glm arti_events i.intervention, family(nb) link(log) exposure(population)
glm gastro_events i.intervention, family(nb) link(log) exposure(population)
glm adm_events i.intervention, family(nb) link(log) exposure(population)


*** II. Time series analysis

** A. Weekly level analysis

*get practice x week level data, then collapse to one row per week, summing event counts for each outcome
use "$gd\output\practice_weekly.dta", replace
gen intervention = uniform() < .5
collapse (sum) all_events rti_events arti_events gastro_events adm_events population, by(date2 week_date intervention)
gen time=week_date - 17.5
gen period = (date2>=d(10nov2020))

*create interaction variables
gen time_period = 0
replace time_period = time if period==1

gen time_intervention = 0
replace time_intervention = time if intervention==1

gen intervention_period = 0
replace intervention_period = 1 if intervention==1 & period==1

gen time_int_period = 0
replace time_int_period = time if intervention_period==1

*Difference in differences model
glm rti_events intervention period intervention_period, family(nb) link(log) exposure(population)

*Controlled interrupted time series model
glm rti_events time intervention period time_intervention time_period intervention_period time_int_period, family(nb) link(log) exposure(population)


** B. Practice level analysis
use "$gd\output\practice_weekly.dta", replace
gen intervention = practice_id < 1500

gen time=week_date - 17.5

*create interaction variables
gen time_period = 0
replace time_period = time if period==1

gen time_intervention = 0
replace time_intervention = time if intervention==1

gen intervention_period = 0
replace intervention_period = 1 if intervention==1 & period==1

gen time_int_period = 0
replace time_int_period = time if intervention_period==1

*Controlled interrupted time series model
glm rti_events time intervention period time_intervention time_period intervention_period time_int_period, family(nb) link(log) exposure(population)

*Random intercepts CITS
menbreg rti_events time intervention period time_intervention time_period intervention_period time_int_period, exposure(population) || practice_id: 




gen time_period = 0
replace time_period = time if period==1

gen time_group = 0
replace time_group = time if group==1

gen group_period = 0
replace group_period = 1 if group==1 & period==1

gen time_group_period = 0
replace time_group_period = time if group_period==1

glm swabcount time group period time_group time_period group_period time_group_period, family(nb) link(log) exposure(attendances2)



log close