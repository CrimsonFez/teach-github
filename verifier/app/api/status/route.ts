import { database, failure, json } from "@/lib/http";
import { CHALLENGE, publicWinner, SELECT_WINNER, type WinnerRow } from "@/lib/race";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const row = await database().prepare(SELECT_WINNER).bind(CHALLENGE).first<WinnerRow>();
    return json({ challenge: CHALLENGE, status: row ? "claimed" : "open",
      winner: row ? publicWinner(row) : null });
  } catch (error) { return failure(error); }
}
