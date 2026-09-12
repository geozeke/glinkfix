# Changelog

All notable changes to glinkfix are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses canonical release versions.

## [2.2.4] - 2026-09-12

[Compare with 2.2.3](https://github.com/geozeke/glinkfix/compare/v2.2.3...v2.2.4)

### Dependencies

- *(deps)* Bump astral-sh/setup-uv from 9.0.0 to 10.0.1 ([b87ce70](https://github.com/geozeke/glinkfix/commit/b87ce7028bf92f245061ecec5a59b4acf83eedc9))
- *(deps-dev)* Bump ruff in the python-dependencies group (#110) ([5e41783](https://github.com/geozeke/glinkfix/commit/5e41783996c5907b05b701e3963aacd8dab6f0ba))
- *(deps-dev)* Bump ruff in the python-dependencies group (#111) ([adb54ef](https://github.com/geozeke/glinkfix/commit/adb54efedf56a04ae88c2ae90fe28debd701aa78))
- *(deps-dev)* Bump ruff in the python-dependencies group (#112) ([2ae6542](https://github.com/geozeke/glinkfix/commit/2ae6542ce9c6a4aaccc939643a12d960c3f8f558))

## [2.2.3] - 2026-08-21

[Compare with 2.2.3rc3](https://github.com/geozeke/glinkfix/compare/v2.2.3rc3...v2.2.3)

### Deployment & Operations

- Add command for local quality runs ([a7c58d0](https://github.com/geozeke/glinkfix/commit/a7c58d0ae46f3d2f1bf427dae0bca646f6475abc))

### Documentation

- Perform documentation audit. ([eb76905](https://github.com/geozeke/glinkfix/commit/eb7690551625b65022aedd67e6b73ff963e03b07))

### Dependencies

- *(deps)* Bump actions/checkout from 5 to 7 ([d9cf2c2](https://github.com/geozeke/glinkfix/commit/d9cf2c2be76cb23c8ec96b17a69a78a267165bce))
- *(deps-dev)* Bump mypy from 1.20.2 to 2.3.0 ([0717739](https://github.com/geozeke/glinkfix/commit/07177397a5608670658f254d81f36586bbaa46f1))
- *(deps)* Bump astral-sh/setup-uv from 8.1.0 to 9.0.0 ([964645d](https://github.com/geozeke/glinkfix/commit/964645dd4ebc75414ca4d8ac43f7457d5da5cf6d))
- *(deps)* Bump actions/upload-artifact from 4 to 7 ([49b367e](https://github.com/geozeke/glinkfix/commit/49b367e5bf68fc120709832d505bb91b20c2f7bd))
- *(deps)* Bump extractions/setup-just from 3 to 4 ([45a51da](https://github.com/geozeke/glinkfix/commit/45a51dae9a82284c345cbd5b7045c63448f6fb1f))
- *(deps-dev)* Bump ruff in the python-dependencies group (#106) ([b6f2da6](https://github.com/geozeke/glinkfix/commit/b6f2da6fe18f0b375cf13bfe78591aa071bac84e))
- *(deps-dev)* Bump the python-dependencies group with 2 updates (#107) ([e02ce43](https://github.com/geozeke/glinkfix/commit/e02ce430ad5d06a1fac4b0b63cfa1545784ec577))

## [2.2.3rc3] - 2026-08-02

[Compare with 2.2.3rc2](https://github.com/geozeke/glinkfix/compare/v2.2.3rc2...v2.2.3rc3)

### Documentation

- Perform a documentation audit ([49f2ff8](https://github.com/geozeke/glinkfix/commit/49f2ff874aeb6d5a20ef594fc480cca6285ab363))

## [2.2.3rc2] - 2026-08-02

[Compare with 2.2.3rc1](https://github.com/geozeke/glinkfix/compare/v2.2.3rc1...v2.2.3rc2)

### Deployment & Operations

- Tune release tooling ([beb02e8](https://github.com/geozeke/glinkfix/commit/beb02e894402b7e2e8c25f0faeb17a23bac4cac9))

## [2.2.3rc1] - 2026-08-02

[Compare with 2.2.2](https://github.com/geozeke/glinkfix/compare/v2.2.2...v2.2.3rc1)

### Deployment & Operations

- Upgrade changelog and release pipelines (#90) ([3e3559c](https://github.com/geozeke/glinkfix/commit/3e3559cd1a069b6dd84c3b2e1324d34ede1bbb7e))

## [2.2.2] - 2026-07-03

### Changed

- Prevent latest tagging of beta builds (0faa345)

### Removed

- Remove "dev" recipe from justfile (bda0d17)

### Fixed

- Lint project tooling (184fc5e)

### Dependencies

- DEPS-See commit msg for list (0a54dd7)
- DEPS-See commit msg for list (434363a)
- DEPS-See commit msg for list (552413e)
- DEPS-See commit msg for list (c63537d)

## [2.2.1] - 2026-05-23

### Changed

- Add github release workflow (d7f618d)

### Fixed

- Fix broken links in README (cc3ef62)

## [2.2.0] - 2026-05-22

### Added

- Allow for selective tagging (786a721)
- Handle more link types (#78) (36b4345)
- Add more command line options (#79) (31f85ab)

### Changed

- Migrate release generation to cliff (2f62157)
- Disable dependabot (4c6821a)
- Update cliff.toml (7b36a8f)
- Lint justfile (bfb98a1)
- Lint justfile (19e7f39)
- Move to codex tooling (#77) (c772720)
- Add Windows CI tooling (#80) (d6c0652)

### Documentation

- Lint CHANGELOG for markdown errors (623cc9b)
- Lint config.toml (052981b)
- Standardize changelog header format (b4311dc)
- Update logo (c521443)
