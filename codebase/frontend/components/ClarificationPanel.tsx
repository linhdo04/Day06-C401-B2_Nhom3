import { HelpCircle, MapPinned, Route } from "lucide-react";

import type { AgentResponse, ClarificationChoice } from "@/lib/types";

type ClarificationPanelProps = {
  result: AgentResponse;
  onClarify: (choice: ClarificationChoice) => void;
};

export function ClarificationPanel({ result, onClarify }: ClarificationPanelProps) {
  return (
    <div className="decision-panel" data-testid="clarification-panel">
      <div className="panel-icon">
        <HelpCircle aria-hidden="true" size={26} />
      </div>
      <p className="eyebrow">Cần xác nhận trước khi xếp hạng</p>
      <h2>{result.clarification_question}</h2>
      <p>
        Agent không tự đoán ở case nhập nhằng vì user có thể ra sai bến hoặc chọn nhầm nhà xe.
      </p>

      <div className="clarify-actions">
        <button data-testid="clarify-pickup" onClick={() => onClarify("pickup_place")} type="button">
          <MapPinned aria-hidden="true" size={18} />
          Đó là điểm đón
        </button>
        <button data-testid="clarify-operator" onClick={() => onClarify("bus_operator")} type="button">
          <Route aria-hidden="true" size={18} />
          Đó là nhà xe
        </button>
      </div>
    </div>
  );
}
