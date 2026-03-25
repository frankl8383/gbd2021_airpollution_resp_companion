# GBD Download Schema Reference

## Minimum Header Contract

Each GBD CSV used in the upgraded workflow should contain the following required columns:

- `location_name`
- `year`
- `val`
- `upper`
- `lower`

## Preferred Metadata Columns

These are not always required for downstream code, but they should be preserved whenever available:

- `population_group_id`
- `population_group_name`
- `measure_id`
- `measure_name`
- `location_id`
- `sex_id`
- `sex_name`
- `age_id`
- `age_name`
- `cause_id`
- `cause_name`
- `rei_id`
- `rei_name`
- `metric_id`
- `metric_name`

## Harmonized Concepts

### Risk

- `pm25`
- `ozone`
- `population`

### Cause

- `copd`
- `lri`
- `na` for population files

### Measure

- `deaths`
- `dalys`
- `population`

### Metric

- `number`
- `rate`

### Age Scope

- `all-ages`
- `age-specific`
- `age-standardized`

### Sex Scope

- `both`
- `mf`

## Current Analysis Mapping

- descriptive 2021 cross-sections need all-age numbers and age-standardized rates
- joinpoint and trend redesign need age-standardized rates
- decomposition needs age-specific counts plus population
- vulnerability profiling needs age-specific counts and population
- provincial heterogeneity needs at least provincial all-age numbers and age-standardized rates

