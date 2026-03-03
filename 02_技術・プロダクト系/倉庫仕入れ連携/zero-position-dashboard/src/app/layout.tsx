import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "0ポジション作戦 | Value Books",
  description: "倉庫オペレーション最適化ダッシュボード - 在庫を計画的に減らし、0ポジションを達成するための進捗管理システム",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className={`${inter.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
