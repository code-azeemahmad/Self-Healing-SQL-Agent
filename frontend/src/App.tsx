import { useMemo, useState } from "react";

import { ExecutionTimeline } from "./components/ExecutionTimeline";
import { Metrics } from "./components/Metrics";
import { QueryInput } from "./components/QueryInput";
import { ResultTable } from "./components/ResultTable";
import { SpikeMark } from "./components/SpikeMark";
import { SqlViewer } from "./components/SqlViewer";
import { streamAgentQuery } from "./services/agentApi";
import type { AgentEvent, AgentResult } from "./types/agent";

const EMPTY_RESULT: AgentResult = {
  sql: null,
  rows: [],
  columns: [],
  attempt: 0,
  max_attempts: 3,
  llm_calls: 0,
  repair_attempts: 0,
  execution_ms: 0,
  row_count: 0,
  status: "idle",
};

function App() {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [result, setResult] = useState<AgentResult>(EMPTY_RESULT);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const finalEvent = useMemo(
    () => [...events].reverse().find((event) => event.event === "agent.finished"),
    [events],
  );

  async function handleQuery(query: string) {
    setRunning(true);
    setError(null);
    setEvents([]);
    setResult(EMPTY_RESULT);

    try {
      await streamAgentQuery(query, {
        onEvent: (event) => {
          setEvents((current) => [...current, event]);
          updateResultFromEvent(event);
        },
        onError: (streamError) => {
          setError(streamError.message);
        },
      });
    } catch (streamError) {
      const message =
        streamError instanceof Error
          ? streamError.message
          : "An unexpected streaming error occurred.";
      setError(message);
    } finally {
      setRunning(false);
    }
  }

  function updateResultFromEvent(event: AgentEvent) {
    setResult((current) => {
      const data = event.data;

      return {
        ...current,
        sql: data.sql ?? current.sql,
        rows: data.rows ?? current.rows,
        columns: data.columns ?? current.columns,
        attempt: data.attempt ?? current.attempt,
        max_attempts: data.max_attempts ?? current.max_attempts,
        llm_calls: data.llm_calls ?? current.llm_calls,
        repair_attempts: data.repair_attempts ?? current.repair_attempts,
        execution_ms: data.execution_ms ?? current.execution_ms,
        row_count: data.row_count ?? current.row_count,
        status: data.status ?? current.status,
        termination_reason: data.termination_reason ?? current.termination_reason,
      };
    });
  }

  const isCompleted = finalEvent?.status === "completed";
  const isFailed = finalEvent?.status === "failed";

  return (
    <div className="app-shell">
      {/* Top Navigation */}
      <nav className="top-nav">
        <div className="top-nav-inner">
          <div className="brand-cluster">
            <SpikeMark size={22} />
            <span className="brand-title">Autonomous SQL Agent</span>
            <span className="brand-badge">Self-Healing Engine</span>
          </div>

          <div className="nav-actions">
            {(running || isCompleted || isFailed) && (
              <div
                className={`status-badge ${
                  running
                    ? "running"
                    : isCompleted
                      ? "success"
                      : "error"
                }`}
              >
                <span className="status-indicator" />
                <span>
                  {running
                    ? "Self-Healing Active..."
                    : isCompleted
                      ? "Execution Succeeded"
                      : "Execution Failed"}
                </span>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-container">
        {/* Editorial Hero Band */}
        <header className="hero-band">
          <h1 className="hero-headline">
            Query your database in natural language with autonomous self-healing.
          </h1>

          <p className="hero-subhead">
            Translates queries into PostgreSQL syntax, performs AST guardrail verification,
            and automatically classifies, diagnoses, and repairs runtime SQL errors in real time.
          </p>
        </header>

        {/* Error Banner */}
        {error && (
          <div className="error-banner">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <div>
              <strong>Execution Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Query Input Section */}
        <QueryInput disabled={running} onSubmit={handleQuery} />

        {/* Real-Time Observability & Timeline */}
        <ExecutionTimeline events={events} />

        {/* SQL Code Window */}
        <SqlViewer sql={result.sql} title="Generated &amp; Repaired SQL" />

        {/* Performance Metrics */}
        <Metrics
          attempt={result.attempt}
          maxAttempts={result.max_attempts}
          llmCalls={result.llm_calls}
          repairAttempts={result.repair_attempts}
          executionMs={result.execution_ms}
          rowCount={result.row_count}
        />

        {/* Results Table */}
        <ResultTable rows={result.rows} columns={result.columns} />
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <SpikeMark size={16} />
            <span>Autonomous SQL Agent</span>
          </div>

          <div className="footer-info">
            FastAPI · LangGraph · PostgreSQL · Ollama · React + TypeScript
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
