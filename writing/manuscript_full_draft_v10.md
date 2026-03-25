# Manuscript Full Draft v10

## Title

**Air pollution-attributable respiratory burden in East Asia: breakpoint trends, four-factor decomposition, and vulnerability profiling from GBD 2021**

## Running Title

**Four-factor respiratory burden transition in East Asia**

## Authors

**Zihao Liu**^1,2^, **Bing Li**^1,2,3*^

## Affiliations

^1^ Department of Respiratory and Critical Care Medicine, Shanghai Pulmonary Hospital, School of Medicine, Tongji University, Shanghai, China  
^2^ School of Medicine, Tongji University, Shanghai, China  
^3^ Shanghai Key Laboratory of Tuberculosis, Shanghai Pulmonary Hospital, School of Medicine, Tongji University, Shanghai, China

## Author Emails

- Zihao Liu: `lzhliu0803@163.com`
- Bing Li: `libing044162@163.com`

## Correspondence

Correspondence: **Bing Li**, Department of Respiratory and Critical Care Medicine, Shanghai Pulmonary Hospital, School of Medicine, Tongji University, Shanghai, China; Shanghai Key Laboratory of Tuberculosis, Shanghai Pulmonary Hospital, School of Medicine, Tongji University, Shanghai, China. Email: `libing044162@163.com`

## Abstract

### Background

Age-standardized trends alone may misrepresent East Asia's air pollution-attributable respiratory burden because demographic aging and vulnerability shifts can alter counts. We examined PM2.5-attributable chronic obstructive pulmonary disease (COPD), PM2.5-attributable lower respiratory infections (LRI), and ozone-attributable COPD using GBD 2021.

### Methods

We analyzed GBD 2021 estimates for China, Japan, Republic of Korea, East Asia, Global, and high Sociodemographic Index (High SDI) from 1990 to 2021. Analyses combined attributable burden, total burden, and population files; a constrained piecewise log-linear breakpoint analysis of annual age-standardized series; a four-factor accounting decomposition of count change into population growth, aging, underlying total disease rate change, and population attributable fraction (PAF) change; and age-sex vulnerability profiling. Sensitivity analyses repeated the assessment for `1990–2019`, compared raw versus capped implied PAF, used annual-chain decomposition, and reran COPD-death decomposition on the common age set after excluding structurally empty `<15` cells.

### Results

Under prespecified model comparisons allowing either no breakpoint or one breakpoint, the preferred specification for all 36 analyzed age-standardized series included one breakpoint. For PM2.5-attributable COPD deaths ASR, China and East Asia shifted from earlier increases to later declines after a 2009 breakpoint; for ozone-attributable COPD deaths ASR, both shifted around 2007. Aging pushed COPD burden counts upward in China and East Asia, whereas underlying total disease rate change pushed downward; PAF change amplified PM2.5-attributable COPD increases but reinforced decline for ozone-attributable COPD DALYs. For PM2.5-attributable LRI deaths, the under-5 share fell from 67.2% to 2.9% in China and from 66.2% to 2.8% in East Asia, while the global comparator remained higher in 2021 (23.1%). By 2021, the age-70-plus group dominated COPD DALY burden across East Asia for both PM2.5 and ozone. Sensitivity analyses preserved the main qualitative patterns, capped versus uncapped implied PAF gave identical results, and the common-age-set rerun preserved COPD-death net changes, with the largest differences concentrated in the population-growth and aging components and smaller corresponding shifts in the underlying-rate and PAF components.

### Conclusions

East Asia’s air pollution-attributable respiratory burden cannot be interpreted from age-standardized decline alone. Net attributable burden change reflected temporal inflection, demographic aging, underlying total disease-rate dynamics, PAF change, and concentration of residual burden in older age groups.

## Keywords

- Global Burden of Disease
- Air pollution
- PM2.5
- Ozone
- Chronic obstructive pulmonary disease
- Lower respiratory infections
- East Asia
- Population aging
- Decomposition analysis

## Background

