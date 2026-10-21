const ISSUER = "https://token.actions.githubusercontent.com";
const JWKS_URL = `${ISSUER}/.well-known/jwks`;
const UPSTREAM_ID = "1428727319";
const JWKS_TTL_MS = 5 * 60_000;
const MIN_REFRESH_MS = 30_000;
const REQUEST_TIMEOUT_MS = 10_000;
const MAX_TOKEN_CHARS = 16_384;
const MAX_RESPONSE_BYTES = 131_072;
const CLOCK_SKEW_SECONDS = 30;
const MAX_TOKEN_AGE_SECONDS = 15 * 60;

export class AuthError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "AuthError";
    this.status = status;
  }
}

export interface ForkIdentity {
  repositoryId: string;
  ownerId: string;
  login: string;
  repository: string;
  runId: string;
}

type Fetcher = (url: string, init?: RequestInit) => Promise<Response>;

export interface IdentityDependencies {
  fetch?: Fetcher;
  crypto?: Crypto;
  /** Epoch milliseconds; injectable only by trusted application code/tests. */
  now?: () => number;
}

type JsonObject = Record<string, unknown>;
type SigningKey = JsonWebKey & { kid: string };
type KeyCache = {
  keys: Map<string, SigningKey>;
  expiresAt: number;
  lastRefreshAt: number;
  pending?: Promise<Map<string, SigningKey>>;
};

// A production fetch function has one bounded cache. Injected test fetchers do
// not share keys with production or with one another.
const keyCaches = new WeakMap<Fetcher, KeyCache>();
const encoder = new TextEncoder();

function object(value: unknown): JsonObject | undefined {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? (value as JsonObject)
    : undefined;
}

function invalidIdentity(): AuthError {
  return new AuthError(401, "GitHub identity could not be verified. Run the workflow again.");
}

function retryLater(): AuthError {
  return new AuthError(503, "GitHub verification is temporarily unavailable. Retry the workflow shortly.");
}

function decodeBase64Url(value: string, maxBytes: number): Uint8Array<ArrayBuffer> {
  if (!value || !/^[A-Za-z0-9_-]+$/.test(value) || value.length % 4 === 1) {
    throw invalidIdentity();
  }
  const padded = value.replace(/-/g, "+").replace(/_/g, "/");
  try {
    const binary = atob(padded + "=".repeat((4 - (padded.length % 4)) % 4));
    if (binary.length > maxBytes) throw invalidIdentity();
    return Uint8Array.from(binary, (character) => character.charCodeAt(0));
  } catch {
    throw invalidIdentity();
  }
}

function decodeObject(value: string, maxBytes: number): JsonObject {
  try {
    const decoded = new TextDecoder("utf-8", { fatal: true }).decode(decodeBase64Url(value, maxBytes));
    const parsed = object(JSON.parse(decoded));
    if (!parsed) throw invalidIdentity();
    return parsed;
  } catch {
    throw invalidIdentity();
  }
}

function numericId(value: unknown): string | undefined {
  if (typeof value !== "string" || !/^[1-9][0-9]{0,15}$/.test(value)) return undefined;
  return Number.isSafeInteger(Number(value)) ? value : undefined;
}

function apiId(value: unknown): string | undefined {
  if (typeof value === "number" && Number.isSafeInteger(value) && value > 0) return String(value);
  return numericId(value);
}

function seconds(value: unknown): value is number {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0;
}

