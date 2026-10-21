import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import { CHALLENGE, recordClaim, validAnswer } from '../lib/race.ts';

function adapter(database) {
  return {
    prepare(sql) { return { sql, bind(...values) { return { sql, values }; } }; },
    async batch(statements) {
      database.exec('BEGIN IMMEDIATE');
      try {
        const results = statements.map(({ sql, values }) => ({
          success: true, results: database.prepare(sql).all(...values),
        }));
        database.exec('COMMIT');
        return results;
      } catch (error) { database.exec('ROLLBACK'); throw error; }
    },
  };
}

function identity(id) {
  return { repositoryId: String(9000 + id), ownerId: String(id),
    login: `student-${id}`, repository: `student-${id}/teach-github`, runId: String(7000 + id) };
}

if (!isMainThread) {
  const database = new DatabaseSync(workerData.path);
  database.exec('PRAGMA busy_timeout = 10000');
  parentPort.once('message', async () => {
    try { parentPort.postMessage(await recordClaim(adapter(database), identity(workerData.id))); }
    catch (error) { parentPort.postMessage({ error: error.message }); }
    finally { database.close(); }
  });
  parentPort.postMessage('ready');
} else {
  test('accepts only an exact integer in range matching the fixed answer', () => {
    assert.equal(validAnswer(42, 42), true);
    for (const value of ['42', true, null, 42.5, 0, 101, NaN, Infinity, 41]) {
      assert.equal(validAnswer(value, 42), false);
    }
  });
  test('simultaneous correct claims create exactly one permanent winner', async () => {
    const directory = mkdtempSync(join(tmpdir(), 'fork-race-test-'));
    const path = join(directory, 'race.sqlite');
    const database = new DatabaseSync(path);
    database.exec(readFileSync(new URL('../drizzle/0000_lonely_amazoness.sql', import.meta.url), 'utf8'));
    const workers = Array.from({ length: 12 }, (_, index) => new Worker(new URL(import.meta.url), {
      workerData: { path, id: index + 1 }, env: { ...process.env, NODE_NO_WARNINGS: '1' },
    }));
    try {
      await Promise.all(workers.map(worker => new Promise((resolve, reject) => {
        worker.once('message', message => message === 'ready' ? resolve() : reject(new Error('Not ready')));
        worker.once('error', reject);
      })));
      const completions = workers.map(worker => new Promise((resolve, reject) => {
        worker.once('message', result => result.error ? reject(new Error(result.error)) : resolve(result));
        worker.once('error', reject);
      }));
      for (const worker of workers) worker.postMessage('claim');
      const results = await Promise.all(completions);
      assert.equal(results.filter(result => result.won).length, 1);
      assert.equal(new Set(results.map(result => result.winner.login)).size, 1);
      assert.equal(database.prepare('SELECT COUNT(*) AS count FROM winners').get().count, 1);
      const winner = database.prepare('SELECT * FROM winners WHERE challenge = ?').get(CHALLENGE);
      const retry = await recordClaim(adapter(database), { ...identity(Number(winner.owner_id)), runId: '999999' });
      assert.equal(retry.won, true);
      assert.equal(retry.winner.run_id, winner.run_id);
      assert.equal(retry.winner.claimed_at, winner.claimed_at);
      assert.deepEqual(Object.keys(retry.winner).sort(), ['claimed_at', 'login', 'repository', 'run_id']);
    } finally {
      await Promise.all(workers.map(worker => worker.terminate()));
      database.close();
      rmSync(directory, { recursive: true, force: true });
    }
  });
}
