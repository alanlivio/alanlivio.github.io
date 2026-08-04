import os
import json
import unittest
from unittest.mock import patch, MagicMock
import macros

class TestMacros(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_fetch_repo_stats_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "stargazers_count": 42,
            "forks_count": 7
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        stats = macros.fetch_repo_stats("alanlivio/alanlivio.github.io")
        self.assertIsNotNone(stats)
        self.assertEqual(stats["stars"], 42)
        self.assertEqual(stats["forks"], 7)

    @patch("urllib.request.urlopen")
    def test_fetch_repo_stats_failure(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection error")
        stats = macros.fetch_repo_stats("invalid/repo")
        self.assertIsNone(stats)

    def test_define_env_with_mock_cache(self):
        class DummyEnv:
            def __init__(self):
                self.variables = {}

        env = DummyEnv()
        macros.define_env(env)
        self.assertIn("github_total_repos", env.variables)
        self.assertIn("github_total_stars", env.variables)
        self.assertIn("github_total_forks", env.variables)
        self.assertGreaterEqual(env.variables["github_total_repos"], 0)

if __name__ == "__main__":
    unittest.main()
