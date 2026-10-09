import React from "react";
import { ArrowRight, AlertCircle, RefreshCw } from "lucide-react";

interface ContractDiffCardProps {
  category: string;
  targetSymbol: string;
  replacementSymbol?: string | null;
  migrationHint: string;
}

export function ContractDiffCard({
  category,
  targetSymbol,
  replacementSymbol,
  migrationHint,
}: ContractDiffCardProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs px-2.5 py-0.5 rounded-full font-mono uppercase bg-cyan-950 border border-cyan-800 text-cyan-300">
          {category.replace(/_/g, " ")}
        </span>
        <span className="text-xs text-slate-500 font-mono">OpenAPI Breaking Diff</span>
      </div>

      <div className="flex items-center gap-3 p-3 bg-slate-950 border border-slate-800/80 rounded-lg text-xs font-mono">
        <span className="text-rose-400 line-through truncate max-w-xs">{targetSymbol}</span>
        {replacementSymbol && (
          <>
            <ArrowRight className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            <span className="text-emerald-400 font-semibold truncate max-w-xs">{replacementSymbol}</span>
          </>
        )}
      </div>

      <p className="text-xs text-slate-400 leading-relaxed">{migrationHint}</p>
    </div>
  );
}
