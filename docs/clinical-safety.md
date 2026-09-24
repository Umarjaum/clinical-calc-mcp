# Clinical safety and intended use

`clinical-calc-mcp` performs a small set of deterministic mathematical calculations and exposes them through the Model Context Protocol. It is a calculation utility, not a diagnostic or treatment-decision system. It does not determine whether a calculated value is appropriate for an individual patient, nor does it establish or replace any standard of care.

The software is intended for education and authorized clinical-software workflows subject to local governance. It is not a substitute for qualified clinician judgment, patient assessment, current applicable guidance, equipment instructions, or institutional protocols. Users are responsible for checking input values and units, understanding the formula's assumptions, reviewing the output, and independently verifying any result before considering it in a clinical context.

## Calculator-specific limitations

### Parkland formula

The tool implements the classic estimate `4 mL × body weight (kg) × %TBSA` and divides that result in half between the first 8-hour period and the following 16-hour period. The first 8 hours are conventionally measured from the time of burn, not the time of hospital arrival. Fluid administered after the burn must be accounted for clinically. Current burn-management protocols may differ. The result is not a determination of actual fluid requirement and does not provide instructions to administer fluid.

### Mosteller BSA and BMI

The tool calculates BSA as `sqrt((height_cm × weight_kg) / 3600)` and BMI as `weight_kg / height_m²`. It reports no category, interpretation, diagnosis, or recommendation. These formulae do not provide a complete clinical assessment.

### Infusion rate

The tool calculates arithmetic rates from the supplied volume, time, and drop factor. The user must supply the actual set calibration. The whole-drop result uses nearest integer rounding with exact half values rounded upward. A rounded gravity rate may not be clinically appropriate and is not an instruction to set equipment or administer a fluid.

### Vital-sign arithmetic

The tool returns pulse pressure (`systolic − diastolic`), an estimated mean arterial pressure (MAP), and the un-interpreted shock index (`heart rate / systolic pressure`). MAP is estimated as `diastolic + (systolic − diastolic)/3`, an approximation associated with the shape of the arterial pressure waveform at ordinary resting heart rates. It is not a direct pressure measurement; at faster heart rates the approximation may be less suitable [1]. Shock index is only a calculated ratio. Its association with outcomes varies across populations and settings, and medications and other factors can confound it [2]. This tool intentionally provides no threshold, normal range, risk score, interpretation, triage, diagnosis, or action recommendation.

### Unit conversions

The temperature converter applies Celsius/Fahrenheit arithmetic and rejects values below absolute zero. The weight converter converts between kilograms and pounds using a fixed conversion factor. Neither converter checks the source measurement, evaluates whether the value is plausible for a particular person, or uses converted weight to calculate a dose.

## Input and numerical validation

Numeric inputs must be finite. Tool-specific constraints apply: most measurements must be greater than zero; systolic blood pressure must exceed diastolic pressure; TBSA must not exceed 100%; the drop factor must be a positive whole number of drops per milliliter; and temperatures below absolute zero are rejected. Booleans supplied as numbers, NaN, infinity, invalid units, and values whose results exceed supported finite numeric precision are rejected. The package does not enforce additional demographic or patient-size thresholds. Validation is not a safety screen and does not make an accepted input clinically appropriate.

## Privacy boundary

This package performs calculations in the local process. It contains no network client, database, patient-file reader, telemetry, or tool-input logging. It does not intentionally retain input values after a tool call. MCP client software, operating systems, and deployment environments have their own data handling; users must assess those independently and must not disclose protected information unless authorized under their policies.

## Limitations of this notice

This notice is not legal, clinical, regulatory, or institutional approval. No claim is made that the software is a medical device or has been validated, certified, or cleared for clinical use. Any clinical deployment requires independent review, verification, validation, governance, and monitoring appropriate to its jurisdiction and use.

## References

[1]: https://cvphysiology.com/blood-pressure/bp006 "Mean Arterial Pressure — Cardiovascular Physiology Concepts"
[2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6698590/ "Shock index in the emergency department: utility and limitations"