Air pollution remains a major contributor to premature mortality and disability worldwide, and respiratory diseases are among the most policy-relevant outcomes within this burden structure [1,2]. Ambient particulate matter pollution (PM2.5) and ambient ozone pollution are both important drivers of respiratory burden, but they do not necessarily follow the same temporal pattern. In settings with prolonged air quality control efforts, age-standardized decline can create an overly optimistic interpretation if burden counts remain high or decline only modestly. For population health planning, it is therefore insufficient to ask only whether rates are falling; it is also necessary to ask how demographic change and vulnerable-group structure reshape the residual burden [1,7].

East Asia is a particularly informative setting in which to examine this problem. China, Japan, and the Republic of Korea have experienced different combinations of industrialization, environmental regulation, demographic aging, and epidemiologic transition, while the regional aggregate of East Asia provides a useful comparison point between country-specific and global patterns [3,7]. This raises two linked questions. First, when PM2.5-attributable respiratory burden begins to improve, does the regional burden recede in parallel, or is part of that gain offset by demographic pressure? Second, do PM2.5-attributable and ozone-attributable respiratory burden move in parallel within the same regional setting?

Recent GBD-based studies have described respiratory burden across countries and over time, including comparative work in China, Japan, and the Republic of Korea [3] and broader burden analyses in other global settings [4,5]. However, many such studies still emphasize descriptive trend summaries or fixed segmented APC approaches. This leaves three issues insufficiently resolved. First, burden counts and age-standardized rates can move in different directions, especially in rapidly aging populations. Second, apparent inflection points are often assumed rather than estimated. Third, the remaining burden may become concentrated in specific vulnerable groups, meaning that the public health interpretation of burden is not captured by an aggregate age-standardized trend alone.

Our earlier BMJ Open paper [3] was limited to PM2.5-attributable COPD in China, Japan, and the Republic of Korea through 2019 and relied mainly on comparative trend summaries. The present study materially expands that design by extending the window to 2021, adding PM2.5-attributable LRI and ozone-attributable COPD, incorporating East Asia, Global, and High SDI comparators, replacing fixed segmentation with prespecified breakpoint model comparison, upgrading the burden-change module to a four-factor accounting decomposition, and adding age-sex vulnerability profiling.

To address these limitations, we examined PM2.5-attributable COPD, PM2.5-attributable LRI, and ozone-attributable COPD across China, Japan, the Republic of Korea, East Asia, Global, and High SDI from 1990 to 2021 using GBD 2021. We replaced a fixed-year segmentation strategy with a data-driven breakpoint analysis, decomposed changes in attributable burden counts under a four-factor accounting identity separating population growth, aging, underlying total disease rate change, and PAF change, and profiled burden vulnerability by age and sex, with particular attention to under-5 LRI burden and age-70-plus COPD burden. Our objective was not only to describe temporal change, but also to clarify whether demographic headwinds were offset by changes in the total disease burden pool and the attributable fraction. The overall study design is summarized in Figure 1.

## Methods

### Data source

This was a secondary analysis of publicly accessible estimates from the Global Burden of Disease Study 2021 (GBD 2021) [1,2]. We focused on three risk-outcome pairs: PM2.5-attributable COPD, PM2.5-attributable LRI, and ozone-attributable COPD. Baseline GBD downloads provided annual all-age death counts, age-standardized death rates (ASR), and age-standardized DALY rates (ASDR) for both sexes. Additional downloads were performed to obtain age-specific attributable burden counts by sex, matched total disease burden counts for the same outcomes, and aligned population tables for the same years and locations.

### Study setting and outcomes

The comparison set comprised China, Japan, Republic of Korea, East Asia, Global, and High SDI. The primary outcomes were deaths (count), deaths ASR (per 100,000), DALYs (count), and DALYs ASDR (per 100,000).

### Data harmonization

Legacy baseline files and newer age-sex downloads used partially different label systems, including Chinese and English naming conventions. All files were harmonized into a unified long-format schema with standardized fields for risk, cause, measure, metric, location, sex, age group, year, value, and uncertainty bounds where available. Location names were harmonized to China, Japan, Republic of Korea, East Asia, Global, and High SDI. Age groups were retained as provided by the GBD export and assigned numeric sort keys to preserve age ordering. Baseline all-age death counts were cross-checked against summed age-sex death counts for each risk-outcome-location-year combination; numerical differences after harmonization were negligible.

### Breakpoint trend analysis

