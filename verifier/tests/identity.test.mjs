import assert from 'node:assert/strict';
import { webcrypto } from 'node:crypto';
import test from 'node:test';
import { authorizeFork, AuthError } from '../lib/github-identity.ts';

const NOW = 1_800_000_000_000;
const AUDIENCE = 'https://challenge.example.test';
const ISSUER = 'https://token.actions.githubusercontent.com';
const JWKS_URL = `${ISSUER}/.well-known/jwks`;
const REPOSITORY_URL = 'https://api.github.com/repositories/2222222';
const pair = await webcrypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
const jwk = { ...await webcrypto.subtle.exportKey('jwk', pair.publicKey), kid: 'test-key', use: 'sig', alg: 'RS256' };
const baseClaims = {
  iss: ISSUER, aud: AUDIENCE, sub: 'repo:student/teach-github:ref:refs/heads/main',
  iat: NOW / 1000 - 10, nbf: NOW / 1000 - 10, exp: NOW / 1000 + 290,
  repository_id: '2222222', repository_owner_id: '123456', actor_id: '123456',
  repository: 'student/teach-github', event_name: 'workflow_dispatch',
  runner_environment: 'github-hosted', run_id: '987654',
};
const baseRepository = {
  id: 2222222, fork: true, private: false, full_name: 'student/teach-github',
  parent: { id: 1428727319 }, owner: { id: 123456, login: 'student', type: 'User' },
};

function encode(value) { return Buffer.from(JSON.stringify(value)).toString('base64url'); }
async function token(overrides = {}, headerOverrides = {}, signingKey = pair.privateKey) {
  const header = encode({ alg: 'RS256', typ: 'JWT', kid: 'test-key', ...headerOverrides });
  const payload = encode({ ...baseClaims, ...overrides });
  const signature = await webcrypto.subtle.sign('RSASSA-PKCS1-v1_5', signingKey, new TextEncoder().encode(`${header}.${payload}`));
  return `${header}.${payload}.${Buffer.from(signature).toString('base64url')}`;
}

function harness({ repository = baseRepository, status = 200, jwks = { keys: [jwk] }, jwksStatus = 200 } = {}) {
  const calls = [];
  const fetch = async (url, options) => {
    calls.push({ url, options });
    assert.equal(options.redirect, 'error');
    assert.ok(options.signal instanceof AbortSignal);
    if (url === JWKS_URL) {
      assert.equal(options.headers.Authorization, undefined, 'runner credential must never reach JWKS origin');
      return new Response(JSON.stringify(jwks), { status: jwksStatus });
    }
    assert.equal(url, REPOSITORY_URL, 'repository lookup must use the signed numeric ID');
    return new Response(JSON.stringify(repository), { status });
  };
  return { calls, dependencies: { fetch, crypto: webcrypto, now: () => NOW } };
}

async function rejected(jwt, context, status) {
  await assert.rejects(authorizeFork(jwt, undefined, AUDIENCE, context.dependencies), (error) => error instanceof AuthError && error.status === status);
}

test('valid GitHub-signed direct fork returns verified identity and scopes runner credential to GitHub API', async () => {
  const context = harness();
  const identity = await authorizeFork(await token(), 'test_runner_token', AUDIENCE, context.dependencies);
  assert.deepEqual(identity, { repositoryId: '2222222', ownerId: '123456', login: 'student', repository: 'student/teach-github', runId: '987654' });
  assert.equal(context.calls.length, 2);
  assert.equal(context.calls[1].options.headers.Authorization, 'Bearer test_runner_token');
});

test('tampered payload fails signature verification before repository lookup', async () => {
  const context = harness();
  const pieces = (await token()).split('.');
  pieces[1] = encode({ ...baseClaims, actor_id: '777777' });
  await rejected(pieces.join('.'), context, 401);
  assert.deepEqual(context.calls.map(({ url }) => url), [JWKS_URL]);
});

test('bad signature bytes fail before repository lookup', async () => {
  const context = harness();
  const pieces = (await token()).split('.');
  const signature = Buffer.from(pieces[2], 'base64url');
  signature[0] ^= 255;
  pieces[2] = signature.toString('base64url');
  await rejected(pieces.join('.'), context, 401);
  assert.equal(context.calls.length, 1);
});

for (const [name, override] of [
  ['wrong audience', { aud: 'https://attacker.example' }],
  ['array audience', { aud: [AUDIENCE] }],
  ['wrong issuer', { iss: 'https://attacker.example' }],
  ['expired token', { exp: NOW / 1000 - 1 }],
  ['not-yet-valid token', { nbf: NOW / 1000 + 120 }],
  ['future issue time', { iat: NOW / 1000 + 120 }],
  ['missing issue time', { iat: undefined }],
  ['unsafe repository ID', { repository_id: '9007199254740992' }],
  ['path in repository ID', { repository_id: '../../users' }],
  ['numeric rather than string repository ID', { repository_id: 2222222 }],
  ['malformed run ID', { run_id: '0' }],
]) {
  test(`${name} fails closed before repository API lookup`, async () => {
    const context = harness();
    await rejected(await token(override), context, 401);
    assert.equal(context.calls.length, 1);
  });
}

