"""Unlock, calculate, and claim the number from a manually started fork workflow."""

import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from challenge import generate_number

UPSTREAM = "hazelfjeld/teach-github"
RETRYABLE = {429, 502, 503, 504}
MAX_RESPONSE_BYTES = 65_536


class PlayError(Exception):
    """A safe, human-readable error that contains no credentials or seed."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        return None


OPENER = build_opener(NoRedirect())


def request_json(url, bearer, body=None):
    """Retry only explicit transient HTTP failures; never expose response bodies."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": "Bearer " + bearer, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers)
    for attempt in range(3):
        try:
            with OPENER.open(request, timeout=15) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise PlayError("The server returned an oversized response.")
            result = json.loads(raw)
            if not isinstance(result, dict):
                raise PlayError("The server returned an unexpected response.")
            return result
        except HTTPError as error:
            status = error.code
            error.close()
            if status in RETRYABLE and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise PlayError(f"Request rejected (HTTP {status}). Check the fork and rerun.") from None
        except (URLError, OSError, TimeoutError):
            raise PlayError("The service could not be reached. Please rerun the workflow.") from None
        except (ValueError, UnicodeError):
            raise PlayError("The server returned unreadable data. Please rerun the workflow.") from None


def configuration():
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise PlayError("Run Actions > Reveal the number in your GitHub fork.")
    if os.environ.get("GITHUB_REPOSITORY", "").lower() == UPSTREAM:
        raise PlayError("Fork this repository first, then run its Reveal the number workflow.")
    if os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch":
        raise PlayError("Start the workflow manually with the Run workflow button.")
    names = (
        "CHALLENGE_URL", "GITHUB_TOKEN", "GITHUB_REPOSITORY", "GITHUB_STEP_SUMMARY",
        "ACTIONS_ID_TOKEN_REQUEST_URL", "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
    )
    if any(not os.environ.get(name) for name in names):
        raise PlayError("Workflow settings are missing. Use the supplied reveal workflow.")
    config = {name: os.environ[name] for name in names}
    origin = config["CHALLENGE_URL"].rstrip("/")
    parsed = urlsplit(origin)
    if (parsed.scheme != "https" or not parsed.netloc or parsed.path
            or parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise PlayError("CHALLENGE_URL must be the HTTPS address of the verifier.")
    config["CHALLENGE_URL"] = origin
    return config


def identity_token(config):
    parsed = urlsplit(config["ACTIONS_ID_TOKEN_REQUEST_URL"])
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise PlayError("GitHub did not provide a valid identity endpoint.")
    query = [(key, value) for key, value in parse_qsl(parsed.query) if key != "audience"]
    query.append(("audience", config["CHALLENGE_URL"]))
    url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), ""))
    result = request_json(url, config["ACTIONS_ID_TOKEN_REQUEST_TOKEN"])
    token = result.get("value")
    if not isinstance(token, str) or not token:
        raise PlayError("GitHub did not issue an identity token.")
    return token


def claim_summary(claim, answer):
    if type(claim.get("won")) is not bool or type(claim.get("answer")) is not int:
        raise PlayError("The claim was not confirmed. Rerun the workflow.")
    if claim["answer"] != answer or not 1 <= answer <= 100:
        raise PlayError("The server did not confirm the calculated answer.")
    winner = claim.get("winner")
    if not isinstance(winner, dict):
        raise PlayError("The server did not confirm a winner.")
    login, repository = winner.get("login"), winner.get("repository")
    run_id, claimed_at = str(winner.get("run_id", "")), winner.get("claimed_at")
    if (not isinstance(login, str) or not re.fullmatch(r"[A-Za-z0-9-]+", login)
            or not isinstance(repository, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
            or not run_id.isdecimal() or not isinstance(claimed_at, str)
            or not re.fullmatch(r"[0-9T:.+Z -]+", claimed_at)):
        raise PlayError("The server returned incomplete winner details.")
    status = "You are the first verified claimant!" if claim["won"] else "A winner was already recorded."
    return (
        "# GitHub fork challenge\n\n"
        f"**The number is {answer}.**\n\n{status}\n\n"
        f"- Winner: [{login}](https://github.com/{login})\n"
        f"- Fork: [{repository}](https://github.com/{repository})\n"
        f"- Winning run: [{run_id}](https://github.com/{repository}/actions/runs/{run_id})\n"
        f"- First claim: {claimed_at}\n"
    )


def play():
    config = configuration()
    token = identity_token(config)
    origin, github_token = config["CHALLENGE_URL"], config["GITHUB_TOKEN"]
    unlocked = request_json(origin + "/api/unlock", token, {"github_token": github_token})
    seed = unlocked.get("seed")
    if not isinstance(seed, str) or not re.fullmatch(r"[0-9a-fA-F]{1,64}", seed):
        raise PlayError("The server did not unlock the challenge for this fork.")
    answer = generate_number(int(seed, 16))
    claim = request_json(origin + "/api/claim", token, {"github_token": github_token, "answer": answer})
    summary = claim_summary(claim, answer)
    try:
        with open(config["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write(summary)
    except OSError:
        raise PlayError("Claim saved, but the summary could not be written. Rerun the workflow.") from None
    print(answer)


def main():
    try:
        play()
    except PlayError as error:
        print(f"Challenge not revealed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
