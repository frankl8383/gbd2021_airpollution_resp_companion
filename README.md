# East Asia Respiratory Burden Manuscript Companion

This public repository is the manuscript-companion mirror for the East Asia
air pollution-attributable respiratory burden study prepared for journal
submission in March 2026.

Current public freeze:
- `BMC_submission_package_v31.zip`
- `BMC_reproducibility_bundle_v29.zip`
- Latest public release: `bmc-v31`
- License for manuscript-companion materials: `CC BY 4.0`

It preserves the source files, breakpoint-ready summary input,
manuscript-facing tables, figures, QC outputs, and build scripts needed to
audit the submitted package and regenerate manuscript-facing assets from the
bundled audit inputs.

## Scope

- Journal-facing route: `BMC Public Health`
- This repository is not a full raw-data or full analysis-pipeline rerun archive.
- Raw IHME/GBD downloads are not redistributed.

## Recommended Release Assets

The current journal-facing freeze uses the package pair listed below. The same
freeze is distributed as GitHub release assets, while the linked Zenodo
concept DOI serves as the stable archive-family entry for the public record:

- `BMC_submission_package_v31.zip`
- `BMC_reproducibility_bundle_v29.zip`
- Releases page: `https://github.com/frankl8383/gbd2021_airpollution_resp_companion/releases`
- Current frozen release: `https://github.com/frankl8383/gbd2021_airpollution_resp_companion/releases/tag/bmc-v31`
- Archived Zenodo concept DOI: `https://doi.org/10.5281/zenodo.19222088`

The same manuscript-companion content is also preserved directly in this public
repository tree for audit and manuscript-facing regeneration. Complete
harmonization, four-factor decomposition, and vulnerability reruns require
upstream raw or intermediate inputs that are not redistributed here.

## Rebuild Entry Point

- Main package builder: `python3 scripts/70_build_submission_package.py`
- Expected output root: `submission_packages/`
- The builder creates `submission_packages/` automatically if it does not
  already exist
- In a clean unzip environment, regenerated package labels restart from
  `v1/current`; these regenerated labels are non-archival convenience outputs,
  while the archived peer-review snapshot remains the frozen package pair
  listed above

See `RUN_STATUS.md` in the bundled reproducibility archive for script-by-script
run scope and internal table-to-manuscript mapping.

## Software Metadata

- Project name: East Asia respiratory burden manuscript package
- Project home page: this public manuscript-companion repository
- Archived version: Zenodo concept DOI `10.5281/zenodo.19222088`
- Operating system: Linux (validated on an Ubuntu-compatible server)
- Programming language: Python 3
- Other requirements: standard scientific Python environment with `pandas`,
  `matplotlib`, and `python-docx`
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) as stated
  in the bundle-root [LICENSE](LICENSE)
- Restrictions for non-academic use: none beyond attribution for the
  manuscript-companion materials; source-data reuse remains subject to IHME
  terms

## Scope Note

This freeze contains only the BMC route and is intended for journal submission
and external audit of the BMC package.
