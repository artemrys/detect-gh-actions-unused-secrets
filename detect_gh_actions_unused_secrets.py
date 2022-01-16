import argparse
import os
import re
import subprocess
import tempfile
from typing import List, Optional, Sequence, Tuple

import requests


def generate_curl(token: str, repo: str, unused_secret: str) -> str:
    _start = 'curl -X DELETE -H "Accept: application/vnd.github.v3+json"'
    _token = f'-H "Authorization: token {token}"'
    _api = f"https://api.github.com/repos/{repo}/actions/secrets/{unused_secret}"
    return " ".join([_start, _token, _api])


def get_secret_names(token: str, repo: str) -> List[str]:
    secret_names = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{repo}/actions/secrets?page={page}",
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"token {token}",
            },
        )
        total_count = response.json()["total_count"]
        for secret in response.json()["secrets"]:
            secret_names.append(secret["name"])
        if len(secret_names) == total_count:
            break
        page += 1
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


def find_secrets_usages(filepaths: List[str], secret: str) -> List[Tuple[str, int]]:
    regex = fr"\${{{{\s*secrets\.{secret}\s*}}}}"
    secret_re = re.compile(regex)
    result = []
    for filepath in filepaths:
        with open(filepath) as f:
            for i, line in enumerate(f.readlines(), 1):
                if secret_re.search(line) is not None:
                    result.append((filepath, i))
    return result


def _strip_tmp_path(path: str, tmp_path: str) -> str:
    return os.path.relpath(path, tmp_path)


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str)
    parser.add_argument("repos", nargs="*")
    parser.add_argument("--generate-curls", action="store_true")
    curls = []
    args = parser.parse_args(argv)
    for repo in args.repos:
        print(repo)
        secret_names = get_secret_names(args.token, repo)
        print(f"\tSecrets {secret_names}")
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
            for github_action_file in github_actions_files:
                relative_path = _strip_tmp_path(github_action_file, tmpdir)
                print(f"\tGithub Actions file {relative_path}")
            if not github_actions_files:
                print("\tThere are no Github Actions files")
            for secret in secret_names:
                secret_used_in_files = find_secrets_usages(github_actions_files, secret)
                if not secret_used_in_files:
                    if args.generate_curls:
                        curls.append(generate_curl(args.token, repo, secret))
                    print(f"\t{secret} is not used anywhere!")
                else:
                    for filepath, line_no in secret_used_in_files:
                        relative_filepath = _strip_tmp_path(filepath, tmpdir)
                        print(
                            f"\t{secret} is used in {relative_filepath}, line {line_no}"
                        )
    if curls:
        with open("curls.sh", "w") as f:
            for curl in curls:
                f.write(curl + "\n")


if __name__ == "__main__":
    main()
