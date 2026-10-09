import React from "react";
import Link from "next/link";
import { GitPullRequest, ArrowRight, CheckCircle2, Activity } from "lucide-react";

export default function PatchBayDashboard() {
  const migrations = [
    {
      id: "mig_stripe_v12_v13",
      target_sdk: "stripe-python",
      breaking_changes: 4,
      call_sites_affected: 18,
      status: "synthesized_and_verified",
      diff_ratio: 0.82,
      typecheck_status: "passed",
    },
    {
      id: "mig_github_rest_v5",
      target_sdk: "octokit-rest",
      breaking_changes: 2,
      call_sites_affected: 9,
      status: "synthesized_and_verified",
      diff_ratio: 0.75,
      typecheck_status: "passed",
    },
    {
      id: "mig_openai_v1_modern",
      target_sdk: "openai-python",
      breaking_changes: 6,
      call_sites_affected: 34,
      status: "synthesized_and_verified",
      diff_ratio: 0.89,
      typecheck_status: "passed",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Semantic API Migrations</h1>
          <p className="text-sm text-slate-400 mt-1">
            AST-level codemod synthesis for upstream breaking changes. Zero brittle regex.
          </p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/graph"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium rounded-lg border border-slate-700 transition-colors"
          >
            Explore API Usage Graph
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Typecheck Recovery Rate</span>
          <p className="text-2xl font-bold text-cyan-400 font-mono">100.0%</p>
          <span className="text-[11px] text-slate-500 font-mono">LibCST Synthesized Candidates</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Average Minimal Diff Ratio</span>
          <p className="text-2xl font-bold text-emerald-400 font-mono">0.85</p>
          <span className="text-[11px] text-slate-500 font-mono">Preserves Comments & Formatting</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Behavioral Equivalence</span>
          <p className="text-2xl font-bold text-indigo-400 font-mono">100.0% Pass</p>
          <span className="text-[11px] text-slate-500 font-mono">Contract Test Suites</span>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-sm font-semibold text-slate-200">Active Migration Plans</h2>
        <div className="space-y-3">
          {migrations.map((m) => (
            <div
              key={m.id}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 transition-all flex items-center justify-between group"
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm font-bold text-slate-100">{m.id}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-cyan-950 border border-cyan-800 text-cyan-300">
                    {m.target_sdk}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Verified</span>
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-400 font-mono">
                  <span>{m.breaking_changes} breaking changes detected</span>
                  <span>•</span>
                  <span>{m.call_sites_affected} call sites patched</span>
                  <span>•</span>
                  <span>diff ratio: {m.diff_ratio}</span>
                </div>
              </div>

              <div>
                <Link
                  href={`/migrations/${m.id}`}
                  className="px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
                >
                  <GitPullRequest className="w-4 h-4" />
                  <span>Review AST Patch</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1 opacity-70 group-hover:translate-x-0.5 transition-transform" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
