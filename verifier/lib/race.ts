export const CHALLENGE = "fork-to-reveal-v1";

export type Identity = {
  repositoryId: string;
  ownerId: string;
  login: string;
  repository: string;
  runId: string;
};

export type WinnerRow = {
  challenge: string;
  login: string;
  repository: string;
  repository_id: string;
  owner_id: string;
  run_id: string;
  claimed_at: string;
};

export const INSERT_WINNER = `INSERT INTO winners
  (challenge, login, repository, repository_id, owner_id, run_id, claimed_at)
  VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(challenge) DO NOTHING`;
export const SELECT_WINNER = "SELECT * FROM winners WHERE challenge = ?";

export function publicWinner(row: WinnerRow) {
  return {
    login: row.login,
    repository: row.repository,
    run_id: row.run_id,
    claimed_at: row.claimed_at,
  };
}

export function validAnswer(answer: unknown, expected: number): answer is number {
  return typeof answer === "number" && Number.isInteger(answer)
    && answer >= 1 && answer <= 100 && answer === expected;
}

export async function recordClaim(db: D1Database, identity: Identity) {
  const parameters = [CHALLENGE, identity.login, identity.repository,
    identity.repositoryId, identity.ownerId, identity.runId,
    new Date().toISOString()];
  // One transactional batch makes competing requests choose exactly one row.
  const results = await db.batch<WinnerRow>([
    db.prepare(INSERT_WINNER).bind(...parameters),
    db.prepare(SELECT_WINNER).bind(CHALLENGE),
  ]);
  const winner = results[1]?.results?.[0];
  if (!winner) throw new Error("Winner registration did not complete.");
  return {
    won: winner.owner_id === identity.ownerId
      && winner.repository_id === identity.repositoryId,
    winner: publicWinner(winner),
  };
}
