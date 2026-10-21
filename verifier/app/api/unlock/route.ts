import { authenticateRequest, configuredChallenge, failure, json } from "@/lib/http";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    await authenticateRequest(request);
    const { seed } = configuredChallenge();
    return json({ seed });
  } catch (error) { return failure(error); }
}
