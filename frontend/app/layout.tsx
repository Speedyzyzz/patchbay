import type { Metadata } from "next";
import React from "react";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "PatchBay — Semantic API-Evolution & AST Migration Infrastructure",
  description: "Compiler-adjacent platform that maps breaking changes to AST call sites and synthesizes minimal rewrites",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col font-sans">
        <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur px-6 py-4 flex items-center justify-between sticky top-0 z-50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-cyan-600 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/20">
              PB
            </div>
            <div>
              <span className="font-semibold text-lg tracking-tight text-white">PatchBay</span>
              <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-300 font-mono">
                LibCST / AST
              </span>
            </div>
          </div>
          <nav className="flex items-center gap-6 text-sm text-slate-400">
            <Link href="/" className="hover:text-white transition-colors">Migrations</Link>
            <Link href="/graph" className="hover:text-white transition-colors">API Usage Graph</Link>
            <span className="text-xs px-2.5 py-1 bg-cyan-950 border border-cyan-800 text-cyan-400 rounded-md font-mono">
              100% Type-Safe Patches
            </span>
          </nav>
        </header>
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto">{children}</main>
      </body>
    </html>
  );
}
