from cohortextractor import StudyDefinition, Measure, patients

study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "2020-01-01", "latest": "today"},
        "rate": "exponential_increase",
        "incidence": 0.2,
    },

    index_date="2020-01-01",

    population=patients.registered_as_of("index_date"),

    stp=patients.registered_practice_as_of(
        "index_date",
        returning="stp_code",
        return_expectations={
            "category": {"ratios": {"stp1": 0.1, "stp2": 0.2, "stp3": 0.7}},
            "incidence": 1,
        },
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),

    admitted=patients.admitted_to_hospital(
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 0.1},
    ),

    died=patients.died_from_any_cause(
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        return_expectations={"incidence": 0.05},
    ),
)

measures = [
    Measure(
        id="hosp_admission_by_stp",
        numerator="admitted",
        denominator="population",
        group_by="stp",
    ),
    Measure(
        id="death_by_stp",
        numerator="died",
        denominator="population",
        group_by="stp",
        small_number_suppression=True,
    ),
]
