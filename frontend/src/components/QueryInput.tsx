import { useState } from "react";

interface QueryInputProps {
  disabled: boolean;
  onSubmit: (query: string) => void;
}

const SAMPLE_QUERIES = [
  {
    label: "Pakistani Customers",
    query: "Show premium customers from Pakistan",
    broken: false,
  },
  {
    label: "Completed Revenue",
    query: "What is the total revenue from completed orders?",
    broken: false,
  },
  {
    label: "Failed Payments",
    query: "Show customers who have failed payments",
    broken: false,
  },
  {
    label: "Test Self-Healing",
    query: "SELECT customer_name, country FROM customers;",
    broken: true,
  },
];

export function QueryInput({ disabled, onSubmit }: QueryInputProps) {
  const [query, setQuery] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const trimmed = query.trim();

    if (!trimmed || disabled) {
      return;
    }

    onSubmit(trimmed);
  }

  function handleChipClick(sampleQuery: string) {
    if (disabled) return;
    setQuery(sampleQuery);
  }

  return (
    <div className="query-card">
      <form className="query-form" onSubmit={handleSubmit}>
        <div className="textarea-wrapper">
          <textarea
            className="query-textarea"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ask a question about your database in natural language (or enter SQL to test)..."
            rows={4}
            disabled={disabled}
          />
        </div>

        <div className="query-card-bottom">
          <div className="suggestions-cluster">
            <span className="suggestions-label">Suggestions:</span>
            {SAMPLE_QUERIES.map((sample) => (
              <button
                type="button"
                key={sample.label}
                disabled={disabled}
                onClick={() => handleChipClick(sample.query)}
                className={`suggestion-chip ${sample.broken ? "broken-query" : ""}`}
                title={sample.broken ? "Injects broken SQL to demonstrate self-healing" : sample.query}
              >
                {sample.label}
              </button>
            ))}
          </div>

          <button
            type="submit"
            disabled={disabled || !query.trim()}
            className="btn-primary"
          >
            {disabled ? (
              <>
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  className="spin-icon"
                  style={{ animation: "spin 1s linear infinite" }}
                >
                  <circle cx="12" cy="12" r="10" strokeOpacity="0.25" />
                  <path d="M12 2a10 10 0 0 1 10 10" />
                </svg>
                <span>Processing...</span>
              </>
            ) : (
              <span>Run Query</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
