This script is used to extract an event log from the original data.
We use the Organ Retrieval and Collection of Health Information for Donation (ORCHID) [dataset](https://doi.org/10.13026/eytj-4f29) for this purpose.
As the dataset is not publicly available, we cannot provide the data here.
You can request access to the data and place the `opd.csv` file in the `data/raw` folder.

### Events
The dataset contains the following events:

1. Referral: The patient is referred to the OPO. This event is always present for each patient and a timestamp is available.
2. Evaluation: The patient is evaluated by the OPO. This event is always present for each patient. However, no timestamp is available.
3. Approach: The OPO approaches the patient. In the dataset, a flag is available that indicates if the patient was approached. If the patient was approached, a timestamp is available.
4. Authorization: The patient is authorized for organ donation. In the dataset, a flag is available that indicates if the patient was authorized. If the patient was authorized, a timestamp is available.
5. Procurement: The organs are procured. In the dataset, a flag is available that indicates if the organs were procured. If the organs were procured, a timestamp is available.
6. Transplant: The organs are transplanted. In the dataset, a flag is available that indicates if the organs were transplanted. However, no timestamp is available.

The events should happen in the above order. However, the dataset contains some inconsistencies. For example, there are cases where the patient was authorized before the patient was approached.

For the events where no timestamp is available, we assume that the event happens one minute after the previous event.

### Patients
The dataset contains the following information for each patient:

| Original Name            | New Name                 | Attribute Type                                                              | Description                                                              |
|--------------------------|--------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `PatientID`              | `case:concept:name`      | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | A unique identifier for each patient. We use this as the case id.        |
| `OPO`                    | `opo_id`                 | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The OPO that is responsible for the patient.                             |
| `HospitalID`             | `hospital_id`            | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The hospital where the patient was treated.                              |
| `Age`                    | `age`                    | [Numerical][backend.src.dataclasses.attributes.AttributeType.NUMERICAL]     | The age of the patient.                                                  |
| `Gender`                 | `gender`                 | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The gender of the patient.                                               |
| `Race`                   | `race`                   | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The race of the patient.                                                 |
| `brain_death`            | `brain_death`            | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Indicates whether the patient experienced brain death.                   |
| `Referral_Year`          | `referral_year`          | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The year of patient referral.                                            |
| `Referral_DayofWeek`     | `referral_day_of_week`   | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The day of the week of patient referral.                                 |
| `Cause_of_Death_UNOS`    | `cause_of_death`         | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The cause of death according to UNOS (United Network for Organ Sharing). |
| `Mechanism_of_Death`     | `mechanism_of_death`     | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The mechanism of death for the patient.                                  |
| `Circumstances_of_Death` | `circumstances_of_death` | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | The circumstances surrounding the patient's death.                       |
| `outcome_heart`          | `outcome_heart`          | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the heart organ.                                             |
| `outcome_liver`          | `outcome_liver`          | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the liver organ.                                             |
| `outcome_kidney_left`    | `outcome_kidney_left`    | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the left kidney organ.                                       |
| `outcome_kidney_right`   | `outcome_kidney_right`   | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the right kidney organ.                                      |
| `outcome_lung_left`      | `outcome_lung_left`      | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the left lung organ.                                         |
| `outcome_lung_right`     | `outcome_lung_right`     | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the right lung organ.                                        |
| `outcome_pancreas`       | `outcome_pancreas`       | [Categorical][backend.src.dataclasses.attributes.AttributeType.CATEGORICAL] | Outcome for the pancreas organ.                                          |

::: backend.src.data.extract