To replace the earlier fixed 2005 segmentation strategy, we performed a constrained piecewise log-linear breakpoint analysis on annual age-standardized series. Separate analyses were run for deaths ASR and DALYs ASDR for each risk-outcome-location combination.

Annual age-standardized rates were modeled on the log scale. Because the annual series contained 32 observations and we wanted interpretable pre-break and post-break segments with at least 8 years per segment, we prespecified model comparison only between no-breakpoint and one-breakpoint specifications. All legal breakpoint years satisfying the minimum segment length were enumerated, and the preferred model was selected using the Bayesian information criterion (BIC). Segment-specific annual percentage change (APC) was calculated as `100 × (exp(beta) − 1)`, where `beta` is the segment slope from the log-linear model. Approximate 95% confidence intervals for APC were derived from the ordinary least squares standard error of the segment slope. Overall average annual percentage change (AAPC) was calculated by weighting segment slopes by segment length.

This breakpoint procedure was intended as a constrained descriptive model comparison rather than a comprehensive change-point search. It was implemented as a pragmatic local segmentation strategy applied to annual point-estimate ASR/ASDR series and was not intended as a replication of the NCI Joinpoint software. Accordingly, breakpoint years were interpreted as empirical inflection estimates rather than policy-effect dates. The complete breakpoint model-comparison outputs for the main and `1990–2021` analysis and the `1990–2019` sensitivity analysis are provided in Additional file 1 and Additional file 2, respectively.

### Decomposition of burden count change

To explain changes in attributable burden counts over time, we decomposed deaths and DALYs under a four-factor accounting identity. For each risk-outcome-measure-location-sex combination, attributable burden counts were represented as:

`D_att = N × sum_a,s (share_a,s × rate_total_a,s × PAF_a,s)`

where `D_att` is attributable burden count, `N` is total population size, `share_a,s` is the age-sex population structure, `rate_total_a,s` is the total disease burden rate for the same age-sex cell, and `PAF_a,s` is the attributable fraction implied by `attributable burden / total burden` for that cell. For both-sex summaries, sex-specific age cells were retained internally so that the structure component represented age-sex composition rather than an age-only aggregate.

We used a symmetric permutation-average stepwise replacement, averaging contributions across all 24 possible update orders of the four components [6]. This approach avoids order dependence and yields a numerically closed partition of total count change. The resulting components were population growth, aging, underlying total disease rate change, and PAF change. Decomposition was performed for the full period `1990–2021`, the breakpoint-derived pre-break and post-break intervals, and both sexes, females, and males; the sex-stratified decomposition output is provided in Additional file 3. For COPD deaths, GBD output structure left the `<15` total-burden cells empty together with the corresponding attributable cells; 6,144 aligned age-sex-year-location-risk rows were affected, all restricted to PM2.5- and ozone-attributable COPD deaths in ages younger than 15 years. These structurally empty cells were retained as zero-valued accounting cells to preserve aligned age coverage.

### Sensitivity analyses

Because 2020–2021 overlapped with the COVID-19 period and could distort respiratory burden trajectories, we repeated the breakpoint analysis after truncating the series at 2019. Four-factor decomposition outputs were also generated for the `1990–2019` window using the corresponding sensitivity breakpoint year where available. Because implied PAF values can in principle exceed the `[0,1]` interval when derived from summary estimates, we also repeated the decomposition using capped PAF values. To assess dependence on a single `1990→2021` replacement jump, we additionally ran an annual-chain decomposition that summed year-to-year component contributions across each analysis window. Finally, for COPD deaths we reran the decomposition on the common age set after excluding the structurally empty `<15` cells entirely. These robustness outputs are provided in Additional file 4, Additional file 5, Additional file 6, and Additional file 7.

### Age-sex vulnerability profiling

We profiled age and sex structure using age-specific burden counts and aligned population tables. Two pre-specified vulnerable age categories were emphasized:

- under-5 years for PM2.5-attributable LRI
- age 70 years and older for COPD burden under both PM2.5 and ozone

For each risk-outcome-measure-location-year-sex combination, we calculated total burden count, burden count and share in the selected vulnerable age group, corresponding burden rates per 100,000 population, and the peak burden age group. The long-format vulnerability summary and peak-age outputs are provided in Additional file 8 and Additional file 9, respectively.

