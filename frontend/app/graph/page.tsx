import React from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { CallSiteGraph } from "@/components/CallSiteGraph";

export default function UsageGraphPage() {
  const items = [
    {
      symbolName: "stripe.Charge.create",
      files: ["services/billing/processor.py", "services/subscriptions/checkout.py"],
    },
    {
      symbolName: "octokit.rest.repos.get",
      files: ["lib/github/sync.ts", "workers/repo_indexer.ts"],
    },
    {
      symbolName: "openai.ChatCompletion.create",
      files: ["agents/coder.py", "agents/reviewer.py", "evals/runner.py"],
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">Repository API Usage Graph</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Call site mapping powered by language AST parsing.
            </p>
          </div>
        </div>
      </div>

      <CallSiteGraph items={items} />
    </div>
  );
}
