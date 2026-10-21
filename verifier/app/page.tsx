"use client";

import { useCallback, useEffect, useRef, useState } from "react";

const REPO = "https://github.com/hazelfjeld/teach-github";
type Winner = { login: string; repository: string; run_id: string; claimed_at: string };
type Race = { status: "open" | "claimed"; winner: Winner | null; challenge: string };
type IconName = "fork" | "arrow" | "external" | "refresh" | "lock" | "check";

function Icon({ name, className = "" }: { name: IconName; className?: string }) {
  const paths: Record<IconName, React.ReactNode> = {
    fork: <><circle cx="6" cy="5" r="2" /><circle cx="18" cy="5" r="2" /><circle cx="6" cy="19" r="2" /><path d="M6 7v10M18 7v2a4 4 0 0 1-4 4H6" /></>,
    arrow: <path d="M4 12h16M14 6l6 6-6 6" />,
    external: <path d="M7 17 17 7M7 7h10v10" />,
    refresh: <><path d="M20 7v5h-5M4 17v-5h5" /><path d="M6.1 6.1A8 8 0 0 1 19.6 10M4.4 14a8 8 0 0 0 13.5 3.9" /></>,
    lock: <><rect x="5" y="10" width="14" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3" /></>,
    check: <path d="m5 12 4 4L19 6" />,
  };
  return <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>;
}

function isRace(value: unknown): value is Race {
  if (!value || typeof value !== "object") return false;
  const race = value as Partial<Race>;
  if (race.challenge !== "fork-to-reveal-v1") return false;
  if (race.status === "open") return race.winner === null;
  if (race.status !== "claimed" || !race.winner) return false;
  const winner = race.winner;
  return typeof winner.login === "string" && /^[a-z\d](?:[a-z\d-]{0,38})$/i.test(winner.login)
    && typeof winner.repository === "string" && /^[a-z\d-]+\/[a-z\d_.-]+$/i.test(winner.repository)
    && typeof winner.run_id === "string" && /^\d+$/.test(winner.run_id)
    && typeof winner.claimed_at === "string" && Number.isFinite(Date.parse(winner.claimed_at));
}

function runUrl(winner: Winner): string {
  return `https://github.com/${winner.repository.split("/").map(encodeURIComponent).join("/")}/actions/runs/${encodeURIComponent(winner.run_id)}`;
}

