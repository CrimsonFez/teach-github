CREATE TABLE `winners` (
	`challenge` text PRIMARY KEY NOT NULL,
	`login` text NOT NULL,
	`repository` text NOT NULL,
	`repository_id` text NOT NULL,
	`owner_id` text NOT NULL,
	`run_id` text NOT NULL,
	`claimed_at` text NOT NULL
);
