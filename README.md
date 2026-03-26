# East Asia Respiratory Burden Manuscript Companion

This public repository is the manuscript-companion mirror for the East Asia
air pollution-attributable respiratory burden study prepared for journal
submission in March 2026.

It preserves the source files, analysis-ready inputs, manuscript-facing tables,
 figures, QC outputs, and build scripts needed to audit and rebuild the
submission-facing assets from the included current inputs.

## Scope

- Journal-facing route: `BMC Public Health`
- This repository is not a full raw-data rerun archive.
- Raw IHME/GBD downloads are not redistributed.

## Recommended Release Assets

The current journal-facing freeze uses the package pair listed below. The same
freeze is distributed as GitHub release assets and archived through the linked
Zenodo concept record:

- `BMC_submission_package_v19.zip`
- `BMC_reproducibility_bundle_v17.zip`
- Releases page: `https://github.com/frankl8383/gbd2021_airpollution_resp_companion/releases`
- Archived Zenodo concept DOI: `https://doi.org/10.5281/zenodo.19222088`

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
- Archived version: Zenodo concept DOI `10.5281/zenodo.19222088`
- Operating system: Linux (validated on an Ubuntu-compatible server)
- Programming language: Python 3
- Other requirements: standard scientific Python environment with `pandas`,
  `matplotlib`, and `python-docx`
- License: custom manuscript-companion use notice in the bundle-root
  [LICENSE](LICENSE)
- Restrictions for non-academic use: commercial reuse requires written
  permission from the authors; source-data reuse remains subject to IHME terms

## Scope Note

This freeze contains only the BMC route and is intended for journal submission
and external audit of the BMC package.
