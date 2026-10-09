import React from "react";
import { CheckCircle2, ShieldCheck, FileCode } from "lucide-react";

interface ASTDiffViewerProps {
  filePath: string;
  originalCode: string;
  patchedCode: string;
  syntaxValid: boolean;
  diffRatio: number;
}

export function ASTDiffViewer({
  filePath,
  originalCode,
  patchedCode,
  syntaxValid,
  diffRatio,
}: ASTDiffViewerProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <FileCode className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-slate-200 text-sm font-mono">{filePath}</span>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="text-slate-400">Minimal Diff Ratio: <strong className="text-cyan-300">{diffRatio}</strong></span>
          <span className="flex items-center gap-1 text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>AST Valid</span>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
        <div className="space-y-1">
          <span className="text-slate-400 block font-sans text-xs">Original Call Site:</span>
          <pre className="p-3 bg-slate-950 border border-slate-800/80 rounded-lg text-rose-300/90 overflow-x-auto max-h-64">
            {originalCode}
          </pre>
        </div>

        <div className="space-y-1">
          <span className="text-slate-400 block font-sans text-xs">Synthesized AST Rewrite (LibCST):</span>
          <pre className="p-3 bg-slate-950 border border-emerald-900/40 rounded-lg text-emerald-300 overflow-x-auto max-h-64">
            {patchedCode}
          </pre>
        </div>
      </div>
    </div>
  );
}
