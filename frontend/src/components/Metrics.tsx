interface MetricsProps {
  attempt: number;
  maxAttempts: number;
  llmCalls: number;
  repairAttempts: number;
  executionMs: number;
  rowCount: number;
}

export function Metrics({
  attempt,
  maxAttempts,
  llmCalls,
  repairAttempts,
  executionMs,
  rowCount,
}: MetricsProps) {
  return (
    <section className="metrics">
      <div className="metric">
        <span>Attempts</span>
        <strong>
          {attempt} / {maxAttempts}
        </strong>
      </div>

      <div className="metric">
        <span>LLM calls</span>
        <strong>{llmCalls}</strong>
      </div>

      <div className="metric">
        <span>Repairs</span>
        <strong>{repairAttempts}</strong>
      </div>

      <div className="metric">
        <span>Execution</span>
        <strong>
          {executionMs.toFixed(1)} ms
        </strong>
      </div>

      <div className="metric">
        <span>Rows</span>
        <strong>{rowCount}</strong>
      </div>
    </section>
  );
}
