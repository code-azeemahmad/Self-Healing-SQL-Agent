import { useMemo, useState } from "react";

import { ExecutionTimeline } from "./components/ExecutionTimeline";
import { Metrics } from "./components/Metrics";
import { QueryInput } from "./components/QueryInput";
import { ResultTable } from "./components/ResultTable";
import { SqlViewer } from "./components/SqlViewer";
import { streamAgentQuery } from "./services/agentApi";
import type {
  AgentEvent,
  AgentResult,
} from "./types/agent";

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
  const [events, setEvents] = useState<
    AgentEvent[]
  >([]);

  const [result, setResult] =
    useState<AgentResult>(
      EMPTY_RESULT,
    );

  const [running, setRunning] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const finalEvent = useMemo(
    () =>
      [...events]
        .reverse()
        .find(
          (event) =>
            event.event === "agent.finished",
        ),
    [events],
  );

  async function handleQuery(
    query: string,
  ) {
    setRunning(true);
    setError(null);
    setEvents([]);
    setResult(EMPTY_RESULT);

    try {
      await streamAgentQuery(
        query,
        {
          onEvent: (event) => {
            setEvents((current) => [
              ...current,
              event,
            ]);

            updateResultFromEvent(event);
          },

          onError: (streamError) => {
            setError(
              streamError.message,
            );
          },
        },
      );
    } catch (streamError) {
      const message =
        streamError instanceof Error
          ? streamError.message
          : "Unknown error.";

      setError(message);
    } finally {
      setRunning(false);
    }
  }

  function updateResultFromEvent(
    event: AgentEvent,
  ) {
    setResult((current) => {
      const data = event.data;

      return {
        ...current,

        sql:
          data.sql ??
          current.sql,

        rows:
          data.rows ??
          current.rows,

        columns:
          data.columns ??
          current.columns,

        attempt:
          data.attempt ??
          current.attempt,

        max_attempts:
          data.max_attempts ??
          current.max_attempts,

        llm_calls:
          data.llm_calls ??
          current.llm_calls,

        repair_attempts:
          data.repair_attempts ??
          current.repair_attempts,

        execution_ms:
          data.execution_ms ??
          current.execution_ms,

        row_count:
          data.row_count ??
          current.row_count,

        status:
          data.status ??
          current.status,

        termination_reason:
          data.termination_reason ??
          current.termination_reason,
      };
    });
  }

  const success =
    finalEvent?.status ===
    "completed";

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <div className="eyebrow">
            AI ENGINEERING PROJECT
          </div>

          <h1>
            Autonomous SQL Agent
          </h1>

          <p>
            Generate, validate, execute,
            and self-heal PostgreSQL queries.
          </p>
        </div>

        <div
          className={`status-badge ${
            running
              ? "running"
              : success
                ? "success"
                : ""
          }`}
        >
          {running
            ? "Running"
            : success
              ? "Completed"
              : "Ready"}
        </div>
      </header>

      <main className="content">
        <QueryInput
          disabled={running}
          onSubmit={handleQuery}
        />

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <ExecutionTimeline
          events={events}
        />

        <SqlViewer
          sql={result.sql}
          title="Current SQL"
        />

        <Metrics
          attempt={result.attempt}
          maxAttempts={
            result.max_attempts
          }
          llmCalls={result.llm_calls}
          repairAttempts={
            result.repair_attempts
          }
          executionMs={
            result.execution_ms
          }
          rowCount={
            result.row_count
          }
        />

        <ResultTable
          rows={result.rows}
          columns={result.columns}
        />
      </main>
    </div>
  );
}

export default App;