### Interpretation boundaries

Breakpoint years were interpreted as empirical inflection estimates rather than causal policy effects. The decomposition partitions count change under an accounting identity and should not be interpreted as individual-level causal inference. The underlying total disease rate should not be interpreted as independent of air pollution; rather, it reflects the composite evolution of the total disease burden pool under the GBD framework. The implied PAF was derived from summary attributable and total burden estimates to preserve algebraic closure and should not be interpreted as a draw-level official IHME PAF object. All-age DALY count uncertainty was not reconstructed from posterior draws; therefore, DALY count-based decompositions were interpreted as descriptive point-estimate summaries rather than precision-qualified component estimates.

## Results

### Long-term age-standardized burden patterns

Across the six comparison locations, age-standardized respiratory burden did not follow a single monotonic pattern, and under the prespecified comparison between no-breakpoint and one-breakpoint specifications, the preferred model for all analyzed series contained one breakpoint (Figure 2; Table 1). For PM2.5-attributable COPD deaths ASR, China and East Asia both increased through the late 2000s and declined thereafter. In China, APC changed from `3.07%` (`95% CI 2.61 to 3.53`) during `1990–2008` to `-6.32%` (`-7.23 to -5.39`) during `2009–2021`; East Asia showed a nearly identical transition from `3.02%` to `-6.28%`. Japan and the Republic of Korea showed long-term decline with different breakpoint years (`2010` and `1999`, respectively).

For PM2.5-attributable LRI deaths ASR, most locations showed decline, but post-break patterns were not uniform. China, East Asia, Japan, Global, and High SDI all showed steeper negative APCs after the breakpoint, with breakpoint years clustering around `2014`. By contrast, the Republic of Korea showed decline during `1990–2002` (`-3.50%`, `95% CI -4.15 to -2.84`) but increase after the 2003 breakpoint (`4.81%`, `3.79 to 5.83`).

For ozone-attributable COPD deaths ASR, China and East Asia showed increases before `2007` and steep declines thereafter. In China, deaths ASR rose by `2.38%` per year (`95% CI 2.18 to 2.58`) during `1990–2006` and fell by `-8.74%` (`-9.78 to -7.69`) during `2007–2021`. East Asia showed an almost identical pattern. The Republic of Korea retained a positive overall AAPC for ozone-attributable COPD deaths ASR. DALYs ASDR broadly mirrored the deaths ASR breakpoint structure, although exact breakpoint timing varied by metric and location.

### Breakpoint timing varied across locations and outcomes

Breakpoint timing differed materially across risk-outcome pairs and locations (Table 1). For PM2.5-attributable COPD deaths ASR, the selected breakpoint year was `2009` in China and East Asia, `2008` in Global, `2007` in High SDI, `2010` in Japan, and `1999` in the Republic of Korea. For PM2.5-attributable LRI, timing ranged from `2003` in the Republic of Korea to `2014` in China, East Asia, Japan, Global, and High SDI. For ozone-attributable COPD, China and East Asia aligned at `2007`, whereas Global and High SDI broke in `2009`, Japan in `2010`, and the Republic of Korea in `2001`.

DALYs ASDR showed similar but not identical timing. PM2.5-attributable COPD DALYs ASDR broke in `2009` in China and East Asia but in `2013–2014` in Japan and the Republic of Korea. PM2.5-attributable LRI DALYs ASDR showed an early break in China (`2002`) and East Asia (`2003`) but a later break in Japan and Global (`2014`). Thus, a fixed `2005` split would have obscured substantial heterogeneity in temporal patterning.

### Four-factor decomposition of burden count change

Figure 3 and Table 2 summarize the main both-sex `1990–2021` endpoint decomposition. For PM2.5-attributable COPD deaths in China, the net increase from 1990 to 2021 was `134,333`, with population growth contributing `37,802`, aging `204,047`, underlying total disease rate change `-222,150`, and PAF change `114,634`. East Asia showed a closely similar profile, with a net increase of `135,216`, aging contribution `204,997`, underlying-rate contribution `-219,864`, and PAF contribution `112,079`. For PM2.5-attributable COPD DALYs, positive demographic and PAF contributions outweighed negative underlying-rate contributions in both China and East Asia, yielding net increases of `2,000,433` and `2,012,020`, respectively.

