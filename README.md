detect-gh-actions-unused-secrets
================================

Detects secrets that are defined in the repository and are not used in GitHub Actions.

What it does:

* Get repository secrets using GitHub Actions API
* Clone the repository
* Search through the GitHub Actions related files (`.github/workflows/*.yaml` and `.github/workflows/*.yml`) and try to find usages of each secret
* Report those secrets which are not found

## Prerequisites

* GitHub token with `repo` scope ([GitHub docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))

## Installation

```console
pip install detect-gh-actions-unused-secrets
```

## Usage

```console
detect-gh-actions-unused-secrets <token> <owner>/<repo1> <owner/repo2>
```

### `--generate-curls`

Option to generate a text file with `curl`s to delete all unused secrets in the repositories that were scanned.

```console
detect-gh-actions-unused-secrets <token> <owner>/<repo1> --generate-curls
```

This command will produce a file called `curls.sh` that will contain line-by-line `curl` commands to delete all unused secrets in `<owner>/<repo1>` repository. [This](https://docs.github.com/en/rest/reference/actions#delete-a-repository-secret) endpoint will be utilized.
