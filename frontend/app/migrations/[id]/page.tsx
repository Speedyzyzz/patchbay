"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, CheckCircle, GitPullRequest, ShieldCheck } from "lucide-react";
import { ContractDiffCard } from "@/components/ContractDiffCard";
import { ASTDiffViewer } from "@/components/ASTDiffViewer";

export default function MigrationReviewPage() {
  const params = useParams();
  const id = (params?.id as string) || "mig_sample";
  const [prCreated, setPrCreated] = useState(false);

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
            <h1 className="text-xl font-bold tracking-tight text-white font-mono">{id}</h1>
            <p className="text-xs text-slate-400 mt-0.5">AST Rewrite Synthesis & Verification Report</p>
          </div>
        </div>

        <button
          onClick={() => setPrCreated(true)}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold flex items-center gap-2 shadow-sm transition-colors"
        >
          <GitPullRequest className="w-4 h-4" />
          <span>Export Automated PR Branch</span>
        </button>
      </div>

      {prCreated && (
        <div className="p-4 bg-emerald-950/80 border border-emerald-800 rounded-xl text-emerald-300 text-xs font-mono flex items-center gap-2">
          <CheckCircle className="w-4 h-4 text-emerald-400" />
          <span>PR Branch generated: `git branch patchbay/mig-stripe-v13`. 100% type-checked.</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4">
          <ContractDiffCard
            category="endpoint_rename"
            targetSymbol="client.charges.create"
            replacementSymbol="client.payment_intents.create"
            migrationHint="Stripe legacy charge API deprecated in favor of PaymentIntents. Required parameter currency preserved."
          />
          <ContractDiffCard
            category="param_added"
            targetSymbol="POST /v1/payment_intents"
            replacementSymbol={null}
            migrationHint="Required parameter automatic_payment_methods={'enabled': True} added."
          />
        </div>

        <div className="lg:col-span-2 space-y-4">
          <ASTDiffViewer
            filePath="services/billing/processor.py"
            originalCode={`# Process payment charge\ncharge = stripe.Charge.create(\n    amount=amount_cents,\n    currency="usd",\n    source=card_token\n)`}
            patchedCode={`# Process payment charge\nintent = stripe.PaymentIntent.create(\n    amount=amount_cents,\n    currency="usd",\n    automatic_payment_methods={"enabled": True}\n)`}
            syntaxValid={true}
            diffRatio={0.85}
          />
        </div>
      </div>
    </div>
  );
}
