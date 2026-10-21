import { env } from "cloudflare:workers";
import { AuthError, authorizeFork } from "./github-identity";

export const AUDIENCE = "https://teach-github-challenge.airheadhazelnut.chatgpt.site";
const MAX_BODY = 8192;

type ChallengeEnvironment = {
  DB?: D1Database;
  CHALLENGE_SEED?: string;
  CHALLENGE_ANSWER?: string;
};

export function runtime() {
  return env as unknown as ChallengeEnvironment;
}

export function configuredChallenge() {
  const { CHALLENGE_SEED: seed, CHALLENGE_ANSWER: raw } = runtime();
  if (!seed || !/^[a-f0-9]{16}$/i.test(seed)
      || !raw || !/^(?:[1-9][0-9]?|100)$/.test(raw)) {
    throw new AuthError(503, "The challenge is being prepared. Please try again shortly.");
  }
  return { seed, answer: Number(raw) };
}

export function database() {
  const db = runtime().DB;
  if (!db) throw new AuthError(503, "The race board is temporarily unavailable. Please retry.");
  return db;
}

export function json(value: unknown, status = 200) {
  return Response.json(value, {
    status,
    headers: {
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      "Referrer-Policy": "no-referrer",
      ...(status === 503 ? { "Retry-After": "3" } : {}),
    },
  });
}

export function failure(error: unknown) {
  if (error instanceof AuthError) return json({ error: error.message }, error.status);
  // Do not log requests, tokens, private seed, or unexpected exception details.
  return json({ error: "The challenge is temporarily unavailable. Please retry." }, 503);
}

async function bodyJson(request: Request): Promise<Record<string, unknown>> {
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
    throw new AuthError(415, "Send the request as application/json.");
  }
  const reader = request.body?.getReader();
  if (!reader) throw new AuthError(400, "A JSON request body is required.");
  const chunks: Uint8Array[] = [];
  let size = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > MAX_BODY) {
      await reader.cancel();
      throw new AuthError(413, "Request body is too large.");
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size);
  let position = 0;
  for (const chunk of chunks) { bytes.set(chunk, position); position += chunk.length; }
  let value: unknown;
  try { value = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes)); }
  catch { throw new AuthError(400, "The request body must be valid JSON."); }
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new AuthError(400, "The request body must be a JSON object.");
  }
  return value as Record<string, unknown>;
}

export async function authenticateRequest(request: Request) {
  const authorization = request.headers.get("authorization") ?? "";
  if (authorization.length > 16384 || !/^Bearer [A-Za-z0-9_.-]+$/.test(authorization)) {
    throw new AuthError(401, "Run Reveal the number from the Actions tab of your fork.");
  }
  const body = await bodyJson(request);
  if (body.github_token !== undefined
      && (typeof body.github_token !== "string" || body.github_token.length > 2048)) {
    throw new AuthError(400, "Invalid GitHub authentication.");
  }
  const identity = await authorizeFork(authorization.slice(7),
    body.github_token as string | undefined, AUDIENCE);
  return { body, identity };
}
