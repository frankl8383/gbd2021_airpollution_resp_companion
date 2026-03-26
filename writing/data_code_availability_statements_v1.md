# Data And Code Availability Statements v1

## Data Availability Statement

The public GBD 2021 estimates analysed during the current study are available from the Institute for Health Metrics and Evaluation (IHME) GBD Results Tool. Raw downloaded GBD files are not redistributed. Submission-facing robustness outputs are provided as numbered additional files with the manuscript. A structured code and packaging bundle containing the exact download manifest, current analysis-ready inputs, author-generated harmonized tables, and the manuscript-facing build scripts is provided as journal Additional file 10.

## Code Availability Statement

The code used for harmonization, breakpoint analysis, four-factor decomposition, vulnerability profiling, publication-asset generation, and submission-package construction is included in the structured reproducibility bundle provided as journal Additional file 10. The bundle is an archived manuscript companion rather than a separate software repository. A public mirror is available [10], and the archived Zenodo record for the current submission state is available [11]. Additional file 10 is the exact peer-review snapshot of the submission-facing bundle; the public mirror and Zenodo archive provide the corresponding public companion record of the workflow. Recommended software metadata for the manuscript are: project name, East Asia respiratory burden manuscript package; project home page, reference [10]; archived version, Zenodo DOI [11] and journal Additional file 10; operating system, Linux (validated on an Ubuntu-compatible server); programming language, Python 3; other requirements, `pandas`, `matplotlib`, and `python-docx`; license, custom manuscript-companion use notice included in the bundled `LICENSE` file; restrictions for non-academic use, commercial reuse requires written permission from the authors and source-data reuse remains subject to the underlying IHME terms of use.

## Reproducibility Note

The bundle includes:

- download manifest
- current analysis-ready inputs required for manuscript-facing figure and table regeneration
- harmonization scripts
- four-factor decomposition and robustness scripts
- vulnerability profiling scripts
- manuscript drafting assets
- publication-ready figure and table builders
- submission-package builder

Raw IHME downloads are not redistributed, but the bundle is organized so that the manuscript-facing tables, figures, and submission package can be rebuilt from the included inputs.