PM2.5-attributable LRI showed a different four-factor pattern. In China and East Asia, PM2.5-attributable LRI deaths decreased overall (`-12,230` and `-11,459`, respectively), because the negative contribution from underlying total disease rate change (`-62,791` and `-60,373`) exceeded the positive contributions from population growth, aging, and PAF change. The same pattern extended to DALYs, with declines of `-2,203,917` in China and `-2,215,981` in East Asia despite positive PAF contributions of `1,744,505` and `1,537,404`.

Ozone-attributable COPD DALYs showed yet another configuration. In China and East Asia, large positive aging contributions (`1,429,508` and `1,455,375`) were almost fully offset by negative underlying-rate contributions (`-1,597,088` and `-1,617,098`) together with smaller negative PAF contributions (`-159,945` and `-136,976`), yielding slight net declines (`-37,808` and `-1,969`). In the global comparator, by contrast, the net change remained strongly positive (`3,458,817`) because positive population growth, aging, and PAF contributions outweighed the negative underlying-rate component.

### Vulnerability structure by age and sex

Vulnerability profiling showed a marked shift in the age composition of PM2.5-attributable LRI deaths between 1990 and 2021 (Figure 4; Additional file 8 and Additional file 9). In 1990, under-5 children accounted for `67.19%` of PM2.5-attributable LRI deaths in China and `66.23%` in East Asia, compared with `59.87%` globally. By 2021, the under-5 share had dropped to `2.89%` in China and `2.80%` in East Asia, whereas the global comparator still retained a larger under-5 share (`23.12%`). In parallel, the age-70-plus share of PM2.5-attributable LRI deaths rose to `73.12%` in China and `73.18%` in East Asia.

For COPD DALYs, the age-70-plus group dominated burden composition across all locations in both PM2.5 and ozone analyses. In China, the age-70-plus share of ozone-attributable COPD DALYs increased from `53.95%` in 1990 to `71.72%` in 2021; East Asia showed a similar increase from `53.88%` to `71.12%`. For PM2.5-attributable COPD DALYs, the age-70-plus share increased from `52.17%` to `68.01%` in China and from `52.12%` to `67.90%` in East Asia. Japan showed the most elderly-skewed COPD burden structure in 2021.

### Sensitivity to exclusion of the pandemic period

The `1990–2019` sensitivity analysis preserved the main direction of the breakpoint findings, although breakpoint years and overall AAPC values shifted modestly in some locations (Additional file 2). For example, the selected breakpoint year for ozone-attributable COPD deaths ASR in China remained unchanged at `2007` in both the sensitivity and full analyses. Within the four-factor module, capped and uncapped implied PAF produced identical decomposition results because no aligned age-sex cell exceeded the `[0,1]` bounds (Additional file 4). Annual-chain decomposition changed component magnitudes but preserved the substantive pattern of positive demographic pressure against negative underlying-rate contributions for COPD and dominant negative underlying-rate contributions for PM2.5-attributable LRI (Additional file 5). Excluding structurally empty `<15` COPD-death cells from the accounting table preserved net changes, with the largest differences concentrated in the redistribution between population-growth and aging components and smaller corresponding shifts in the underlying-rate and PAF components (Additional file 6). The `1990–2019` four-factor rerun also preserved the main accounting interpretation (Additional file 7). These checks support the robustness of the main accounting interpretation while acknowledging that the pandemic period may still have affected absolute burden estimates.

## Discussion

Rather than serving as a simple time-update of earlier regional GBD summaries, this study adds an explanation-oriented comparative layer to the interpretation of air pollution-attributable respiratory burden in East Asia. Its distinct value rests on a three-part upgrade: the addition of PM2.5-attributable LRI and ozone-attributable COPD beyond a single outcome focus, the East Asia/Global/High SDI comparative frame beyond a three-country comparison, and the combination of prespecified breakpoint model comparison, a numerically closed four-factor accounting decomposition, and age-sex vulnerability profiling beyond routine descriptive trend reporting. Three findings are central. First, age-standardized respiratory burden did not change monotonically across the study period, and under the prespecified comparison between no-breakpoint and one-breakpoint models, the one-break specification was preferred for every analyzed series. Second, burden count change was strongly shaped by demographic pressure, especially aging, but the non-demographic counterweight was not a single generic rate term; it consisted of changes in the total disease burden rate and in the attributable fraction. Third, the remaining burden became increasingly concentrated in older age groups, especially for COPD, while the pediatric share of PM2.5-attributable LRI deaths in East Asia became much smaller than that observed in the global comparator.

