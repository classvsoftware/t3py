# USAGE.md

## Development

`pip-compile requirements.in`
`pip-compile dev_requirements.in`

`mypy t3py/**/*.py --check-untyped-defs`

## Versioning

`git tag -a v1.0.0 -m "Release version 1.0.0"`
`git push origin v1.0.0`

## Deployment

Reinstall the package locally to test:
`pip install -e .`

Test the command:
`t3py`


## Build

This generates the dist/ directory containing .tar.gz and .whl files.

`python -m build`

This uploads the dist/ package to pypi

`twine upload dist/*`