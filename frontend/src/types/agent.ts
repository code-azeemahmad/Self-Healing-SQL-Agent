export type AgentEventName =
  | "agent.started"
  | "sql.generated"
  | "validation.updated"
  | "execution.updated"
  | "error.classified"
  | "diagnosis.completed"
  | "sql.repaired"
  | "agent.completed"
  | "agent.finished";

export interface AgentEvent {
  request_id: string;
  event: AgentEventName | string;
  status: string;
  data: {
    sql?: string;
    status?: string;
    error_category?: string;
    error_message?: string;
    diagnosis?: string;
    repair_reason?: string;
    attempt?: number;
    max_attempts?: number;
    llm_calls?: number;
    repair_attempts?: number;
    execution_ms?: number;
    row_count?: number;
    rows?: Record<string, unknown>[];
    columns?: string[];
    termination_reason?: string;
  };
}

export interface AgentResult {
  sql: string | null;
  rows: Record<string, unknown>[];
  columns: string[];
  attempt: number;
  max_attempts: number;
  llm_calls: number;
  repair_attempts: number;
  execution_ms: number;
  row_count: number;
  status: string;
  termination_reason?: string;
}
