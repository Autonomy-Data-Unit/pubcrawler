# Change Log

See RELEASES.txt for the commit hashes for each release.


## [0.2.1] - 2023-08-22

### Changed

- Removed MANIFEST.in as it is superceded by pyproject.toml
- `prepare_project.py` no longer commits and pushes changes at the end.
- Changed the name of the template to `adu-template-main`.
- Ask whether to add `adu-tools` as a dev or prod dependency.
- removed utils cli and moved to adu_proj
- Changed the default python requirement to `>=given_python_version`.

### Added

- Creates a file envname, which stores the name of the environment used for the project.
- Changed `settings.ini` to allow for `slideshow` cell metadata in notebooks.

### Fixed

- Added '<3.13' into the Python range specification, to avoid conflicts with numpy.

## [0.2.0] - 2023-08-14

### Added

- Added a `CHANGELOG.md` to keep track of changes to this template.

- Added a `CHANGELOG_template.md` for use in projects.

- Moved the `data`, `log`, `pre_output` and `output` folders into the `store` directory in the module directory, and changed the `const` variables accordingly.
This is mainly because when python wheels are installed, it doesn't have a nested `site_pacakges/adu_template_main/adu_template_main` structure, but rather a single
`site_pacakges/adu_template_main` structure. Therefore, all storage needs to be inside the module directory.

- Moved the `fetch_spec.json` into the module directory.


## [0.1.0] - 2023-08-13

Commit: 2b492ec960ca4953d1f38097eb07baac6e2c13bd

First version of the ADU project template
