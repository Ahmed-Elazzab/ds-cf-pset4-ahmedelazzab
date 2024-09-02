# pset4_AhmedElazzab

This bundle is for Dsdev pset4.

Generated using [this build](https://github.com/procter-gamble/de-cf-python-pod/tree/09403bf3fc25b5851af956ced653a995778bc3b2)
 of de-cf-python-pod.

[![python](https://img.shields.io/badge/Python-3.9-3776AB?logo=Python&logoColor=white)](https://python.org/)
[![P&G Continuous Winning (Continuous Integration) DEV](https://github.com/pg-ds-dev-class/ds-cf-pset3-ahmed-elazzab/actions/workflows/cw.yml/badge.svg)](https://github.com/pg-ds-dev-class/ds-cf-pset4-ahmedelazzab/actions/workflows/cw.yml)
[![sonarqube](https://img.shields.io/badge/SonarQube-ds--cf--pset4--ahmedelazzab-4E9BCD?logo=SonarQube&labelColor=303030)](https://sonarqubeenterprise.pgcloud.com/sonarqube/dashboard?id=ds-cf-pset4-ahmedelazzab)
[![confluence](https://img.shields.io/badge/Confluence-none-172B4D?logo=Confluence)](https://jira-pg-ds.atlassian.net/wiki/spaces/none)
[![python-pod](https://img.shields.io/badge/created%20with-python--pod-AF1685)](https://github.com/procter-gamble/de-cf-python-pod)

## Quickstart

### For Developers

You need to create a Python virtual environment for this project. We recommend you install and use
[Miniforge](https://github.com/conda-forge/miniforge). Once installed, create the environment:

```sh
conda create -y --name=pset4-ahmedelazzab python=3.9
```

activate it:

```sh
conda activate pset4-ahmedelazzab
```

upgrade your pip installation:

```sh
pip install --upgrade pip
```

Finally, install the project in "development mode" (note, you must be in the project's toplevel directory
for issuing this command):

```sh
pip install -e ".[devel]"
```

The command above works on Windows, macOS and Linux.

#### Running tests

Decorate long-running tests with `pytest.mark.slow` so they will be excluded from the default run.
To run tests execute:

```sh
./test/run_pytest_cov.py
```

Add `--include-slow` flag to the command when it's necessary to run both long- and short-running tests.

CI/CD pipeline will also filter out decorated long-running tests. If necessary add a label
`include-slow` to your pull request in GitHub. Adding a label will trigger the pipeline with all the
tests.

#### Generating the documentation

The documentation can be generated with [MkDocs](https://www.mkdocs.org) based on docstrings and
static content provided by developers. `flake8` rules enforce presence of docstrings in relevant
places, but it's your responsibility to fill them with valuable content.

To generate documentation page, go to
`ds-cf-pset4-ahmedelazzab/docs/`
subdirectory and execute:

```bash
mkdocs build
```

The fresh version of documentation will be generated in
`ds-cf-pset4-ahmedelazzab/docs/site/`.
Open `ds-cf-pset4-ahmedelazzab/docs/site/index.html` with your browser to view it.

> **Note:** More information about MkDocs configuration and documentation structure in [MkDocs introduction](docs/docs/index.md).
You can also check [MkDocs official documentation](https://www.mkdocs.org/) and how
[MkDocs is being used in dnalib.](https://github.com/procter-gamble/de-cf-dnalib/blob/master/CONTRIBUTING.md#documentation)

#### Linting Markdown files

To make sure that our Markdown files are formatted correctly we apply Markdown linter to the CI
pipeline. The configuration file `.markdownlint.yml` is located in `/.github/workflows/config/` and
it's used by CI step and local linter.

The process of how to use Markdown linter locally is described in
[Python Pod documentation for contributors][1] and done similarly.

[1]: https://github.com/procter-gamble/de-cf-python-pod/blob/09403bf3fc25b5851af956ced653a995778bc3b2/CONTRIBUTING.md#linting-markdown-files

## PyrogAI

Please read [PyrogAI Documentation](https://not-exists-yet).

### CICD setup

To be able to use our asynchronous CD, you need to copy your
[GitHub personal access token](https://jira-pg-ds.atlassian.net/wiki/spaces/CR/pages/189005860/Setup+GitHub+link+GCP)
to github repository secrets and name it `USER_GITHUB_TOKEN`.

### Setup to run from CLI

To be able to run pipelines on remote environments from your local PC using CLI,
certain secrets needs to be provided.

Use below command to populate gh_token with your
[GitHub personal access token](https://jira-pg-ds.atlassian.net/wiki/spaces/CR/pages/189005860/Setup+GitHub+link+GCP)

```commandline
aif secret add --secret gh_token --value <YOUR USER_GITHUB_TOKEN HERE>
```

#### Databricks specific setup

Databricks requires DBR_TOKEN to be added to secrets.json to be able to communicate with Databricks Workspace.

Create access token following
[Databricks official docs](https://docs.databricks.com/en/dev-tools/auth.html#databricks-personal-access-tokens-for-users)
and past it to below command

```commandline
aif secret add --secret dbr_token --value <YOUR DBR TOKEN HERE>
```

#### AzureMl specific setup

CLI runs for AzureML requires authentication into Azure account, by default if user is not
authenticated - it will be prompted to do so.
For system-wide authentication, you may run command `az login` although it is optional.

#### Vertex specific setup

Vertex and CF does not require any additional setup.

### Downloading opinionated pipelines

In order to download `ml_iris` opinionated pipeline run pyrogAI command

```shell
aif pipeline from-template --pipe-name ml_iris
```

To see more options on how to download opinionated pipeline run command

```shell
aif pipeline from-template --help
```

Remember that you won't be able to execute `aif pipeline run` command without
any pipeline saved in pset4_ahmedelazzab.data.

### Running pipelines

In order to run pipeline on defined provider run command

```shell
aif pipeline run
```

Keep in mind that depending on the provider you need several environment variables defined.
Unfortunately we didn't create any list of all needed variables yet.

### More options

For more options on how to use pyrogai library run commands

```shell
aif pipeline --help
aif steps --help
```

### Staging and Production environments

To create Staging and Production environments go to:
[Environment settings](https://github.com/procter-gamble/ds-cf-pset4-ahmedelazzab/settings/environments).

To enable a protection rule that grants permission to specific users
or teams for approving workflow runs on Staging or Production environemnt you have to:

1. Navigate to the "Configure Production" section.
2. Locate the "Deployment Protection Rules - Required Reviewers" option.
3. Select the desired users or teams from the available options.

When executing GitHub actions in the Staging or Production environment,
at least one of the selected reviewers will be required to provide approval.
