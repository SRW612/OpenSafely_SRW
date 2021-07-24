from cohortextractor import StudyDefinition, patients, Measure

from codelists import *

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # include all patients registered with a GP at time of intervention
    population = patients.registered_as_of(
        "2020-11-10",
        return_expectations={"incidence": 0.98},
    ),

    # count of consultations for respiratory tract infections
    RTI_events=patients.with_these_clinical_events(
        RTI_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.4,
        },
    ),

    # count of consultations for acute respiratory tract infections
    aRTI_events=patients.with_these_clinical_events(
        aRTI_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.3,
        },
    ),

    # count of consultations for gastrointestinal infections
    gastro_events=patients.with_these_clinical_events(
        gastro_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.3,
        },
    ),

    # count of consultations for probable covid
    coviddiag_events=patients.with_gp_consultations(
        coviddiag_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.4,
        },
    ),

    # count of consultations for suspected covid (sensitive codelist)
    covidsympsens_events=patients.with_gp_consultations(
        covidsympsens_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.2,
        },
    ),

    # count of consultations for suspected covid (specific codelist)
    covidsympspec_events=patients.with_gp_consultations(
        covidsympspec_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.5,
        },
    ),

    # count of consultations where antibiotics were prescribed
    antibio_events=patients.with_gp_consultations(
        antibio_codes,
        between=["2020-07-14", "2021-03-15"],
        returning="number_of_matches_in_period",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.8,
        },
    ),

    #count of hospital admissions
    adm_events=patients.admitted_to_hospital(
        returning="number_of_matches_in_period",
        between=["2020-07-14", "2021-03-15"],
        date_format="YYYY-MM-DD",
        return_expectations={
        "int": {"distribution": "normal", "mean": 2, "stddev": 1},
        "incidence": 0.3,
        },
    ),
    #GP practice ID
    practice_ID=patients.registered_practice_as_of(
        "2020-11-10",
        returning="pseudo_id",
        return_expectations={
        "rate" : "universal",
        "int" : {"distribution" : "normal", "mean": 1500, "stddev": 15},
        },
    ),
)

# request counts disaggregated by week and GP practice
measures = [
    Measure(
        id="RTI_weekly",
        numerator="RTI_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="aRTI_weekly",
        numerator="aRTI_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="gastro_weekly",
        numerator="gastro_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="coviddiag_weekly",
        numerator="coviddiag_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="covidsympsens_weekly",
        numerator="covidsympsens_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="covidsympspec_weekly",
        numerator="covidsympspec_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="antibio_weekly",
        numerator="antibio_events",
        denominator="population",
        group_by="practice_ID",
    ),
    Measure(
        id="adm_weekly",
        numerator="adm_events",
        denominator="population",
        group_by="practice_ID",
    ),
]
