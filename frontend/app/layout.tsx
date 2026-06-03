import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "SmartBus AI",
  description: "AI-assisted intercity bus ticket ranking prototype"
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
