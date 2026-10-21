# Fork to Reveal — verifier

The server for [hazelfjeld/teach-github](https://github.com/hazelfjeld/teach-github).
The hosted race board is at <https://teach-github-challenge.airheadhazelnut.chatgpt.site>.

## Routes

| Route | Purpose | Authentication |
| --- | --- | --- |
| `GET /` | Participant instructions and live winner board | Public when the host opens the race |
| `GET /api/status` | Winner metadata only; never the seed or answer | Same as the board |
| `POST /api/unlock` | Return the fixed private seed | Valid GitHub Actions OIDC token from an eligible fork |
| `POST /api/claim` | Check an integer and atomically register the first winner | The same fork verification |

The race counts the first correct claim received by the server, not workflow start time.
The runner waits for the claim response before printing the answer or writing its summary.
Later correct claims cannot replace the winner, and retrying the winning account's claim is idempotent.

## Identity checks

`lib/github-identity.ts` verifies GitHub's RS256 signature against its fixed JWKS endpoint.
It checks issuer, exact audience, expiry, activation/issue times, manual workflow trigger,
GitHub-hosted runner, numeric repository/owner/actor/run IDs, and the actor's ownership.
GitHub's repository API must then confirm a public personal-account fork whose direct
parent ID is `1428727319` (the original repository).

The originating repository is rejected. A same-named unrelated repository is rejected.
Changing the public client cannot make an unsigned or unrelated identity pass verification.
The optional read-only `GITHUB_TOKEN` is used only for GitHub's metadata lookup, never stored or logged.
JWTs and response sizes are bounded; requests use timeouts and do not follow redirects.

The public copy contains no production secret and no production Site identity.
Possessing this source is not permission to use an existing deployment's private values.

## Runtime configuration

Set these once as **secret** runtime environment values in the host's configuration:

| Name | Value |
| --- | --- |
| `CHALLENGE_SEED` | Exactly 16 hexadecimal characters, generated once for the race |
| `CHALLENGE_ANSWER` | The decimal integer returned by `generate_number(int(seed, 16))` |

Both values are already configured on Hazel's deployment. They are intentionally absent from this repository.
Do not put them in workflow YAML, client bundles, build logs, `.openai/hosting.json`, or tracked environment files.
Changing either value during a race would invalidate its fixed-answer contract.

Persistence uses the D1 binding `DB`. The `winners.challenge` primary key enforces one winner.
`lib/race.ts` inserts and selects in one transactional batch. Schema and migration are in `db/` and `drizzle/`.
The app does not provide a public reset or administration endpoint.

## Local verification

Use **Node 24** for the dependency-free security and race tests:

```sh
node tests/identity.test.mjs
node tests/race.test.mjs
```

The identity suite signs test tokens with temporary test keys and mocks GitHub responses.
The race suite sends 12 concurrent claims through SQLite using the actual production SQL.
These tests do not contact the live challenge, disclose its seed, or create a winner.

To install and check the web application:

```sh
npm ci
npx tsc --noEmit
npm run build
```

This project uses the Sites Vinext starter and its `sites()` build integration.
Use the Sites workflow to register a new deployment, configure its identity and secret values,
apply migrations, and publish it. The public `.openai/hosting.json` declares only logical
bindings; the deployment's own checkout contains its Site ID. If deploying another instance,
update `AUDIENCE` in `lib/http.ts` and `CHALLENGE_URL` in the reveal workflow to that instance's exact HTTPS origin.

The verifier must be publicly reachable for GitHub-hosted runners to reach it.
Owner-private access is appropriate for review, but it blocks participants until the owner opens the race.

## Verification limits

A complete live fork run needs a different GitHub account with its own direct fork.
The original repository's owner cannot qualify by running the upstream workflow.
Do not add a production bypass merely to make an upstream test pass.

Official references: [GitHub OIDC](https://docs.github.com/en/actions/reference/security/oidc),
[repository metadata](https://docs.github.com/en/rest/repos/repos#get-a-repository),
[D1 batch API](https://developers.cloudflare.com/d1/worker-api/d1-database/#batch).
