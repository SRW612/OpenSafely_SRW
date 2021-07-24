from cohortextractor.codelistlib import codelist_from_csv

RTI_codes = codelist_from_csv(
    "codelists/user-S_Walter-respiratory-tract-infections.csv", system="snomed", column="code"
)

aRTI_codes = codelist_from_csv(
    "codelists/user-S_Walter-acute-respiratory-tract-infections.csv", system="snomed", column="code"
)

gastro_codes = codelist_from_csv(
    "codelists/user-S_Walter-gastrointestinal-infections.csv", system="snomed", column="code"
)

coviddiag_codes = codelist_from_csv(
    "codelists/user-S_Walter-covid-19-diagnoses.csv", system="snomed", column="code"
)

covidsympsens_codes = codelist_from_csv(
    "codelists/user-S_Walter-covid-19-symptoms-sensitive.csv", system="snomed", column="code"
)

covidsympspec_codes = codelist_from_csv(
    "codelists/user-S_Walter-covid-19-symptoms-specific.csv", system="snomed", column="code"
)

antibio_codes = codelist_from_csv(
    "codelists/user-S_Walter-antibiotics.csv", system="pseudoBNF", column="code"
)