async function readJson(
  fetcher: Fetcher,
  url: string,
  headers: Record<string, string>,
  repositoryLookup = false,
): Promise<JsonObject> {
  const aborter = new AbortController();
  const timeout = setTimeout(() => aborter.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetcher(url, { headers, redirect: "error", signal: aborter.signal });
    if (!response.ok) {
      if (repositoryLookup && response.status === 404) {
        throw new AuthError(403, "This repository could not be verified as a public fork of hazelfjeld/teach-github.");
      }
      throw retryLater();
    }
    const declaredLength = response.headers.get("content-length");
    if (declaredLength && Number(declaredLength) > MAX_RESPONSE_BYTES) {
      await response.body?.cancel();
      throw retryLater();
    }
    if (!response.body) throw retryLater();
    const reader = response.body.getReader();
    const chunks: Uint8Array[] = [];
    let length = 0;
    try {
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        length += value.byteLength;
        if (length > MAX_RESPONSE_BYTES) {
          await reader.cancel();
          throw retryLater();
        }
        chunks.push(value);
      }
    } finally {
      reader.releaseLock();
    }
    const bytes = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) {
      bytes.set(chunk, offset);
      offset += chunk.byteLength;
    }
    const parsed = object(JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes)));
    if (!parsed) throw retryLater();
    return parsed;
  } catch (error) {
    if (error instanceof AuthError) throw error;
    throw retryLater();
  } finally {
    clearTimeout(timeout);
  }
}

async function signingKey(fetcher: Fetcher, kid: string, now: number): Promise<SigningKey> {
  let cache = keyCaches.get(fetcher);
  if (!cache) {
    cache = { keys: new Map(), expiresAt: 0, lastRefreshAt: -Infinity };
    keyCaches.set(fetcher, cache);
  }
  const fresh = now < cache.expiresAt;
  const cachedKey = cache.keys.get(kid);
  if (fresh && cachedKey) return cachedKey;
  if (!cache.pending && now - cache.lastRefreshAt < MIN_REFRESH_MS) {
    throw fresh ? invalidIdentity() : retryLater();
  }
  if (!cache.pending) {
    const current = cache;
    current.lastRefreshAt = now;
    current.pending = (async () => {
      const body = await readJson(fetcher, JWKS_URL, { Accept: "application/json" });
      if (!Array.isArray(body.keys) || body.keys.length === 0 || body.keys.length > 32) throw retryLater();
      const keys = new Map<string, SigningKey>();
      for (const candidate of body.keys) {
        const key = object(candidate);
        if (!key || key.kty !== "RSA" || key.alg !== "RS256" || (key.use !== undefined && key.use !== "sig")) continue;
        if (typeof key.kid !== "string" || !key.kid || key.kid.length > 200) continue;
        if (typeof key.n !== "string" || typeof key.e !== "string") continue;
        if (key.key_ops !== undefined && (!Array.isArray(key.key_ops) || !key.key_ops.includes("verify"))) continue;
        let modulus: Uint8Array;
        try { modulus = decodeBase64Url(key.n, 1024); } catch { continue; }
        if (modulus.byteLength < 256 || keys.has(key.kid)) throw retryLater();
        keys.set(key.kid, { kty: "RSA", alg: "RS256", kid: key.kid, n: key.n, e: key.e, use: "sig", key_ops: ["verify"], ext: true });
      }
      if (keys.size === 0) throw retryLater();
      current.keys = keys;
      current.expiresAt = now + JWKS_TTL_MS;
      return keys;
    })();
  }
  try {
    const pending = cache.pending;
    if (!pending) throw retryLater();
    const keys = await pending;
    const key = keys.get(kid);
    if (!key) throw invalidIdentity();
    return key;
  } finally {
    cache.pending = undefined;
  }
}

