import { AlertTriangle, CheckCircle2 } from "lucide-react";

import type { AgentResponse } from "@/lib/types";

type PathStatusProps = {
  result: AgentResponse;
};

export function PathStatus({ result }: PathStatusProps) {
  const isWarning = result.path === "low_confidence";
  const Icon = isWarning ? AlertTriangle : CheckCircle2;

  return (
    <div
      className={isWarning ? "path-status warning" : "path-status"}
      data-testid={isWarning ? "low-confidence-warning" : "happy-status"}
    >
      <Icon aria-hidden="true" size={20} />
      <div>
        <p>{result.summary}</p>
        {result.warning ? <span>{result.warning}</span> : null}
      </div>
    </div>
  );
}