for (const [name, override] of [
  ['upstream repository', { repository_id: '1428727319' }],
  ['non-owner actor', { actor_id: '789012' }],
  ['pull-request event', { event_name: 'pull_request' }],
  ['self-hosted runner', { runner_environment: 'self-hosted' }],
]) {
  test(`${name} is rejected before repository API lookup`, async () => {
    const context = harness();
    await rejected(await token(override), context, 403);
    assert.equal(context.calls.length, 1);
  });
}

for (const [name, changes, status] of [
  ['wrong parent', { parent: { id: 555 } }, 403],
  ['unrelated repository', { fork: false }, 403],
  ['private repository', { private: true }, 403],
  ['wrong repository ID', { id: 9999999 }, 403],
  ['wrong owner ID', { owner: { id: 999, login: 'student', type: 'User' } }, 403],
  ['organization fork', { owner: { id: 123456, login: 'student', type: 'Organization' } }, 403],
  ['mismatched repository name', { full_name: 'student/different' }, 401],
  ['inconsistent owner login', { owner: { id: 123456, login: 'someone-else', type: 'User' } }, 401],
]) {
  test(`${name} in verified GitHub metadata is rejected`, async () => {
    const context = harness({ repository: { ...baseRepository, ...changes } });
    await rejected(await token(), context, status);
    assert.equal(context.calls.length, 2);
  });
}

test('case differences in the signed repository name are accepted', async () => {
  const context = harness();
  const identity = await authorizeFork(await token({ repository: 'Student/Teach-GitHub' }), undefined, AUDIENCE, context.dependencies);
  assert.equal(identity.repository, 'student/teach-github');
});

test('malformed, oversized, and algorithm-confused tokens do not cause any outbound request', async () => {
  const context = harness();
  for (const malformed of ['', 'abc.def', 'a'.repeat(17_000), '!.!.!', await token({}, { alg: 'none' }), await token({}, { crit: ['untrusted'] })]) {
    await rejected(malformed, context, 401);
  }
  assert.equal(context.calls.length, 0);
});

test('valid-key JWKS cache prevents repeated key requests', async () => {
  const context = harness();
  const signed = await token();
  await authorizeFork(signed, undefined, AUDIENCE, context.dependencies);
  await authorizeFork(signed, undefined, AUDIENCE, context.dependencies);
  assert.deepEqual(context.calls.map(({ url }) => url), [JWKS_URL, REPOSITORY_URL, REPOSITORY_URL]);
});

test('unknown key refreshes cached JWKS after cooldown and accepts a rotated signing key', async () => {
  const secondPair = await webcrypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
  const secondJwk = { ...await webcrypto.subtle.exportKey('jwk', secondPair.publicKey), kid: 'rotated-key', use: 'sig', alg: 'RS256' };
  const keys = [jwk];
  const context = harness({ jwks: { keys } });
  await authorizeFork(await token(), undefined, AUDIENCE, context.dependencies);
  keys.push(secondJwk);
  context.dependencies.now = () => NOW + 31_000;
  await authorizeFork(await token({}, { kid: 'rotated-key' }, secondPair.privateKey), undefined, AUDIENCE, context.dependencies);
  assert.equal(context.calls.filter(({ url }) => url === JWKS_URL).length, 2);
});

test('unknown keys cannot amplify JWKS requests during refresh cooldown', async () => {
  const context = harness();
  await authorizeFork(await token(), undefined, AUDIENCE, context.dependencies);
  await rejected(await token({}, { kid: 'unknown-1' }), context, 401);
  await rejected(await token({}, { kid: 'unknown-2' }), context, 401);
  assert.equal(context.calls.filter(({ url }) => url === JWKS_URL).length, 1);
});

for (const status of [401, 403, 429, 500, 503]) {
  test(`GitHub API ${status} produces a safe retryable verification error`, async () => {
    const context = harness({ status });
    await rejected(await token(), context, 503);
  });
}

test('missing public repository produces a denied-fork error', async () => {
  const context = harness({ status: 404 });
  await rejected(await token(), context, 403);
});

test('JWKS network or HTTP failures fail closed with retryable status', async () => {
  await rejected(await token(), harness({ jwksStatus: 503 }), 503);
  const dependencies = { fetch: async () => { throw new Error('private network detail'); }, crypto: webcrypto, now: () => NOW };
  await assert.rejects(authorizeFork(await token(), undefined, AUDIENCE, dependencies), (error) => error instanceof AuthError && error.status === 503 && !error.message.includes('private network detail'));
});

test('oversized JWKS response is rejected', async () => {
  const context = harness({ jwks: { keys: [jwk], padding: 'x'.repeat(140_000) } });
  await rejected(await token(), context, 503);
  assert.equal(context.calls.length, 1);
});

test('runner credential with header injection is rejected before GitHub API request', async () => {
  const context = harness();
  await assert.rejects(authorizeFork(await token(), 'unsafe\r\nheader', AUDIENCE, context.dependencies), (error) => error instanceof AuthError && error.status === 401);
  assert.equal(context.calls.length, 1);
});
