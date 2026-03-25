# Data And Code Availability Statements v1

## Data Availability Statement

The public GBD 2021 estimates analysed during the current study are available from the Institute for Health Metrics and Evaluation (IHME) GBD Results Tool. Raw downloaded GBD files are not redistributed. Submission-facing robustness outputs are provided as numbered additional files with the manuscript. A structured code and packaging bundle containing the exact download manifest, current analysis-ready inputs, author-generated harmonized tables, and the manuscript-facing build scripts is provided as journal Additional file 10.

## Code Availability Statement

The code used for harmonization, breakpoint analysis, four-factor decomposition, vulnerability profiling, publication-asset generation, and submission-package construction is included in the structured reproducibility bundle provided as journal Additional file 10. The bundle is an archived manuscript companion rather than a separate software repository. No separate repository DOI has been assigned at submission; the archived peer-review version is therefore journal Additional file 10 itself. Recommended software metadata for the manuscript are: project name, East Asia respiratory burden manuscript package; project home page, not applicable because the archived bundle accompanies the submission directly; archived version, journal Additional file 10; operating system, Linux (validated on an Ubuntu-compatible server); programming language, Python 3; other requirements, `pandas`, `matplotlib`, and `python-docx`; license, custom manuscript-companion use notice included in the bundled `LICENSE` file; restrictions for non-academic use, commercial reuse requires written permission from the authors and source-data reuse remains subject to the underlying IHME terms of use.

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
