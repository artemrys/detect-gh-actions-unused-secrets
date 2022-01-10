detect-gh-actions-unused-secrets
================================

Detects secrets that are defined in the repository and are not used in Github Actions.

What it does:

* Get repository secrets using Github Actions API
* Clone the repository
* Search through the Github Actions related files (`.github/workflows/*.yaml` and `.github/workflows/*.yml`) and try to find usages of each secret
* Report those secrets which are not found

## Prerequisites

* Github token with `repo` scope ([Github docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))

## Example

```console
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python detect_gh_actions_unused_secrets.py <token> <owner>/<repo1> <owner/repo2>
```