The breakpoint results show that East Asia cannot be summarized using a single common inflection year. China and East Asia showed similar timing for PM2.5-attributable COPD and ozone-attributable COPD, but Japan and the Republic of Korea often followed different patterns. This finding weakens any simple narrative of a uniform regional burden trajectory and instead points to heterogeneous temporal change within the region [3,4].

The four-factor decomposition helps reconcile why burden counts and age-standardized rates can point in different directions. It also clarifies that the older “age-specific attributable rate change” term was mixing two distinct accounting channels: change in the total disease burden pool and change in the attributable fraction under the GBD comparative risk assessment framework. Across PM2.5-attributable COPD and ozone-attributable COPD, aging remained the dominant upward demographic force in China and East Asia, whereas underlying total disease rate change contributed downward pressure. PAF change, however, did not move uniformly: it amplified PM2.5-attributable COPD increases in China and East Asia but reinforced decline for ozone-attributable COPD DALYs. Thus, a declining ASR should not be taken to mean that the burden problem is receding at the same speed in population terms. In rapidly aging settings, demographic pressure can partly or largely offset improvement in the underlying disease burden rate, and PAF dynamics can either attenuate or amplify that balance [6,7].

This issue was particularly visible for ozone-attributable COPD. In China and East Asia, the net change in ozone-attributable COPD DALYs from 1990 to 2021 was small relative to the size of the underlying aging component because downward total-rate and PAF contributions nearly cancelled the demographic increase. In contrast, the global comparator still showed a large positive net change, with positive PAF change contributing alongside demographic expansion. PM2.5-attributable LRI illustrated a different configuration: the overall decline was driven mainly by falling total LRI burden rates, while positive PAF contributions partly offset that decline. Within the selected respiratory outcomes examined here, PM2.5-attributable and ozone-attributable burden trajectories were therefore not interchangeable, and neither can be summarized as a simple one-channel improvement story.

The vulnerability profile adds an important population-health dimension to this interpretation. For PM2.5-attributable LRI deaths, East Asia in 1990 still exhibited a strongly child-centered burden structure, but by 2021 the under-5 share had fallen sharply and the burden composition had become markedly older. Meanwhile, the global comparator retained a much larger pediatric share in 2021. For COPD DALYs, the age-70-plus group accounted for a dominant share of burden across East Asia in both PM2.5 and ozone analyses by 2021. These findings suggest that East Asia’s residual respiratory burden is increasingly one of aging populations rather than one dominated by pediatric burden [7,8].

The study has several strengths. It used a consistent East Asia-centered comparison framework, replaced an arbitrary segmented trend design with a reproducible breakpoint search, and linked temporal trends to a numerically closed four-factor accounting decomposition aligned with the GBD comparative risk assessment logic. It also embedded age and sex profiling into the mainline analysis, allowing the burden story to be interpreted through a vulnerability lens rather than through rates alone. In addition, the decomposition module was stress-tested with a `1990–2019` rerun, capped-PAF comparison, and annual-chain alternative path calculation, and the structured manuscript-packaging reproducibility bundle is provided as Additional file 10.

Several limitations should also be recognized. First, all estimates derive from the GBD 2021 framework and therefore inherit the assumptions, modelling structure, and uncertainty architecture of GBD [1,2]. Second, the breakpoint analysis was implemented as a local piecewise log-linear search rather than the NCI Joinpoint software itself; the resulting breakpoints should therefore be interpreted as empirical inflection estimates within the prespecified 0-versus-1-break model space rather than as exact policy turning points. Third, the four-factor decomposition is an accounting decomposition and does not provide individual-level or mechanistic causal inference [6]. The underlying total disease rate is a composite quantity rather than a channel independent of air pollution, and the implied PAF was derived from summary attributable and total burden estimates rather than official draw-level PAF outputs. Fourth, COPD death exports contained structurally empty `<15` cells in 6,144 aligned rows; these were handled consistently in the main accounting table, and a common-age-set sensitivity analysis preserved net changes while indicating that the largest differences were concentrated in the population-growth and aging components, with smaller corresponding shifts in the underlying-rate and PAF components. Fifth, all-age DALY count uncertainty was not reconstructed from posterior draws, so DALY count-based decompositions should be interpreted as descriptive point-estimate summaries. Finally, a validated China provincial risk-attributable branch was not included in the active mainline, which limits inference on within-China spatial heterogeneity.

