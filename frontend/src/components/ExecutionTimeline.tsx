import type { AgentEvent } from "../types/agent";

interface ExecutionTimelineProps {
  events: AgentEvent[];
}

function getEventLabel(event: AgentEvent): string {
  switch (event.event) {
    case "agent.started":
      return "Agent Workflow Initialized";

    case "sql.generated":
      return "SQL Generated";

    case "validation.updated":
      if (
        event.data.status === "classifying_error" ||
        event.data.status === "failed"
      ) {
        return "SQL Validation Detected Error";
      }
      return "SQL Validated (AST Guardrails Passed)";

    case "execution.updated":
      if (event.data.status === "completed") {
        return "PostgreSQL Execution Succeeded";
      }

      if (event.data.status === "classifying_error") {
        return "PostgreSQL Execution Failed";
      }

      return "PostgreSQL Execution Updated";

    case "error.classified":
      return `Error Classified: ${event.data.error_category ?? "unknown"}`;

    case "diagnosis.completed":
      return "Root Cause Diagnosed";

    case "sql.repaired":
      return "SQL Repaired (Self-Healing Invoked)";

    case "agent.completed":
      return "Workflow Completed Successfully";

    case "agent.finished":
      return event.status === "completed"
        ? "Workflow Finished Successfully"
        : "Workflow Finished (Failed)";

    default:
      return event.event;
  }
}

function getIconState(event: AgentEvent): {
  icon: string;
  className: string;
} {
  if (event.event === "sql.repaired") {
    return { icon: "↻", className: "icon-repair" };
  }

  if (
    event.event === "error.classified" ||
    (event.event === "execution.updated" &&
      event.data.status === "classifying_error") ||
    (event.event === "validation.updated" &&
      (event.data.status === "classifying_error" ||
        event.data.status === "failed"))
  ) {
    return { icon: "✗", className: "icon-error" };
  }

  if (event.event === "diagnosis.completed") {
    return { icon: "!", className: "icon-diagnose" };
  }

  if (event.event === "agent.finished") {
    return event.status === "completed"
      ? { icon: "✓", className: "icon-success" }
      : { icon: "✗", className: "icon-error" };
  }

  return { icon: "✓", className: "icon-success" };
}

export function ExecutionTimeline({ events }: ExecutionTimelineProps) {
  return (
    <section className="product-mockup-dark">
      <div className="mockup-header">
        <div className="mockup-title-wrap">
          <div className="terminal-dots">
            <span className="terminal-dot" style={{ backgroundColor: "#ff5f56" }} />
            <span className="terminal-dot" style={{ backgroundColor: "#ffbd2e" }} />
            <span className="terminal-dot" style={{ backgroundColor: "#27c93f" }} />
          </div>
          <span className="mockup-title">Execution Timeline & Observability</span>
        </div>
        <span className="mockup-badge">
          {events.length} {events.length === 1 ? "Event" : "Events"}
        </span>
      </div>

      {events.length === 0 ? (
        <div className="empty-timeline">
          No execution telemetry yet. Submit a query above to view real-time LangGraph agent events.
        </div>
      ) : (
        <div className="timeline-list">
          {events.map((event, index) => {
            const { icon, className } = getIconState(event);
            return (
              <div className="timeline-row" key={`${event.event}-${index}`}>
                <div className={`timeline-icon-box ${className}`}>{icon}</div>

                <div className="timeline-content-card">
                  <div className="timeline-main-line">
                    <span className="timeline-title">{getEventLabel(event)}</span>
                    {event.data.attempt && (
                      <span className="timeline-meta">
                        Attempt {event.data.attempt} / {event.data.max_attempts}
                      </span>
                    )}
                  </div>

                  {(event.data.error_category ||
                    event.data.error_message ||
                    event.data.diagnosis ||
                    event.data.repair_reason ||
                    (event.event === "sql.generated" && event.data.sql) ||
                    (event.event === "sql.repaired" && event.data.sql)) && (
                    <div className="timeline-details-area">
                      {event.data.error_category && (
                        <span className="category-tag">
                          Category: {event.data.error_category}
                        </span>
                      )}

                      {event.data.error_message && (
                        <div style={{ color: "#ff9b9b", fontSize: "12px" }}>
                          Error: {event.data.error_message}
                        </div>
                      )}

                      {event.data.diagnosis && (
                        <div className="diagnosis-box">
                          <strong>Diagnosis:</strong> {event.data.diagnosis}
                        </div>
                      )}

                      {event.data.repair_reason && (
                        <div className="repaired-box">
                          <strong>Repair Reason:</strong> {event.data.repair_reason}
                        </div>
                      )}

                      {(event.event === "sql.generated" || event.event === "sql.repaired") &&
                        event.data.sql && (
                          <code
                            style={{
                              fontFamily: "var(--font-code)",
                              fontSize: "12px",
                              color: "#cbd5e1",
                              background: "rgba(0,0,0,0.3)",
                              padding: "4px 8px",
                              borderRadius: "4px",
                              display: "block",
                              marginTop: "4px",
                            }}
                          >
                            {event.data.sql}
                          </code>
                        )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
