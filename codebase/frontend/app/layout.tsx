import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "SmartTravel AI",
  description: "AI-assisted travel planning, ticket search, and stay support prototype"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
