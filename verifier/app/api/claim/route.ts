import { AuthError } from "@/lib/github-identity";
import { authenticateRequest, configuredChallenge, database, failure, json } from "@/lib/http";
import { recordClaim, validAnswer } from "@/lib/race";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    const { identity, body } = await authenticateRequest(request);
    const { answer } = configuredChallenge();
    if (!validAnswer(body.answer, answer)) {
      throw new AuthError(422, "The answer did not match. Restore challenge.py and run again.");
    }
    const result = await recordClaim(database(), identity);
    return json({ ...result, answer });
  } catch (error) { return failure(error); }
}
