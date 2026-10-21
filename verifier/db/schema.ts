import { sqliteTable, text } from "drizzle-orm/sqlite-core";

export const winners = sqliteTable("winners", {
  challenge: text("challenge").primaryKey(),
  login: text("login").notNull(),
  repository: text("repository").notNull(),
  repositoryId: text("repository_id").notNull(),
  ownerId: text("owner_id").notNull(),
  runId: text("run_id").notNull(),
  claimedAt: text("claimed_at").notNull(),
});
