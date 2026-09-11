import type { AgentEvent } from "../types/agent";

interface ExecutionTimelineProps {
  events: AgentEvent[];
}

function getEventLabel(event: AgentEvent): string {
  switch (event.event) {
    case "agent.started":
      return "Agent started";

    case "sql.generated":
      return "SQL generated";

    case "validation.updated":
      return "SQL validated";

    case "execution.updated":
      if (event.data.status === "completed") {
        return "SQL execution succeeded";
      }

      if (event.data.status === "classifying_error") {
        return "SQL execution failed";
      }

      return "SQL execution updated";

    case "error.classified":
      return `Error classified: ${
        event.data.error_category ?? "unknown"
      }`;

    case "diagnosis.completed":
      return "Error diagnosed";

    case "sql.repaired":
      return "SQL repaired";

    case "agent.completed":
      return "Agent completed";

    case "agent.finished":
      return "Agent finished";

    default:
      return event.event;
  }
}

function getIcon(event: AgentEvent): string {
  if (event.event === "sql.repaired") {
    return "↻";
  }

  if (
    event.event === "error.classified" ||
    (
      event.event === "execution.updated" &&
      event.data.status === "classifying_error"
    )
  ) {
    return "✗";
  }

  if (event.event === "agent.finished") {
    return event.status === "completed"
      ? "✓"
      : "✗";
  }

  return "✓";
}

export function ExecutionTimeline({
  events,
}: ExecutionTimelineProps) {
  return (
    <section className="panel">
      <div className="panel-title">
        Execution
      </div>

      {events.length === 0 ? (
        <div className="empty-state">
          No execution yet.
        </div>
      ) : (
        <div className="timeline">
          {events.map((event, index) => (
            <div
              className="timeline-item"
              key={`${event.event}-${index}`}
            >
              <span className="timeline-icon">
                {getIcon(event)}
              </span>

              <div className="timeline-content">
                <div className="timeline-label">
                  {getEventLabel(event)}
                </div>

                {event.data.error_category && (
                  <div className="timeline-detail">
                    Category:{" "}
                    {event.data.error_category}
                  </div>
                )}

                {event.data.attempt && (
                  <div className="timeline-detail">
                    Attempt {event.data.attempt}
                    {" / "}
                    {event.data.max_attempts}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
