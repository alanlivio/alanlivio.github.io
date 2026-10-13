import json
from unittest.mock import patch, MagicMock
import macros


@patch("urllib.request.urlopen")
def test_fetch_repo_stats_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "stargazers_count": 42,
        "forks_count": 7,
        "description": "A sample description"
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    stats = macros.fetch_repo_stats("alanlivio/alanlivio.github.io")
    assert stats is not None
    assert stats["stars"] == 42
    assert stats["forks"] == 7
    assert stats["description"] == "A sample description"


@patch("urllib.request.urlopen")
def test_fetch_repo_stats_failure(mock_urlopen):
    mock_urlopen.side_effect = Exception("Connection error")
    stats = macros.fetch_repo_stats("invalid/repo")
    assert stats is None


def test_define_env_with_mock_cache():
    class DummyEnv:
        def __init__(self):
            self.variables = {}

    env = DummyEnv()
    macros.define_env(env)
    assert "github_total_repos" in env.variables
    assert "github_total_stars" in env.variables
    assert "github_total_forks" in env.variables
    assert env.variables["github_total_repos"] >= 0


def test_define_env_updates_opensource_page_meta():
    class DummyPage:
        def __init__(self):
            self.meta = {
                "template": "opensource.html",
                "sections": [
                    {
                        "title": "Academic Tools",
                        "repositories": [
                            {"name": "alanlivio/autograder-gen", "title": "autograder-gen"}
                        ]
                    }
                ]
            }

    class DummyEnv:
        def __init__(self):
            self.variables = {}

    env = DummyEnv()
    page = DummyPage()
    macros.define_env(env)
    repo = page.meta["sections"][0]["repositories"][0]
    assert "stars" in repo
    assert "forks" in repo
    assert "description" in repo