export default function Home() {
  const [race, setRace] = useState<Race | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updated, setUpdated] = useState<Date | null>(null);
  const activeRequest = useRef<AbortController | null>(null);
  const refresh = useCallback(async () => {
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    setLoading(true);
    try {
      const response = await fetch("/api/status", { cache: "no-store", credentials: "same-origin", headers: { Accept: "application/json" }, signal: controller.signal });
      if (!response.ok) throw new Error("Status unavailable");
      const data: unknown = await response.json();
      if (!isRace(data)) throw new Error("Invalid race status");
      if (controller.signal.aborted) return;
      setRace(data);
      setUpdated(new Date());
      setError("");
    } catch {
      if (!controller.signal.aborted) setError("Couldn’t refresh the race. Please try again.");
    } finally {
      if (!controller.signal.aborted) setLoading(false);
    }
  }, []);
  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => { if (document.visibilityState === "visible") void refresh(); }, 15_000);
    const onVisible = () => { if (document.visibilityState === "visible") void refresh(); };
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisible);
      activeRequest.current?.abort();
    };
  }, [refresh]);
  const winner = race?.winner ?? null;
  const stateLabel = winner ? "FIRST PLACE CLAIMED" : race ? "THE RACE IS OPEN" : error ? "STATUS UNAVAILABLE" : "CHECKING THE RACE";

  return (
    <div className="site-shell">
      <a href="#main" className="skip-link">Skip to challenge</a>
      <header className="site-header">
        <a href="/" className="wordmark" aria-label="Fork to Reveal home"><span className="brand-icon"><Icon name="fork" /></span>fork<span className="wordmark-join">to</span>reveal<span className="brand-dot">.</span></a>
        <a className="header-link" href={REPO} target="_blank" rel="noreferrer">View on GitHub <Icon name="external" /></a>
      </header>
      <main id="main">
        <section className="hero" aria-labelledby="challenge-title">
          <div className="hero-copy">
            <p className="eyebrow"><span className="tiny-square" /> HAZEL’S GITHUB CHALLENGE <span className="edition">/ 001</span></p>
            <h1 id="challenge-title">Fork it.<br />Find the <span>number.</span></h1>
            <p className="hero-description">One fixed number. Two hundred lines of Python. Fork the repo, run the workflow, and get there first.</p>
            <div className="hero-actions">
              <a className="button primary-button" href={`${REPO}/fork`} target="_blank" rel="noreferrer"><Icon name="fork" /> Fork the repository <Icon name="arrow" /></a>
              <a className="text-link" href="#how-to-play">How to play <span aria-hidden="true">↓</span></a>
            </div>
            <p className="setup-note"><Icon name="check" /> No installs needed. Runs in GitHub Actions.</p>
          </div>
          <div className="number-vault" role="img" aria-label="A secret integer between 1 and 100, revealed by completing the challenge">
            <div className="vault-grid" aria-hidden="true" />
            <div className="vault-heading"><span><Icon name="lock" /> THE SECRET INTEGER</span><span>PY / 200</span></div>
            <div className="vault-range" aria-hidden="true"><span>01</span><span className="range-divider">—</span><span>100</span></div>
            <div className="vault-footer"><span className="vault-code">print(<span>the_answer</span>)</span><span className="hidden-answer">?</span></div>
            <span className="vault-corner corner-one" aria-hidden="true" /><span className="vault-corner corner-two" aria-hidden="true" />
          </div>
        </section>
        <section className={`race-board ${winner ? "race-claimed" : ""}`} aria-labelledby="race-title">
          <div className="race-content" aria-live="polite" aria-atomic="true">
            <p className="eyebrow race-eyebrow"><span className={`status-dot ${!race && loading ? "status-loading" : ""}`} /> {stateLabel}</p>
            <h2 id="race-title">{winner ? <><a href={`https://github.com/${encodeURIComponent(winner.login)}`} target="_blank" rel="noreferrer">@{winner.login}</a> got there first.</> : race ? "Your name could be right here." : error ? "The race board is taking a moment." : "Finding the latest result…"}</h2>
            <p className="race-description">{winner ? <>Verified {new Date(winner.claimed_at).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" })}. You can still complete the challenge.</> : race ? "The first verified correct result takes first place. Your workflow submits it automatically." : "You can open the repository while we check the race status."}</p>
          </div>
          <div className="race-actions">
            {winner && <a className="winner-link" href={runUrl(winner)} target="_blank" rel="noreferrer">View winning run <Icon name="external" /></a>}
            <button type="button" className="refresh-button" onClick={() => void refresh()} disabled={loading} aria-label="Refresh race status"><Icon name="refresh" className={loading ? "spinning" : ""} /> {loading ? "Checking…" : "Refresh"}</button>
            {updated && <span className="last-checked">Checked {updated.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" })}</span>}
          </div>
          {error && <p className="status-error" role="alert">{error}{race ? " The last confirmed result is shown above." : ""}</p>}
        </section>
        <section className="how-section" id="how-to-play" aria-labelledby="how-title">
          <div className="section-heading"><p className="eyebrow">THREE STEPS. ONE ANSWER.</p><h2 id="how-title">Your first fork is the starting line.</h2></div>
          <ol className="steps">
            <li><span className="step-number" aria-hidden="true">01</span><h3>Make it yours.</h3><p>Fork <a href={REPO} target="_blank" rel="noreferrer">hazelfjeld/teach-github</a> into your <strong>personal GitHub account</strong>.</p></li>
            <li><span className="step-number" aria-hidden="true">02</span><h3>Press run.</h3><p>In your fork, open <strong>Actions</strong> and enable workflows if asked. Select <strong>Reveal the number</strong>, then <strong>Run workflow</strong>.</p></li>
            <li><span className="step-number" aria-hidden="true">03</span><h3>Open the result.</h3><p>Your workflow calculates and submits the answer. Open the finished run’s <strong>summary</strong> to see your integer and result.</p></li>
          </ol>
        </section>
        <aside className="rules" aria-labelledby="rules-title">
          <div><p className="eyebrow" id="rules-title">A FEW GROUND RULES</p><p>Simple enough to play.<br />Interesting enough to inspect.</p></div>
          <ul><li><Icon name="check" /> Fork the original repo directly into your personal account.</li><li><Icon name="check" /> Everyone gets the same fixed number between 1 and 100.</li><li><Icon name="check" /> The first verified correct submission wins.</li><li><Icon name="check" /> The code is yours to explore. Later finishers still get the answer.</li></ul>
        </aside>
      </main>
      <footer className="site-footer"><span>A little challenge from <a href="https://github.com/hazelfjeld" target="_blank" rel="noreferrer">Hazel</a>.</span><span>200 LINES <span aria-hidden="true">·</span> PYTHON <span aria-hidden="true">·</span> ONE INTEGER</span></footer>
    </div>
  );
}
