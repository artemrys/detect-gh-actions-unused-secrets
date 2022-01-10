import argparse
import os
import re
import subprocess
import tempfile
from typing import List

import requests


def get_secret_names(token: str, repo: str) -> List[str]:
    response = requests.get(
        f"https://api.github.com/repos/{repo}/actions/secrets",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        },
    )
    secret_names = []
    for secret in response.json()["secrets"]:
        secret_names.append(secret["name"])
    return secret_names


def get_github_actions_files(repo_path: str) -> List[str]:
    github_actions_files_path = f"{repo_path}/.github/workflows"
    if not os.path.exists(github_actions_files_path):
        return []
    result = []
    for filename in os.listdir(github_actions_files_path):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            result.append(f"{github_actions_files_path}/{filename}")
    return result


def find_secrets_usages(filepaths: str, secret: str) -> List[str]:
    regex = fr"\${{{{\s*secrets\.{secret}\s*}}}}"
    secret_re = re.compile(regex)
    result = []
    for filepath in filepaths:
        with open(filepath) as f:
            content = f.read()
            if secret_re.search(content) is not None:
                result.append(filepath)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str)
    parser.add_argument("repos", nargs="*")
    args = parser.parse_args()
    for repo in args.repos:
        print(f"Processing {repo}")
        secret_names = get_secret_names(args.token, repo)
        print(f"\t{repo} has secrets {secret_names}")
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.call(
                (
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    f"https://{args.token}@github.com/{repo}",
                    tmpdir,
                ),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            github_actions_files = get_github_actions_files(tmpdir)
            print(f"\t{repo} has Github actions files {github_actions_files}")
            for secret in secret_names:
                secret_used_in_files = find_secrets_usages(github_actions_files, secret)
                if not secret_used_in_files:
                    print(f"\t{secret} is not used anywhere!")
                else:
                    print(f"\t{secret} is used in {secret_used_in_files}")


if __name__ == "__main__":
    main()
