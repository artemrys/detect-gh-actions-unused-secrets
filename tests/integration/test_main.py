import os

from detect_gh_actions_unused_secrets import main


def test_main(capsys):
    expected_output = """artemrys/test-repo
\tSecrets ['UNUSED_SECRET_1', 'UNUSED_SECRET_2', 'USED_SECRET_KEY']
\tGithub Actions file .github/workflows/main.yml
\tUNUSED_SECRET_1 is not used anywhere!
\tUNUSED_SECRET_2 is not used anywhere!
\tUSED_SECRET_KEY is used in .github/workflows/main.yml, line 14
"""
    main(
        (
            os.getenv("GH_TOKEN_INTEGRATION_TEST"),
            "artemrys/test-repo",
        )
    )
    captured = capsys.readouterr()
    assert expected_output == captured.out
