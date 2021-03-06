# Contributing to Yadism

If you are not a member of development team pleas look below for [external
contributions guidelines](.github/contributing.md#external-contributions)

## Internal development

### Installation

#### Test Dependencies

Currently this package has two non-python test dependencies:

- `lhapdf`, provides PDF sets, only required for benchmarks
- `apfel`, only required for benchmarks

For `apfel` and `lhapdf` you should get them following the instructions on their
respective official distribution sources.
Than make sure to make them available in your python (virtual)environment.

Install the other dependencies using:

```
pip install -r test_requirements.txt --ignore-installed
```

#### Docs dependencies

Install the dependencies using:

```
pip install -r doc_requirements.txt --ignore-installed
```

### Unit Tests

To run test install the package and run `pytest tests` in the project root
(configurations are in `setup.cfg`).

<!--TODO further descriptions should be moved to the wiki, in order to have a
unique place to reference for development and to keep this document as short as
possible-->

#### Markers

Show known marks with `pytest --markers` and run them with:

- quick check: `pytest -m quick_check`
- commit check: `pytest -m "quick_check or commit_check"`
- full check: `pytest`

#### Test coverage

Use `pytest ... --cov=src` to obtain a report for test coverage.

### Benchmarks and regression tests

Since there is a non-trivial framework to manage these tasks you should look
into the specific
[documentation](https://n3pdf.github.io/yadism/dev-tools/db-suite.html).

The main idea is to generate the input databases customizing and running
provided scripts, and then select with suitable queries the combinations of
input you are interested in, and running the benchmark utility passing the
queries as arguments.

### Release based workflow

Since it is appropriate to develop this code in versions (as in the way
suggested by [SemVer](https://semver.org/)) we decided to base our workflow on
the popular [git flow model](https://nvie.com/posts/a-successful-git-branching-model/).

In order to help you with the management consider using [`git flow`](https://github.com/petervanderdoes/gitflow-avh) CLI tool (and the
corresponding [shell
completion](https://github.com/petervanderdoes/git-flow-completion)), or the
original version of [`git flow`](https://github.com/nvie/gitflow).

## External contributions

Currently the main guideline we would like to highlight is to use [GitHub
issues](https://github.com/N3PDF/yadism/issues) for requests, bugs reporting,
and any other communication, and [GitHub pull
requests](https://github.com/N3PDF/yadism/pulls) for code contributions.

External pull requests should be applied to the latest release branch, if not
available choose simply `master` as base, and it will be moved to a suitable one
by maintainers.

Please take the time to fulfill the proper template (it will be automatically provided).