/** Authorize an owner-triggered workflow running inside a direct public fork. */
export async function authorizeFork(
  jwt: string,
  githubToken: string | undefined,
  audience: string,
  dependencies: IdentityDependencies = {},
): Promise<ForkIdentity> {
  if (typeof jwt !== "string" || jwt.length > MAX_TOKEN_CHARS) throw invalidIdentity();
  if (!audience || audience.length > 1024) throw new AuthError(503, "Challenge verification is not configured.");
  const parts = jwt.split(".");
  if (parts.length !== 3) throw invalidIdentity();
  const header = decodeObject(parts[0], 2048);
  const claims = decodeObject(parts[1], 12_288);
  const signature = decodeBase64Url(parts[2], 1024);
  if (header.alg !== "RS256" || typeof header.kid !== "string" || !header.kid || header.kid.length > 200) throw invalidIdentity();
  if ((header.typ !== undefined && header.typ !== "JWT") || header.crit !== undefined) throw invalidIdentity();
  const fetcher = dependencies.fetch ?? globalThis.fetch;
  const cryptography = dependencies.crypto ?? globalThis.crypto;
  const nowMs = (dependencies.now ?? Date.now)();
  const key = await signingKey(fetcher, header.kid, nowMs);
  let verified = false;
  try {
    const imported = await cryptography.subtle.importKey("jwk", key, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
    verified = await cryptography.subtle.verify("RSASSA-PKCS1-v1_5", imported, signature, encoder.encode(`${parts[0]}.${parts[1]}`));
  } catch {
    throw invalidIdentity();
  }
  if (!verified) throw invalidIdentity();
  const now = Math.floor(nowMs / 1000);
  if (claims.iss !== ISSUER || claims.aud !== audience) throw invalidIdentity();
  if (!seconds(claims.exp) || !seconds(claims.nbf) || !seconds(claims.iat)) throw invalidIdentity();
  if (claims.exp <= now || claims.nbf > now + CLOCK_SKEW_SECONDS || claims.iat > now + CLOCK_SKEW_SECONDS) throw invalidIdentity();
  if (claims.iat < now - MAX_TOKEN_AGE_SECONDS || claims.exp <= claims.iat || claims.nbf > claims.exp) throw invalidIdentity();
  if (claims.exp - claims.iat > MAX_TOKEN_AGE_SECONDS) throw invalidIdentity();
  const repositoryId = numericId(claims.repository_id);
  const ownerId = numericId(claims.repository_owner_id);
  const actorId = numericId(claims.actor_id);
  const runId = numericId(claims.run_id);
  if (!repositoryId || !ownerId || !actorId || !runId) throw invalidIdentity();
  if (claims.event_name !== "workflow_dispatch" || claims.runner_environment !== "github-hosted") {
    throw new AuthError(403, "Run the Reveal the number workflow manually in your fork using GitHub's hosted runner.");
  }
  if (repositoryId === UPSTREAM_ID || actorId !== ownerId) {
    throw new AuthError(403, "Fork hazelfjeld/teach-github into your personal account, then run its workflow yourself.");
  }
  if (typeof claims.repository !== "string" || !/^[A-Za-z0-9-]{1,39}\/[A-Za-z0-9_.-]{1,100}$/.test(claims.repository)) throw invalidIdentity();
  const headers: Record<string, string> = {
    Accept: "application/vnd.github+json",
    "User-Agent": "teach-github-challenge",
    "X-GitHub-Api-Version": "2022-11-28",
  };
  if (githubToken !== undefined && githubToken !== "") {
    if (typeof githubToken !== "string" || githubToken.length > 4096 || !/^[\x21-\x7E]+$/.test(githubToken)) throw invalidIdentity();
    headers.Authorization = `Bearer ${githubToken}`;
  }
  // The supplied runner token is used only on this fixed GitHub API origin.
  const repository = await readJson(fetcher, `https://api.github.com/repositories/${repositoryId}`, headers, true);
  const owner = object(repository.owner);
  const parent = object(repository.parent);
  if (apiId(repository.id) !== repositoryId || repository.fork !== true || repository.private !== false || apiId(parent?.id) !== UPSTREAM_ID) {
    throw new AuthError(403, "This repository must be a direct public fork of hazelfjeld/teach-github.");
  }
  if (!owner || owner.type !== "User" || apiId(owner.id) !== ownerId) {
    throw new AuthError(403, "Use a fork owned by your personal GitHub account.");
  }
  if (typeof repository.full_name !== "string" || repository.full_name.toLowerCase() !== claims.repository.toLowerCase()) throw invalidIdentity();
  if (typeof owner.login !== "string" || !/^[A-Za-z0-9-]{1,39}$/.test(owner.login)) throw invalidIdentity();
  if (repository.full_name.split("/")[0].toLowerCase() !== owner.login.toLowerCase()) throw invalidIdentity();
  return { repositoryId, ownerId, login: owner.login, repository: repository.full_name, runId };
}
