# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

### Changed

### Removed

## [1.2.0]

### Added
- Add the ability to make test groups based on file names with `--test-group-by filename` (#20)

### Changed

- When tests are sorted randomly, they are now still run in the original order (#12)
- Use hookwrapper to ensure that grouping occurs after other filtering has been applied to items (#8)

## [1.1.1]

### Added
- Releases now signed with sigstore