import { useState } from "react";

interface QueryInputProps {
  disabled: boolean;
  onSubmit: (query: string) => void;
}

export function QueryInput({
  disabled,
  onSubmit,
}: QueryInputProps) {
  const [query, setQuery] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const trimmed = query.trim();

    if (!trimmed || disabled) {
      return;
    }

    onSubmit(trimmed);
  }

  return (
    <form
      className="query-form"
      onSubmit={handleSubmit}
    >
      <textarea
        value={query}
        onChange={(event) =>
          setQuery(event.target.value)
        }
        placeholder="Ask a question about your database..."
        rows={4}
        disabled={disabled}
      />

      <button
        type="submit"
        disabled={disabled || !query.trim()}
      >
        {disabled ? "Running..." : "Run Query"}
      </button>
    </form>
  );
}
