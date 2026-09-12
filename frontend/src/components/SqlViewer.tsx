import { useState } from "react";

interface SqlViewerProps {
  sql: string | null;
  title?: string;
}

export function SqlViewer({ sql, title = "Current SQL Query" }: SqlViewerProps) {
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    if (!sql) return;
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <section className="code-window-card">
      <div className="code-window-header">
        <div className="code-window-title">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="16 18 22 12 16 6" />
            <polyline points="8 6 2 12 8 18" />
          </svg>
          <span>{title}</span>
        </div>

        {sql && (
          <button type="button" onClick={handleCopy} className="copy-btn">
            {copied ? "Copied!" : "Copy SQL"}
          </button>
        )}
      </div>

      {sql ? (
        <pre className="code-block">
          <code>{sql}</code>
        </pre>
      ) : (
        <div className="code-empty">
          -- Generated or repaired SQL query will appear here.
        </div>
      )}
    </section>
  );
}
