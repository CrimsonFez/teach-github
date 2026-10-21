import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from scripts import play


ORIGIN = "https://teach-github-challenge.airheadhazelnut.chatgpt.site"
WINNER = {"login": "learner", "repository": "learner/teach-github",
          "run_id": "1234567", "claimed_at": "2026-10-21T18:00:00.000Z"}


class PlayTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.summary = Path(self.directory.name) / "summary.md"
        self.env = {
            "GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "workflow_dispatch",
            "GITHUB_REPOSITORY": "learner/teach-github", "CHALLENGE_URL": ORIGIN,
            "GITHUB_TOKEN": "github-secret", "GITHUB_STEP_SUMMARY": str(self.summary),
            "ACTIONS_ID_TOKEN_REQUEST_URL": "https://github.test/token?api-version=2",
            "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "request-secret",
        }
        self.claim = {"won": True, "winner": WINNER, "answer": 61}

    def invoke(self, replies, environment=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.dict(os.environ, self.env if environment is None else environment, clear=True), \
                patch.object(play, "request_json", side_effect=replies) as request, \
                patch.object(play, "generate_number", return_value=61) as calculate, \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = play.main()
        return status, stdout.getvalue(), stderr.getvalue(), request, calculate

    def test_success_claims_before_revealing_and_sets_audience(self):
        def reply(url, bearer, body=None):
            self.assertFalse(self.summary.exists())
            if url.startswith("https://github.test/"):
                self.assertEqual(parse_qs(urlsplit(url).query)["audience"], [ORIGIN])
                self.assertEqual(bearer, "request-secret")
                return {"value": "oidc-secret"}
            self.assertEqual(bearer, "oidc-secret")
            self.assertEqual(body["github_token"], "github-secret")
            if url.endswith("/api/unlock"):
                return {"seed": "cafebabe"}
            self.assertEqual(url, ORIGIN + "/api/claim")
            self.assertEqual(body["answer"], 61)
            return self.claim

        status, stdout, stderr, request, calculate = self.invoke(reply)
        self.assertEqual((status, stdout, stderr), (0, "61\n", ""))
        self.assertEqual(request.call_count, 3)
        calculate.assert_called_once_with(int("cafebabe", 16))
        summary = self.summary.read_text()
        self.assertIn("first verified claimant", summary)
        self.assertIn("learner/teach-github/actions/runs/1234567", summary)
        for secret in ("cafebabe", "oidc-secret", "github-secret", "request-secret"):
            self.assertNotIn(secret, stdout + stderr + summary)

    def test_claim_failure_does_not_print_answer_or_write_summary(self):
        replies = [{"value": "oidc-secret"}, {"seed": "cafebabe"}, play.PlayError("Claim rejected.")]
        status, stdout, stderr, _, _ = self.invoke(replies)
        self.assertEqual(status, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Claim rejected", stderr)
        self.assertFalse(self.summary.exists())
        for secret in ("cafebabe", "oidc-secret", "github-secret", "61"):
            self.assertNotIn(secret, stderr)

    def test_missing_workflow_environment_fails_without_network(self):
        for missing in self.env:
            with self.subTest(missing=missing):
                environment = {key: value for key, value in self.env.items() if key != missing}
                status, stdout, _, request, _ = self.invoke([], environment)
                self.assertEqual((status, stdout), (1, ""))
                request.assert_not_called()

    def test_upstream_is_rejected_without_network(self):
        environment = dict(self.env, GITHUB_REPOSITORY=play.UPSTREAM)
        status, stdout, stderr, request, _ = self.invoke([], environment)
        self.assertEqual((status, stdout), (1, ""))
        self.assertIn("Fork this repository first", stderr)
        request.assert_not_called()

    def test_existing_winner_still_reveals_after_a_valid_claim(self):
        claim = dict(self.claim, won=False)
        result = self.invoke([{"value": "oidc-secret"}, {"seed": "cafebabe"}, claim])
        self.assertEqual(result[:3], (0, "61\n", ""))
        self.assertIn("winner was already recorded", self.summary.read_text())

    def test_invalid_seed_stops_before_calculation_and_claim(self):
        result = self.invoke([{"value": "oidc-secret"}, {"seed": "not-hex"}])
        self.assertEqual(result[:2], (1, ""))
        self.assertEqual(result[3].call_count, 2)
        result[4].assert_not_called()

    def test_unconfirmed_or_wrong_claim_never_reveals(self):
        for claim in ({"error": "private response"}, dict(self.claim, answer=True),
                      dict(self.claim, answer=62), dict(self.claim, won="true")):
            with self.subTest(claim=claim):
                result = self.invoke([{"value": "oidc-secret"}, {"seed": "cafebabe"}, claim])
                self.assertEqual(result[:2], (1, ""))
                self.assertFalse(self.summary.exists())


class HttpTests(unittest.TestCase):
    @staticmethod
    def response(body):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps(body).encode()
        return response

    def test_transient_http_failures_retry_at_most_three_identical_requests(self):
        failures = [HTTPError(ORIGIN, 503, "private", None, io.BytesIO(b"secret")) for _ in range(3)]
        with patch.object(play.OPENER, "open", side_effect=failures) as request, \
                patch.object(play.time, "sleep") as sleep:
            with self.assertRaisesRegex(play.PlayError, "HTTP 503") as error:
                play.request_json(ORIGIN + "/api/claim", "token-secret", {"answer": 61})
        self.assertEqual(request.call_count, 3)
        self.assertEqual(sleep.call_args_list, [call(1), call(2)])
        self.assertIs(request.call_args_list[0].args[0], request.call_args_list[2].args[0])
        self.assertNotIn("secret", str(error.exception))

    def test_transient_http_failure_can_recover(self):
        failure = HTTPError(ORIGIN, 429, "private", None, io.BytesIO(b"secret"))
        with patch.object(play.OPENER, "open", side_effect=[failure, self.response({"ok": True})]), \
                patch.object(play.time, "sleep") as sleep:
            self.assertEqual(play.request_json(ORIGIN, "token-secret"), {"ok": True})
        sleep.assert_called_once_with(1)

    def test_other_http_and_network_errors_do_not_retry_or_expose_details(self):
        errors = [HTTPError(ORIGIN, 403, "token-secret", None, io.BytesIO(b"seed-secret")),
                  URLError("token-secret")]
        for failure in errors:
            with self.subTest(kind=type(failure)), \
                    patch.object(play.OPENER, "open", side_effect=failure) as request, \
                    patch.object(play.time, "sleep") as sleep:
                with self.assertRaises(play.PlayError) as error:
                    play.request_json(ORIGIN, "token-secret")
                request.assert_called_once()
                sleep.assert_not_called()
                self.assertNotIn("secret", str(error.exception))

    def test_redirects_cannot_forward_credentials(self):
        handler = play.NoRedirect()
        self.assertIsNone(handler.redirect_request(None, None, 302, "", {}, "https://other.test"))


if __name__ == "__main__":
    unittest.main()
