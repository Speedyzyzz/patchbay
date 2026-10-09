import React from "react";
import { GitFork, FileCode, ArrowRight } from "lucide-react";

interface CallSiteItem {
  symbolName: string;
  files: string[];
}

interface CallSiteGraphProps {
  items: CallSiteItem[];
}

export function CallSiteGraph({ items }: CallSiteGraphProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <GitFork className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-slate-200 text-sm">Repository API Usage Graph</span>
        </div>
        <span className="text-xs text-slate-500 font-mono">AST Parsed Symbols</span>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {items.map((item) => (
          <div
            key={item.symbolName}
            className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono space-y-2"
          >
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800 text-cyan-300 font-bold">
                {item.symbolName}
              </span>
              <span className="text-slate-500">invoked across {item.files.length} call site(s)</span>
            </div>

            <div className="space-y-1 pl-2 border-l border-slate-800">
              {item.files.map((f) => (
                <div key={f} className="flex items-center gap-2 text-slate-400">
                  <FileCode className="w-3.5 h-3.5 text-slate-600" />
                  <span>{f}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
