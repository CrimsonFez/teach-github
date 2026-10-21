import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Fork to Reveal — Hazel’s GitHub Challenge",
  description: "One fixed number. Two hundred lines of Python. Fork the repository, run the workflow, and be first to reveal the answer.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
