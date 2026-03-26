# East Asia Respiratory Burden Manuscript Companion

This public repository is the manuscript-companion mirror for the East Asia
air pollution-attributable respiratory burden study prepared for journal
submission in March 2026.

It preserves the source files, analysis-ready inputs, manuscript-facing tables,
 figures, QC outputs, and build scripts needed to audit and rebuild the
submission-facing assets from the included current inputs.

## Scope

- Journal-facing route: `BMC Public Health`
- Companion source commit in the private working repository:
  `78f1a89c6d7e4626784275f6f8f1c66a3191f2eb`
- This repository is not a full raw-data rerun archive.
- Raw IHME/GBD downloads are not redistributed.

## Recommended Release Assets

The current journal-facing freeze uses a later local package pair
(`BMC_submission_package_v17.zip` and `BMC_reproducibility_bundle_v15.zip`),
while the latest public archival record is the Zenodo-mirrored GitHub release
listed below.

The matched public archival artifacts are distributed as GitHub release assets
and archived on Zenodo:

- `BMC_submission_package_v16.zip`
- `BMC_reproducibility_bundle_v14.zip`
- Releases page: `https://github.com/frankl8383/gbd2021_airpollution_resp_companion/releases`
- Archived Zenodo DOI: `https://doi.org/10.5281/zenodo.19222089`

The same manuscript-companion content is also preserved directly in this public
repository tree for audit and rebuild purposes.

## Rebuild Entry Point

- Main package builder: `python3 scripts/70_build_submission_package.py`
- Expected output root: `submission_packages/`
- The builder creates `submission_packages/` automatically if it does not
  already exist

## Software Metadata

- Project name: East Asia respiratory burden manuscript package
- Project home page: this public manuscript-companion repository
- Archived version: Zenodo DOI `10.5281/zenodo.19222089`
- Operating system: Linux (validated on an Ubuntu-compatible server)
- Programming language: Python 3
- Other requirements: standard scientific Python environment with `pandas`,
  `matplotlib`, and `python-docx`
- License: custom manuscript-companion use notice in the bundle-root
  [LICENSE](LICENSE)
- Restrictions for non-academic use: commercial reuse requires written
  permission from the authors; source-data reuse remains subject to IHME terms

## Scope Note

Only the BMC route is journal-facing in this freeze. The retained Archives
route in the builder is included solely for internal compatibility and should
be ignored for submission or external audit of the BMC package.
