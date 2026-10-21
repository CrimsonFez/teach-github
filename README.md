# Fork to Reveal

**200 lines. One integer. One winner.**

A fixed number from **1 to 100** is hidden behind 200 lines of Python math.
Fork this repository, run the challenge, and be the first person to reveal it.
The first correct result accepted by the verifier wins automatically.

## Play

1. Click **[Fork](https://github.com/hazelfjeld/teach-github/fork)** and create the fork under **your personal GitHub account**.
2. Open the **Actions** tab in **your fork**. If GitHub asks, enable its workflows.
3. Select **Reveal the number** in the left sidebar, then **Run workflow** → **Run workflow** on `main`.
4. Open the new run. When it finishes, its **Summary** shows your number and who won.

No local installation, access-token setup, repository secrets, or paid services are required to participate.
GitHub runs the Python program for you.

**[View the race board](https://teach-github-challenge.airheadhazelnut.chatgpt.site)**

If the race board asks for a ChatGPT sign-in or the workflow cannot reach the verifier, the host has not opened public access yet. Wait for Hazel to start the challenge, then rerun your workflow.

## Rules

- Use a **direct fork** of `hazelfjeld/teach-github`, owned by your personal account.
- Start the workflow while signed in as that fork's owner.
- Everyone receives the **same fixed seed**, so everyone calculates the **same integer**.
- The first verified correct claim received by the server wins. Clicking Fork first or starting a workflow first does not guarantee the win.
- Later players can still complete the challenge and see the result.
- The answer is printed **after** the claim is recorded. Someone watching your public log cannot steal your claim by copying that output.
- Once revealed, the answer can be shared. This is a first-to-finish classroom race.

## What you are learning

| Action | GitHub concept |
| --- | --- |
| Fork this repository | Create your own connected copy of a project |
| Explore `challenge.py` | Read and navigate source code |
| Run a workflow | Execute repeatable jobs with GitHub Actions |
| Read the run summary | Inspect job results and diagnose failures |

## How the lock works

`challenge.py` is exactly **200 nonblank lines** and uses Python's standard library.
Its modular arithmetic, matrix powers, finite-field operations, recurrences, and integer transforms are deterministic.
The essential seed stays on the verifier's server, outside this repository and its history.

When you run the workflow, GitHub supplies a short-lived signed identity token.
The verifier validates that token and asks GitHub whether its repository is a real direct fork of the original.
Only then does it release the seed. The runner computes the number and submits it before printing anything.
One atomic database write chooses the winner.

The workflow uses GitHub's automatically provided, temporary read-only repository token to look up fork metadata.
It sends that token only to the challenge verifier, which uses it only with GitHub's API and never stores or logs it.
You never need to create or paste a personal access token.

## Explore locally

Python **3.8+** is enough for the puzzle and its runner.

```sh
python3 -m unittest discover -s tests -v
```

Running `challenge.py` without the private seed will not reveal the race's number.
You can import `generate_number(seed)` and experiment with your own integer seed; that does not change the fixed race answer.

The hosted verifier's source and deployment notes are in [`verifier/`](verifier/README.md).

## Troubleshooting

| Problem | What to do |
| --- | --- |
| No Run workflow button | Open Actions in **your fork**, enable workflows, and select Reveal the number. |
| Original repository rejected | Fork the repo and run the workflow in the fork. |
| Fork owner required | Use a personal-account fork and start the run as its owner. |
| GitHub or verifier temporarily unavailable | Wait briefly, then use **Re-run all jobs**. Retries cannot replace an existing winner. |
| Answer did not match | Restore `challenge.py` from upstream and run again. |

Official references: [Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo), [Run a workflow manually](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow), [GitHub OIDC](https://docs.github.com/en/actions/reference/security/oidc).
