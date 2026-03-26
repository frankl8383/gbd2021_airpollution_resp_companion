# Data And Code Availability Statements v1

## Data Availability Statement

The public GBD 2021 estimates analysed during the current study are available from the Institute for Health Metrics and Evaluation (IHME) GBD Results Tool. Raw downloaded GBD files are not redistributed. Submission-facing robustness outputs are provided as numbered additional files with the manuscript. A structured code and packaging bundle containing the exact download manifest, the breakpoint-ready summary panel, manuscript-facing output tables and figures, QC logs, and the manuscript-facing build scripts is provided as journal Additional file 10.

## Code Availability Statement

The code used for manuscript-facing breakpoint rerun, publication-asset generation, and submission-package construction is included in the structured reproducibility bundle provided as journal Additional file 10. The bundle is an archived manuscript companion rather than a separate software repository. A public mirror is available [10], and the Zenodo concept DOI family entry for the public archive is available [11]. Additional file 10 is the exact peer-review snapshot of the submission-facing bundle; the public mirror provides the project-home discovery route, and the Zenodo concept DOI provides the stable public archive-family entry for the workflow. Recommended software metadata for the manuscript are: project name, East Asia respiratory burden manuscript package; project home page, reference [10]; archived version, Zenodo concept DOI [11] and journal Additional file 10; operating system, Linux (validated on an Ubuntu-compatible server); programming language, Python 3; other requirements, `pandas`, `matplotlib`, and `python-docx`; license, Creative Commons Attribution 4.0 International (CC BY 4.0) for the manuscript-companion materials as stated in the bundled `LICENSE` file; restrictions for non-academic use, none beyond attribution for the manuscript-companion materials, while reuse of underlying IHME/GBD source data remains subject to the underlying IHME terms of use.

## Reproducibility Note

The bundle includes:

- download manifest
- breakpoint-ready summary input required for breakpoint rerun
- manuscript-facing output tables, figures, and QC files
- harmonization, decomposition, and vulnerability scripts for audit
- manuscript drafting assets
- publication-ready figure and table builders
- submission-package builder

Raw IHME downloads are not redistributed. The bundled inputs are sufficient for breakpoint rerun and for regeneration of the manuscript-facing tables, figures, and submission package. Complete harmonization, four-factor decomposition, and vulnerability reruns require upstream raw or intermediate inputs that are not redistributed in the journal bundle. Script-by-script run scope is documented in the bundled `RUN_STATUS.md`.
