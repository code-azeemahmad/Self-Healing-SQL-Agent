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
    <section className="metrics-grid">
      <div className="metric-card">
        <span className="metric-label">Attempts</span>
        <strong className="metric-value">
          {attempt} <span style={{ fontSize: "18px", color: "var(--color-muted)" }}>/ {maxAttempts}</span>
        </strong>
        <span className="metric-sub">Self-healing quota</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">LLM Calls</span>
        <strong className="metric-value">{llmCalls}</strong>
        <span className="metric-sub">Generations + Repairs</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Repairs</span>
        <strong className="metric-value" style={{ color: repairAttempts > 0 ? "var(--color-primary)" : "inherit" }}>
          {repairAttempts}
        </strong>
        <span className="metric-sub">Autonomous fixes</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Latency</span>
        <strong className="metric-value">{executionMs.toFixed(0)}<span style={{ fontSize: "16px" }}> ms</span></strong>
        <span className="metric-sub">Database execution</span>
      </div>

      <div className="metric-card">
        <span className="metric-label">Rows</span>
        <strong className="metric-value">{rowCount}</strong>
        <span className="metric-sub">Records returned</span>
      </div>
    </section>
  );
}
