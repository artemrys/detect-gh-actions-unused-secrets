import os

from detect_gh_actions_unused_secrets import main


def test_main(capsys):
    expected_output = """artemrys/detect-gh-actions-unused-secrets-demo
\tSecrets ['UNUSED_SECRET_1', 'UNUSED_SECRET_2', 'USED_SECRET_KEY']
\tGitHub Actions file .github/workflows/main.yaml
\tUNUSED_SECRET_1 is not used anywhere!
\tUNUSED_SECRET_2 is not used anywhere!
\tUSED_SECRET_KEY is used in .github/workflows/main.yaml, line 18
"""
    main(
        (
            os.getenv("GH_TOKEN_INTEGRATION_TEST"),
            "artemrys/detect-gh-actions-unused-secrets-demo",
        )
    )
    captured = capsys.readouterr()
    assert expected_output == captured.out