## Conclusions

East Asia’s air pollution-attributable respiratory burden cannot be adequately summarized by age-standardized decline alone. Across the selected respiratory outcomes, burden trajectories reflected the interaction of temporal inflection, demographic aging, underlying total disease-rate dynamics, PAF change, and vulnerable-group concentration. The key public health message is therefore not simply that some rates have improved, but that demographic pressure is reshaping how much burden remains, how large the underlying disease pool is, and what share of that pool remains attributable to air pollution.

## List of abbreviations

- `AAPC`: average annual percentage change
- `APC`: annual percentage change
- `ASDR`: age-standardized DALY rate
- `ASR`: age-standardized death rate
- `COPD`: chronic obstructive pulmonary disease
- `DALY`: disability-adjusted life year
- `GBD`: Global Burden of Disease
- `IHME`: Institute for Health Metrics and Evaluation
- `LRI`: lower respiratory infections
- `PAF`: population attributable fraction
- `PM2.5`: fine particulate matter with aerodynamic diameter less than or equal to 2.5 micrometers
- `SDI`: Sociodemographic Index

## Declarations

## Ethics approval and consent to participate

Ethics approval was not required for this secondary analysis because it used publicly accessible, de-identified, aggregate GBD estimates and did not involve identifiable human participants.

## Consent for publication

Not applicable.

## Availability of data and materials

The public GBD 2021 data analysed during the current study are available from the IHME GBD Results Tool [9], subject to IHME terms of use. Raw downloaded GBD files are not redistributed. Submission-facing robustness outputs are provided as Additional file 1 through Additional file 9. A structured code and packaging bundle containing the exact download manifest, current analysis-ready inputs, author-generated harmonized tables, and the scripts used for harmonization, breakpoint analysis, four-factor decomposition, vulnerability profiling, publication-table generation, figure generation, and submission-package construction is provided as journal Additional file 10 (`__REPRO_BUNDLE_FILENAME__`). At the time of submission, no separate repository DOI had been assigned; the archived peer-review version of the software and packaging bundle is therefore the journal-hosted Additional file 10 itself. Software and code metadata for Additional file 10 are as follows: project name, East Asia respiratory burden manuscript package; project home page, not applicable because the archived bundle accompanies the submission directly; archived version, journal Additional file 10 (`__REPRO_BUNDLE_FILENAME__`); operating system, Linux (validated on an Ubuntu-compatible server); programming language, Python 3; other requirements, a standard scientific Python environment with `pandas`, `matplotlib`, and `python-docx`; license, custom manuscript-companion use notice included in the bundled `LICENSE` file; restrictions for non-academic use, commercial reuse requires written permission from the authors and source-data reuse remains subject to the underlying IHME terms of use.

## Competing interests

The authors declare that they have no competing interests.

## Funding

This study received no specific external funding.

## Authors' contributions

ZL conceived the study, designed the analytical workflow, performed data curation, formal analysis, visualization, and manuscript drafting. BL supervised the study, contributed to interpretation of the findings, critically revised the manuscript for important intellectual content, and approved the final version as corresponding author. All authors read and approved the final manuscript.

## Acknowledgements

We acknowledge the Institute for Health Metrics and Evaluation and the Global Burden of Disease Study 2021 collaborators for making the underlying estimates publicly accessible.

## Additional files

- Additional file 1. `breakpoint_model_comparison_1990_2021.csv` (CSV): model comparison output for the main `1990–2021` breakpoint analysis across all age-standardized series.
- Additional file 2. `breakpoint_model_comparison_1990_2019.csv` (CSV): breakpoint model comparison output for the `1990–2019` sensitivity analysis.
- Additional file 3. `four_factor_decomposition_all_periods_by_sex.csv` (CSV): sex-stratified four-factor decomposition output for the main and sensitivity windows, including the full, pre-break, and post-break analysis intervals.
- Additional file 4. `four_factor_decomposition_capped_paf_both.csv` (CSV): both-sex four-factor decomposition rerun using capped implied PAF values.
- Additional file 5. `four_factor_decomposition_annual_chain_both.csv` (CSV): both-sex four-factor decomposition rerun using annual-chain accumulation.
- Additional file 6. `four_factor_decomposition_common_age_set_both.csv` (CSV): both-sex four-factor decomposition rerun for COPD deaths after excluding structurally empty `<15` cells.
- Additional file 7. `four_factor_decomposition_sensitivity_both.csv` (CSV): both-sex four-factor decomposition rerun for the `1990–2019` sensitivity window.
- Additional file 8. `vulnerability_focus_long.csv` (CSV): long-format vulnerability summary file for pre-specified under-5 and age-70-plus burden shares.
- Additional file 9. `vulnerability_peak_age_long.csv` (CSV): long-format peak-age vulnerability output.
- Additional file 10. `__REPRO_BUNDLE_FILENAME__` (ZIP): audit and manuscript-packaging bundle containing the current source files, analysis-ready inputs, output tables, QC logs, and scripts required to rebuild the manuscript-facing tables, figures, and submission package.

## References

1. GBD 2021 Risk Factors Collaborators. Global burden and strength of evidence for 88 risk factors in 204 countries and 811 subnational locations, 1990–2021: a systematic analysis for the Global Burden of Disease Study 2021. Lancet. 2024;403:2162-2203. doi:10.1016/S0140-6736(24)00933-4.
2. GBD 2021 Causes of Death Collaborators. Global burden of 288 causes of death and life expectancy decomposition in 204 countries and territories and 811 subnational locations, 1990–2021: a systematic analysis for the Global Burden of Disease Study 2021. Lancet. 2024;403:2100-2132. doi:10.1016/S0140-6736(24)00367-2.
3. Cheng X-F, Min S-H, Guo R-Q, Zhang J-D, Zhang Y-L, Li B. Disease burden of COPD attributable to PM2.5 in China, Japan and South Korea from 1990 to 2019: a comparative study based on Global Burden of Disease Study 2019. BMJ Open. 2024;14(2):e078887. doi:10.1136/bmjopen-2023-078887.
4. Wu Y, Ning P, Rao Z, Li L, Schwebel DC, Cheng P, et al. Burden of disease in the Belt and Road countries from 1990 to 2021: analysis of estimates from the Global Burden of Disease 2021. Glob Health Res Policy. 2025;10:20. doi:10.1186/s41256-025-00403-3.
5. Liu J, Xu T, Wang Y, Ji F, Zhang L. The spatio-temporal trends and determinants of liver cancer attributable to specific etiologies: a systematic analysis from the Global Burden of Disease Study 2021. Glob Health Res Policy. 2025;10:22. doi:10.1186/s41256-025-00416-y.
6. Cheng X, Yang Y, Schwebel DC, Liu Z, Li L, Cheng P, et al. Population ageing and mortality during 1990-2017: a global decomposition analysis. PLoS Med. 2020;17(6):e1003138. doi:10.1371/journal.pmed.1003138.
7. Health Effects Institute. State of Global Air report 2024. Special report. Boston, MA: Health Effects Institute; 2024. https://www.stateofglobalair.org/resources/archived/state-global-air-report-2024. Accessed 25 Mar 2026.
8. GBD 2021 Lower Respiratory Infections and Antimicrobial Resistance Collaborators. Global, regional, and national incidence and mortality burden of non-COVID-19 lower respiratory infections and aetiologies, 1990-2021: a systematic analysis from the Global Burden of Disease Study 2021. Lancet Infect Dis. 2024;24(9):974-1002. doi:10.1016/S1473-3099(24)00176-2.
9. Institute for Health Metrics and Evaluation. Global Burden of Disease Study 2021 (GBD 2021) Results Tool. https://vizhub.healthdata.org/gbd-results/. Accessed 25 Mar 2026.
